import os
import json

def parse_detail_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    detail = {}
    for line in lines:
        line = line.strip()
        if ': ' in line:
            key, value = line.split(': ', 1)
            detail[key] = value
    
    detail['笔记点赞数量'] = int(detail.get('笔记点赞数量', 0))
    detail['笔记收藏数量'] = int(detail.get('笔记收藏数量', 0))
    detail['笔记评论数量'] = int(detail.get('笔记评论数量', 0))
    detail['笔记分享数量'] = int(detail.get('笔记分享数量', 0))
    
    return detail

def read_data(base_dir):
    data = {}
    for user_folder in os.listdir(base_dir):
        user_path = os.path.join(base_dir, user_folder)
        if os.path.isdir(user_path):
            user_name = user_folder  # 保留整个文件夹名称，包括用户昵称和后面的乱码
            posts = []
            for post_file in os.listdir(user_path):
                if post_file.endswith('.txt'):
                    post_path = os.path.join(user_path, post_file)
                    post_data = parse_detail_file(post_path)
                    posts.append(post_data)
            if posts:  # 只有当有帖子时才加入用户数据
                data[user_name] = posts
    return data

# 更新数据文件夹路径
base_dir = r'D:\newdata_txt'
data = read_data(base_dir)

# 将数据写入 JSON 文件
with open('json/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


