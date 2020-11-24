
function drawChart(chart_args) {
    var x_axis_labels = chart_args.x_axis_labels;
    var data_labels = chart_args.data_labels;
    var chart_data = chart_args.chart_data;
    var chart_type = chart_args.chart_type;
    var ctx = document.getElementById(chart_args.container_id).getContext('2d');

    if (window.chart != undefined)
        window.chart.destroy();
    window.chart = new Chart(ctx, {
	// The type of chart we want to create
	    type: chart_type,

	// The data for our dataset
        data: {
            labels: x_axis_labels,
            datasets: [{
                label: data_labels,
                backgroundColor: 'rgba(100, 100, 255, 0.5)',
                borderColor: 'rgb(55, 99, 132)',
                data: chart_data,
            }]
        },

	// Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    display: true
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }

    });
};
