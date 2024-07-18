# encoding:utf-8
import requests
import json

host = "https://api.map.baidu.com"
uri = "/geocoding/v3"
ak = "aMctpWf3LMEJwzPEV7dbxA7T9HTlcAcD"

# 读取JSON文件
json_file = 'json/addresses.json'
with open(json_file, 'r', encoding='utf-8') as file:
    addresses = json.load(file)

# 提取地址并统计每个地址的出现次数
address_counts = {}
for entry in addresses:
    address = entry['address']
    if address in address_counts:
        address_counts[address] += 1
    else:
        address_counts[address] = 1

results = []

# 遍历每个地址，获取经纬度
for address, count in address_counts.items():
    params = {
        "address": address,
        "output": "json",
        "ak": ak,
    }

    response = requests.get(url=host + uri, params=params)
    if response:
        data = response.json()
        if data['status'] == 0:
            location = data['result']['location']
            results.append({
                "lat": location['lat'],
                "lng": location['lng'],
                "count": count
            })

# 将结果保存为JSON文件
with open('json/Heatmap_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("经纬度获取并保存到Heatmap_data.json文件中")
