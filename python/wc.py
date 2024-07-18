'''
Functions relating to taking text, parsing it, and generating a wordcloud.
Text should all be in one file, in the format: "朋友是一个坚韧不拔的纪录片...", i.e. already compiled from separate user posts
Separate functions for parsing text and generating wordcloud, because we only need to pass text to JS on website to generate live wordcloud
May need to be altered for compatibility with online data downloads and uploads
'''

# Imports
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import pandas as pd
from collections import OrderedDict
import json
from preprocessing import *

# Given a dataframe with post data, turn all the posts into one single string
def merge_text(df):
    all_text = ' '.join(df['text'])
    return all_text

# Use a local string variable, use after text has been merged from dataframe
def parse_text(text, stopwords_dir, encoding_type):
    raw_wordlist = jieba.cut(text)
    stopwords = set()
    with open(stopwords_dir, 'r', encoding=encoding_type) as file:
        for line in file:
            stopwords.add(line.strip())

    # Filter out all stopwords AND one-character phrases (probably not relevant)
    filtered_wordlist = [word for word in raw_wordlist if word not in stopwords and len(word) > 1]
    filtered_text = ' '.join(filtered_wordlist)
    return filtered_text

# Import from local .txt file (may need adaptation to online environment once deployed)
def import_parse_text(text_dir, stopwords_dir, encoding_type):
    # Import and parse text
    text = open(text_dir, 'rb').read()
    raw_wordlist = jieba.cut(text)

    # Import chinese stopwords set, remove stopwords from wordlist
    stopwords = set()
    with open(stopwords_dir, 'r', encoding=encoding_type) as file:
        for line in file:
            stopwords.add(line.strip())

    # Filter out all stopwords AND one-character phrases (probably not relevant)
    filtered_wordlist = [word for word in raw_wordlist if word not in stopwords and len(word) > 1]
    filtered_text = ' '.join(filtered_wordlist)
    return filtered_text

# Create a sorted dictionary containing the frequency of the words
def word_frequency(text):
    # Split the string into words
    words = text.split()
    
    # Create an empty dictionary to store the word frequencies
    freq_dict = {}
    
    # Iterate over each word in the list
    for word in words:
        # If the word is already in the dictionary, increment its count
        if word in freq_dict:
            freq_dict[word] += 1
        # If the word is not in the dictionary, add it with a count of 1
        else:
            freq_dict[word] = 1
    
    # Sort the dictionary by frequency in descending order and return it
    sorted_freq = OrderedDict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_freq

# Export a wordcloud formatted json file (WIP)
def create_wordcloud_json(sorted_freq, count=100, output_file='top_100_words_default.json'):
    # Calcualte a normalization factor using the total frequency of the first x amount of words (words to display)
    first_x = list(sorted_freq.values())[:count]
    totalCount = sum(first_x)
    print(f'Total count of first {count} words: {totalCount}')
    normFact = 2500/totalCount     # Normalization factor to ensure all wordclouds are roughly the same size

    # Get top x items in the already sorted dictionary, in proper format. Size is scaled based on total word count
    top_x = [{'text': word, 'size': freq * normFact} for word, freq in list(sorted_freq.items())[:count]]

    # Export into JSON
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(top_x, file, indent=4, ensure_ascii=False)
    print(f'Top {count} words exported as {output_file}')

    return top_x

# OVERALL FUNCTION: DEPRECATED
def generate_wordcloud_json(data_dir, stopwords_dir='combined_stopwords.txt', 
                            output_dir='json/default.json', start_date='2024-06-01', end_date='2024-06-02', 
                            output_amount=100, encoding_type='utf-8'):
    print(f'Generating wordcloud JSON from {data_dir}, outputting to {output_dir}')
    print(f'Start date: {start_date}, end date: {end_date}')
    df = create_dataframe_from_folder(data_dir)                                # Read the files and create a dataframe
    cut_df = cut_dataset(df, start_date, end_date)                              # Cut the dataframe to the selected timeframe
    all_text = merge_text(cut_df)                                               # Merge all the text data
    cut_text = parse_text(all_text, stopwords_dir, encoding_type)               # Parse all the text data using jieba
    word_count = word_frequency(cut_text)                                       # Count all the words in the text
    create_wordcloud_json(word_count, output_amount, output_file=output_dir)    # Create the wordcloud JSON based on word count
    print(f'Successfully generated wordcloud JSON file for top {output_amount} words ')
    print(f'JSON File saved to {output_dir}')

# FUNCTION FOR DJANGO HTTP REQUESTS
def backend_wordcloud_json(data_dir='python/detail_files/detail_files/post_details', 
                           stopwords_dir='python/combined_stopwords.txt', 
                           output_dir='json/default.json', 
                           start_date='2024-06-01', 
                           end_date='2024-06-02', 
                           output_amount=100, 
                           encoding_type='utf-8'):
    # Instead of generating a JSON file locally, return a JSON file so that the function in views.py can return to webpage
    print(f'Request received to generate wordcloud JSON between {start_date} and {end_date}.')
    df = create_dataframe_from_folder(data_dir)
    cut_df = cut_dataset(df, start_date, end_date)                                              # Cut the dataframe to the selected timeframe
    all_text = merge_text(cut_df)                                                               # Merge all the text data
    cut_text = parse_text(all_text, stopwords_dir, encoding_type)                               # Parse all the text data using jieba
    word_count = word_frequency(cut_text)                                                       # Count all the words in the text
    json_file = create_wordcloud_json(word_count, output_amount, output_file=output_dir)        # Create the wordcloud JSON based on word count
    print(f'Successfully generated wordcloud JSON file for top {output_amount} words.')

    return json_file

# Works!
# backend_wordcloud_json()