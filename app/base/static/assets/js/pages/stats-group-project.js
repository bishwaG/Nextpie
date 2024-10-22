
/*
-------------------------------------------------------------------------------
Project run status by workflow
-------------------------------------------------------------------------------
*/
function status(data){
Highcharts.chart('proj-pipe-run', {
    credits: {enabled : false},
    title: {
        text: ''
    },
    accessibility: {
        point: {
            valueDescriptionFormat: '{index}. {point.from} to {point.to}, {point.weight}.'
        }
    },
    series: [{
        keys: ['from', 'to', 'weight'],
        data: data,
        type: 'sankey',
        name: 'Count'
    }]

});

}


$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "analysis/get-proj-pipe-run",
        dataType: "json",
        success: function(data) {
            status(data);
            //document.getElementById("global").innerHTML = data;
        }
     });
     
});




 /*
-------------------------------------------------------------------------------
detailed workflow runtime per project BUBBLE plot 
-------------------------------------------------------------------------------
*/

function bubble_plot(data){
Highcharts.chart('group-size', {
    credits: {enabled : false},
    chart: {
        type: 'packedbubble',
        height: '100%'
    },
    title: {
        text: '',
        align: 'left'
    },
    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value} project(s).</sub>'
    },
    legend:{ enabled:false },
    plotOptions: {
        packedbubble: {
            minSize: 1,
            maxSize: 300,
            zMin: 0,
            zMax: 100,
            layoutAlgorithm: {
                splitSeries: false,
                gravitationalConstant: 0.02
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}',
                filter: {
                    property: 'y',
                    operator: '>',
                    value: 250
                },
                style: {
                    color: 'black',
                    textOutline: 'none',
                    fontWeight: 'normal'
                }
            }
        }
    },
    series: data
});
}


$.ajax({
	type: "GET",
	url: "analysis/get-projects-in-group",
	dataType: "json",
	success: function(data) {
	    bubble_plot(data);
	    //document.getElementById("global").innerHTML = data;
	}
});




 /*
-------------------------------------------------------------------------------
Group process size and runtime
-------------------------------------------------------------------------------
*/


$.ajax({
	type: "GET",
	url: "analysis/get-per-group-workflow-runs-runtime",
	dataType: "json",
	success: function(data) {
	    
	    Highcharts.chart('p-size-runtime', {
            credits: {enabled : false},
	    chart: {
		type: 'variwide'
	    },

	    title: {
		text: ''
	    },


	    xAxis: {
		type: 'category',
		labels: { allowOverlap: false, 
		          rotation: 45 }
	    },

	    caption: {
		text: 'Column widths are proportional to runtime (hours)'
	    },

	    legend: {
		enabled: false
	    },

	    series: [{
		name: 'Total runtime',
		data: data,
		dataLabels: {
		    enabled: true,
		},
		tooltip: {
		    pointFormat: 'Workflow runs: <b> {point.y}</b><br>' +
		        'Total runtime: <b> {point.z} hr</b><br>'
		},
		borderRadius: 3,
		colorByPoint: true
	    }]

	});
	}
});





 /*
-------------------------------------------------------------------------------
Group workflow runs CIRCOS plot
-------------------------------------------------------------------------------
*/

(function(H) {
  H.seriesTypes.dependencywheel.prototype.pointClass.prototype.getDataLabelPath = function(a) {

                function EstimateLabelWidth(label) {
                    // Wasn't able to properly calculate the required width
                    // use label text length as a guide, this probably breaks if font size etc change a lot
                    return label.length * 5.6 + 15;
                }

                const c = this.series.chart.renderer;
                const f = this.shapeArgs;
                const e = 0 > this.angle || this.angle > Math.PI;
                const g = f.start;
                const b = f.end;

                this.dataLabelPath ||
                (this.dataLabelPath = c.arc({
                    open: true
                }).add(a));

                this.dataLabelPath.attr({
                    x: f.x,
                    y: f.y,
                    r: f.r + (this.series.options.dataLabels.distance || 0),
                    start: e ? g : b,
                    end: e ? b : g,
                    clockwise: +e
                });

                const availWidth = (f.r + (this.series.options.dataLabels.distance || 0)) * (b - g);

                if (EstimateLabelWidth(this.id) > availWidth) {
                    // if label won't fit then create an acronym
                    let shortName = this.id.toString();
                    if (EstimateLabelWidth(shortName) > availWidth) {
                        // acronym still too big so use just first letter
                        shortName = shortName.substring(0, 1);
                    }
                    a.textStr = "";
                    a.textSetter("");
                }

                return this.dataLabelPath;
            };
})(Highcharts);

$.ajax({
	type: "GET",
	url: "analysis/get-per-group-workflow-runs",
	dataType: "json",
	success: function(data) {
	    Highcharts.chart('per-group-workflow-runs', {
                    credits: {enabled : false},
		    title: {
			text: ''
		    },

		    accessibility: {
			point: {
			    valueDescriptionFormat: '{index}. From {point.from} to {point.to}: {point.weight}.'
			}
		    },
		    tooltip: {
            pointFormat: '<span>Workflow: {point.from}</span><br/><span>Group: {point.to:%e. %b}</span><br/><span>Workflow runs: {point.weight}</span>'
        },

		    series: [{
			keys: ['from', 'to', 'weight'],
			data: data,
			type: 'dependencywheel',
			name: '',
			dataLabels: {
			    color: '#333',
			    style: {
				textOutline: 'none'
			    },
			    textPath: {
				enabled: true
			    },
			    distance: 10
			},
			size: '95%',
			
		    },
		    ]

		});

	}
});



