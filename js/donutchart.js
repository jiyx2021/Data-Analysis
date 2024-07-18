var chartDom = document.getElementById('donutchart-container');
var myChart = echarts.init(chartDom);
var option;

// This example requires ECharts v5.5.0 or later
option = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Posts that are...',
      type: 'pie',
      radius: ['40%', '100%'],
      center: ['50%', '90%'],
      // adjust the start and end angle
      startAngle: 180,
      endAngle: 360,
      data: [
        { value: 1048, name: 'Very Positive' },
        { value: 735, name: 'Somewhat Positive' },
        { value: 580, name: 'Neutral' },
        { value: 484, name: 'Somewhat Negative' },
        { value: 300, name: 'Very Negative' }
      ]
    }
  ]
};

option && myChart.setOption(option);
