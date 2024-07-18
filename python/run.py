from preprocessing import *
from wc import *

# Currently used values. For some reason, the python/ has to be specified.
data_dir = 'python\detail_files\detail_files\post_details'
stopwords_dir = 'python/combined_stopwords.txt'
output_dir = 'json/wordcloud1.json'
encoding_type = 'utf-8'

start_date = '2024-01-01'
end_date = '2024-03-01'
output_amount = 100

# Get the data and export as csv, can be later used as import
generate_wordcloud_json(data_dir, stopwords_dir, output_dir, start_date, end_date, output_amount, encoding_type)