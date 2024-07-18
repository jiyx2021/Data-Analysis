import os
import re
import ast
import pandas as pd
from datetime import datetime

# Function to extract data from one single post (details.txt)
def extract_data_from_post(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Extract numeric data using regular expressions
    likes = re.search(r'笔记点赞数量:\s*(\d+)', content)
    likes = int(likes.group(1)) if likes else 0

    saves = re.search(r'笔记收藏数量:\s*(\d+)', content)
    saves = int(saves.group(1)) if saves else 0

    comments = re.search(r'笔记评论数量:\s*(\d+)', content)
    comments = int(comments.group(1)) if comments else 0

    shares = re.search(r'笔记分享数量:\s*(\d+)', content)
    shares = int(shares.group(1)) if shares else 0

    # Extract text data
    title = re.search(r'笔记标题:\s*(.*)', content)
    title = title.group(1) if title else ""

    text = re.search(r'笔记描述:\s*(.*)', content)
    text = text.group(1) if text else ""

    url = re.search(r'笔记url:\s*(.*)', content)
    url = url.group(1) if url else ""
    
    type = re.search(r'笔记类型:\s*(.*)', content)
    type = type.group(1) if type else ""

    ip = re.search(r'笔记ip归属地:\s*(.*)', content)
    ip = ip.group(1) if ip else ""

    # Extract upload date (don't care about exact time)
    time = re.search(r'笔记上传时间:\s*(.*)', content)
    time = time.group(1) if time else ""
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

    # Extract hashtags
    tags = re.search(r'笔记标签:\s*(\[\'.*\'])', content)
    tags = tags.group(1) if tags else ""
    if tags:
        tags = ast.literal_eval(tags)
    

    # Return all the extracted attributes in dictionary format
    return {
        'url': url,
        'type': type,
        'title': title,
        'text': text,
        'likes': likes,
        'saves': saves,
        'comments': comments,
        'shares': shares,
        'time': time,
        'tags': tags,
        'ip': ip
    }

# Function to traverse the dataset folder and create a DataFrame. DEPRECATED
def create_dataframe_from_dataset(dataset_folder):
    data = []
    
    for root, dirs, files in os.walk(dataset_folder):
        for file in files:
            if file == 'detail.txt':
                file_path = os.path.join(root, file)
                # print(f'Reading {file_path}')
                post_data = extract_data_from_post(file_path)
                data.append(post_data)
    
    df = pd.DataFrame(data)
    return df

# Changed to adapt to newest data format as of 07.12
def create_dataframe_from_folder(dataset_folder):
    data = []
    
    for root, dirs, files in os.walk(dataset_folder):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                post_data = extract_data_from_post(file_path)
                data.append(post_data)
    
    df = pd.DataFrame(data)
    return df

# Cut the dataset given a start date and end date
def cut_dataset(df, start_date, end_date):
    return df.loc[(df['time'] >= start_date) & (df['time'] <= end_date)]