import json
from pyecharts.charts import Map
from pyecharts import options as opts

# 读取JSON数据
json_file = 'json/addresses.json'
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计每个省份出现的次数，仅保留中国大陆的省份数据
province_counts = {}
for item in data:
    province = item['address']
    if province in ['北京', '天津', '上海', '重庆', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆']:
        if province in province_counts:
            province_counts[province] += 1
        else:
            province_counts[province] = 1

# 输出省份统计信息
print("省份统计信息：")
for province, count in province_counts.items():
    print(f"{province}: {count}")

# 创建地图对象
map_chart = (
    Map()
    .add(
        series_name="活跃度",
        data_pair=[(province, province_counts.get(province, 0)) for province in province_counts],
        maptype="china",
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=max(province_counts.values()),
            is_piecewise=True,
            range_color=["#f0f0f0", "#006edd", "#e0ffff"],  # 调整颜色范围
        ),
        title_opts=opts.TitleOpts(title="中国地图上各省份IP在社交媒体上的活跃度"),
    )
)

# 渲染地图到HTML文件
map_chart.render("中国IP活跃度地图.html")
