// lda.js
async function fetchLDAData() {
    const response = await fetch('json/LDA_analysisdata.json');
    return await response.json();
}

function createPieChart(ctx, labels, data) {
    const backgroundColors = [
        '#FF6384',   // 红色
        '#36A2EB',   // 蓝色
        '#FFCE56',   // 鲜黄色
        '#008B8B',   // 紫色
        '#FF6347',   // 橙红色
        '#00CED1',   // 青色
        '#9370DB',   // 紫色
        '#FF8C00',   // 橙色
        '#32CD32',   // 鲜绿色
        '#DAA520'    // 金色
    ];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors.slice(0, labels.length),
            }]
        },
        options: {
            responsive: false, // 设置为false
            maintainAspectRatio: false, // 取消宽高比保持
        }
    });
}

async function renderCharts() {
    const ldaData = await fetchLDAData();
    const container = document.getElementById('charts');

    Object.keys(ldaData).forEach((topic, index) => {
        const canvasContainer = document.createElement('div');
        canvasContainer.classList.add('chart-container');
        const canvas = document.createElement('canvas');
        canvas.id = `chart-${index}`;
        canvasContainer.appendChild(canvas);
        container.appendChild(canvasContainer);

        const labels = ldaData[topic].map(item => item[0]);
        const data = ldaData[topic].map(item => item[1]);

        createPieChart(document.getElementById(`chart-${index}`).getContext('2d'), labels, data);
    });
}

renderCharts();
