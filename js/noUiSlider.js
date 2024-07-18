// 我爱你 chatgpt

// Initialize noUiSlider
var dateSlider = document.getElementById('dateSlider');

noUiSlider.create(dateSlider, {
    range: {
        min: new Date('2020-01-01').getTime(),
        max: new Date().getTime()
    },
    step: 24 * 60 * 60 * 1000, // One day in milliseconds
    start: [new Date('2020-01-01').getTime(), new Date().getTime()],
    connect: true,
    tooltips: [true, true],
    format: {
        to: function (value) {
            return new Date(value).toISOString().split('T')[0];
        },
        from: function (value) {
            return Date.parse(value);
        }
    }
});

// Add event listener to the update button
document.getElementById('updateButton').addEventListener('click', function() {
    var filename = document.getElementById('fileInput').value;
    var dateValues = dateSlider.noUiSlider.get();
    var startDate = dateValues[0];
    var endDate = dateValues[1];

    if (!filename.startsWith("http")) {
        filename = `json/${filename}`;
    }

    loadWords(myWordCloud, filename, startDate, endDate);
});
