import json

def extract_addresses_to_json(json_file, output_json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        user_data = json.load(file)
    
    addresses = []
    for user_posts in user_data.values():
        for post in user_posts:
            addresses.append({"address": post['笔记ip归属地']})
    
    with open(output_json_file, 'w', encoding='utf-8') as file:
        json.dump(addresses, file, ensure_ascii=False, indent=4)
    
    print(f'地址数据已保存到 {output_json_file}')

# 设置JSON文件路径和输出JSON文件路径
json_file = 'json/data.json'
output_json_file = 'json/addresses.json'

# 提取地址并生成JSON文件
extract_addresses_to_json(json_file, output_json_file)
