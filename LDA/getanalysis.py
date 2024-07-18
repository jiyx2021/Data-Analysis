import os
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import defaultdict
from datetime import datetime
from textblob import TextBlob

# 自定义的JSON序列化器，处理numpy数据类型
def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError

# 读取 data.json 文件
with open('json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理每个用户的帖子数据
analysis_results = {}
for user, posts in data.items():
    # 初始化用户分析结果
    user_result = {
        'total_likes': 0,
        'total_favorites': 0,
        'total_comments': 0,
        'likes_over_time': {'dates': [], 'likes': []},
        'tags': [],
        'titles_descriptions': [],
        'likes_to_comments_ratio': 0,
        'likes_to_favorites_ratio': 0,
        'sentiments': {'positive': 0, 'neutral': 0, 'negative': 0},
        'lda_topics': [],
        'top_tags': []
    }
    
    tag_frequency = defaultdict(int)

    for post in posts:
        user_result['total_likes'] += post.get("笔记点赞数量", 0)
        user_result['total_favorites'] += post.get("笔记收藏数量", 0)
        user_result['total_comments'] += post.get("笔记评论数量", 0)
        
        # 收集时间和点赞数据
        upload_time_str = post.get("笔记上传时间", "")
        if upload_time_str:
            upload_time = datetime.strptime(upload_time_str, "%Y-%m-%d %H:%M:%S")
            user_result['likes_over_time']['dates'].append(upload_time.strftime("%Y-%m-%d"))
            user_result['likes_over_time']['likes'].append(post.get("笔记点赞数量", 0))
        
        # 收集标签和帖子内容
        tags_str = post.get("笔记标签", "[]")
        tags = eval(tags_str)
        user_result['tags'].extend(tags)
        title = post.get("笔记标题", "").strip()
        description = post.get("笔记描述", "").strip()
        if title:
            user_result['titles_descriptions'].append(title)
        if description:
            user_result['titles_descriptions'].append(description)
        
        # 统计标签频率
        for tag in tags:
            tag_frequency[tag] += 1
        
        # 情感分析
        text = f"{title} {description}".strip()
        if text:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            if polarity > 0:
                user_result['sentiments']['positive'] += 1
            elif polarity == 0:
                user_result['sentiments']['neutral'] += 1
            else:
                user_result['sentiments']['negative'] += 1
    
    # 计算点赞评论比和点赞收藏比
    if user_result['total_comments'] > 0:
        user_result['likes_to_comments_ratio'] = user_result['total_likes'] / user_result['total_comments']
    if user_result['total_favorites'] > 0:
        user_result['likes_to_favorites_ratio'] = user_result['total_likes'] / user_result['total_favorites']
    
    # 获取使用频率最高的前五个标签
    sorted_tags = sorted(tag_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    user_result['top_tags'] = [tag[0] for tag in sorted_tags]
    
    # 计算 LDA 主题模型
    vectorizer = CountVectorizer(token_pattern=r'\b\w+\b', stop_words='english')
    texts = [' '.join(user_result['titles_descriptions'])]
    
    # 输出检查文本数据
    print(f"User: {user}")
    print(f"Texts: {texts[:10]}")  # 输出前10个文本以进行检查

    if texts and any(text.strip() for text in texts):
        dtm = vectorizer.fit_transform(texts)
        lda = LatentDirichletAllocation(n_components=5, random_state=0)
        lda.fit(dtm)
        
        for topic_idx, topic in enumerate(lda.components_):
            topic_words = {vectorizer.get_feature_names_out()[i]: float(topic[i]) for i in topic.argsort()[:-11:-1]}
            user_result['lda_topics'].append({'topic': topic_idx, 'words': topic_words})
    else:
        print(f"No valid texts for user {user}")

    # 将用户分析结果添加到最终结果中
    analysis_results[user] = user_result

# 将分析结果保存到 JSON 文件
with open('json/analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, default=convert, ensure_ascii=False, indent=4)
