var chartDom = document.getElementById('barchart-container');
var myChart = echarts.init(chartDom);
var option;

option = {
  dataset: {
    source: [
      ['score', 'amount', 'region'],
      [100, 58212, '北京'],
      [80, 78254, '广东'],
      [60, 41032, '上海'],
      [40, 12755, '四川'],
      [20, 20145, '湖南']
    ]
  },
  grid: { containLabel: true },
  xAxis: { name: 'amount' },
  yAxis: { type: 'category' },
  visualMap: {
    orient: 'horizontal',
    left: 'center',
    min: 10,
    max: 100,
    text: ['High Score', 'Low Score'],
    // Map the score column to color
    dimension: 0,
    inRange: {
      color: ['#65B581', '#FFCE34', '#FD665F']
    }
  },
  series: [
    {
      type: 'bar',
      encode: {
        // Map the "amount" column to X axis.
        x: 'amount',
        // Map the "region" column to Y axis
        y: 'region'
      }
    }
  ]
};

option && myChart.setOption(option);
console.log("Barchart generating")