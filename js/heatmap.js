var map = new BMap.Map("container",{minZoom:4,maxZoom:5});          
var point = new BMap.Point(78.480237, 48.236305); // 设置中心点坐标
map.centerAndZoom(point, 4); // 初始化地图，设置中心点坐标和地图级别
map.enableScrollWheelZoom(); // 允许滚轮缩放
  
// AJAX 请求加载 JSON 数据
fetch('json/Heatmap_data.json')
    .then(response => response.json())
    .then(data => {
        var points = data;

        if(!isSupportCanvas()){
            alert('热力图目前只支持有canvas支持的浏览器,您所使用的浏览器不能使用热力图功能~');
            return;
        }

        heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":20});
        map.addOverlay(heatmapOverlay);
        heatmapOverlay.setDataSet({data:points, max:150});

        // 是否显示热力图
        openHeatmap();
    })
    .catch(error => console.error('Error loading JSON data:', error));

function openHeatmap(){
    heatmapOverlay.show();
}
function closeHeatmap(){
    heatmapOverlay.hide();
}

function setGradient(){
    var gradient = {};
    var colors = document.querySelectorAll("input[type='color']");
    colors = [].slice.call(colors,0);
    colors.forEach(function(ele){
        gradient[ele.getAttribute("data-key")] = ele.value; 
    });
    heatmapOverlay.setOptions({"gradient":gradient});
}

// 判断浏览区是否支持canvas
function isSupportCanvas(){
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));
}

// 调整地图中心
function adjustMapCenter() {
    map.centerAndZoom(point, 6);
}

window.addEventListener('resize', adjustMapCenter);