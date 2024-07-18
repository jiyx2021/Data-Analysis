// 动态加载 JSON 文件
fetch('analysis_results.json')
    .then(response => response.json())
    .then(analysisResults => {
        const userListElement = document.getElementById('userList');
        const userNameElement = document.getElementById('userName');
        const ctx1 = document.getElementById('likesOverTimeChart').getContext('2d');
        const ctx2 = document.getElementById('ratiosChart').getContext('2d');
        const tagsListElement = document.getElementById('topTags');
        let likesOverTimeChart, ratiosChart;

        // Function to clean user names
        function cleanUserName(userName) {
            return userName.split('_')[0];
        }

        // Populate user list
        Object.keys(analysisResults).forEach(key => {
            const li = document.createElement('li');
            li.textContent = cleanUserName(key);
            li.addEventListener('click', () => showUserData(key));
            userListElement.appendChild(li);
        });

        function showUserData(user) {
            const userData = analysisResults[user];
            userNameElement.textContent = `Data for ${cleanUserName(user)}`;

            // Destroy previous charts if they exist
            if (likesOverTimeChart) likesOverTimeChart.destroy();
            if (ratiosChart) ratiosChart.destroy();

            // Likes over time chart
            likesOverTimeChart = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: userData.likes_over_time.dates,
                    datasets: [{
                        label: '点赞数',
                        data: userData.likes_over_time.likes,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: '日期'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: '点赞数'
                            }
                        }
                    }
                }
            });

            // Ratios chart
            ratiosChart = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['转化一个评论需要的点赞数', '转化一个收藏需要的点赞数'],
                    datasets: [{
                        label: '比值',
                        data: [userData.likes_to_comments_ratio, userData.likes_to_favorites_ratio],
                        backgroundColor: ['rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'],
                        borderColor: ['rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '比值'
                            }
                        }
                    }
                }
            });

            // 显示用户最常用的5个标签
            tagsListElement.innerHTML = '<h3>使用最多的5个tags</h3>';
            const topTags = userData.top_tags.slice(0, 5);
            topTags.forEach(tag => {
                const li = document.createElement('li');
                li.textContent = tag;
                tagsListElement.appendChild(li);
            });
        }
    })
    .catch(error => console.error('Error loading analysis_results.json:', error));