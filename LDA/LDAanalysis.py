import json
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# 读取data.json
with open('json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 停用词列表
stop_words = set([
    "一些", "可以", "喜欢", "这个", "我们", "你们", "他们", "我的", "你的", "他的","还是","真的","这么","一个","觉得","直接","出来","最近","大家","很多",
    "它的", "会", "还", "而且", "并且", "但是", "然后", "就是", "没有", "以及", "自己", "一直","一下","不错","感觉","现在","开始","这是","什么","哈哈哈","比较","不是","应该","每天","每次","不要"
])

# 提取所有帖子的描述文本
texts = [post['笔记描述'] for user_posts in data.values() for post in user_posts if '笔记描述' in post]

# 分词并去除停用词
def tokenize(text):
    words = jieba.lcut(text)
    return [word for word in words if word not in stop_words]

tokenized_texts = [" ".join(tokenize(text)) for text in texts]

# 构建词频矩阵
vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000)
tf = vectorizer.fit_transform(tokenized_texts)

# LDA分析
n_topics = 5
lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
lda.fit(tf)

# 提取主题词及其频率
def get_top_words_and_frequencies(model, feature_names, n_top_words):
    topics = {}
    for topic_idx, topic in enumerate(model.components_):
        total_frequency = np.sum(topic)
        topic_words = [(feature_names[i], topic[i] / total_frequency) for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics[f'Topic {topic_idx + 1}'] = topic_words
    return topics

tf_feature_names = vectorizer.get_feature_names_out()
n_top_words = 10
topics = get_top_words_and_frequencies(lda, tf_feature_names, n_top_words)

# 生成LDA_analysisdata.json
with open('json/LDA_analysisdata.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, ensure_ascii=False, indent=4)
