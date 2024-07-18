var chartDom = document.getElementById('polar-chart');
var myChart = echarts.init(chartDom);
var option;

option = {
  title: [
    {
      text: ''
    }
  ],
  polar: {
    radius: [30, '80%']
  },
  angleAxis: {
    max: 100,
    startAngle: 75
  },
  radiusAxis: {
    type: 'category',
    data: ['Likes', 'Comments', 'Shares']
  },
  tooltip: {},
  series: {
    type: 'bar',
    data: [
        {
        value: 100,
        itemStyle: {
            color: '#ff9800'
        }
        },
        {
        value: 70,
        itemStyle: {
            color: '#9c27b0'
        }
        },
        {
        value: 30,
        itemStyle: {
            color: '#4Caf50'
        }
        },
    ],
    coordinateSystem: 'polar',
    label: {
      show: true,
      position: 'middle',
      formatter: '{b}: {c}'
    }
  }
};

option && myChart.setOption(option);
console.log('Polar chart polar chart')