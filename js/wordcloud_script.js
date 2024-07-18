function wordCloud(selector) {
    var fill = d3.scale.category20();

    // Append the SVG container
    var svg = d3.select(selector)
                .append("svg")
                .attr("width", "100%")
                .attr("height", "100%");

    // Append a single 'g' element for the word cloud
    var g = svg.append("g");

    // Function to draw the words
    function draw(words) {
        // Get the width and height of the container
        var containerWidth = parseInt(d3.select(selector).style("width"));
        var containerHeight = parseInt(d3.select(selector).style("height"));
        var centerX = containerWidth / 2;
        var centerY = containerHeight / 2;

        // Update the 'g' element's transform attribute to center the word cloud
        g.attr("transform", "translate(" + centerX + "," + centerY + ")");

        // Bind the word data to text elements
        var cloud = g.selectAll("text")
                     .data(words, function(d) { return d.text; });

        // Entering words: append new text elements for each word
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });

        // Entering and updating words: transition to the new word positions and sizes
        cloud.transition()
            .duration(600)
            .style("font-size", function(d) { return d.size + "px"; })
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("fill-opacity", 1);

        // Exiting words: fade out and remove the old words
        cloud.exit()
            .transition()
            .duration(200)
            .style('fill-opacity', 1e-6)
            .attr('font-size', 1)
            .remove();
    }

    return {
        update: function(words) {
            // Use the container dimensions to size the layout
            var containerWidth = parseInt(d3.select(selector).style("width"));
            var containerHeight = parseInt(d3.select(selector).style("height"));

            // Configure the layout and start it
            d3.layout.cloud().size([containerWidth, containerHeight])
                .words(words)
                .padding(3)
                .rotate(function() { return ~~(Math.random() < 0.5 ? -1 : 1) * 0; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();
        }
    }
}

// Part of the wordCloud script
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initialized wordcloud');
    // Call the function to initialize and generate the word cloud only if not initialized before
    var myWordCloud = wordCloud("#wordcloud_container");

    // Define the start and end dates
    var startDate = new Date('2024-01-01').getTime();
    var endDate = new Date('2024-07-01').getTime();

    console.log("Start Date Timestamp:", startDate);
    console.log("End Date Timestamp:", endDate);

    // Initialize the noUiSlider
    var slider = document.getElementById("dateSlider");
    noUiSlider.create(slider, {
        range: {
            min: startDate,
            max: endDate
        },
        start: [startDate, endDate], // Correct initial positions of the two handles
        connect: true, // Connect the two handles with a colored bar
        tooltips: [true, true], // Show tooltips for both handles
        format: {
            to: function(value) {
                var date = new Date(value);
                if (isNaN(date.getTime())) {
                    return '';
                }
                return date.toISOString().split('T')[0];
            },
            from: function(value) {
                var date = new Date(value);
                if (isNaN(date.getTime())) {
                    return 0;
                }
                return date.getTime();
            }
        }
    });

    // Explicitly set the slider handle values to ensure they are correct
    slider.noUiSlider.setHandle(0, startDate);
    slider.noUiSlider.setHandle(1, endDate);

    console.log("Slider initial start values: ", [startDate, endDate]);
    console.log("Slider values after set: ", slider.noUiSlider.get());

    document.getElementById("updateButton").addEventListener("click", function() {
        var filename = document.getElementById("fileInput").value;
        var sliderValues = slider.noUiSlider.get();
        loadWords(myWordCloud, filename, sliderValues);
    });

    // Load the initial word cloud
    var initialSliderValues = slider.noUiSlider.get();
    loadWords(myWordCloud, 'json/wordcloud1.json', initialSliderValues);

});

// Function to load words from JSON and update the word cloud
function loadWords(vis, filename, sliderValues) {
    console.log("sliderValues argument: ", sliderValues); // Log the sliderValues argument


    if (filename.startsWith("http")) {
        fetch(filename)
            .then(response => response.json())
            .then(words => {
                vis.update(words);
            });
    } else {
        d3.json(filename, function(error, words) {
            if (error) throw error;
            vis.update(words);
        });
    }
}
