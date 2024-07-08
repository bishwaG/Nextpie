/*
-------------------------------------------------------------------------------
Pipeline I/O
-------------------------------------------------------------------------------
*/

function memory(data){
    Highcharts.chart('io', {
    credits: {enabled : false},
    chart:{
        type:'areaspline',
        zoomBySingleTouch: true,
        zoomType: 'x'
    },
    title: {
        text: 'Disk I/O'
    },

    data: {
        csv: data
    },
    yAxis: {
        title: {
            text: 'Terabytes'
        }
    },
    xAxis: {
      type: "datetime",
      labels: {
        formatter: function() {
          return Highcharts.dateFormat('%Y-%b-%e', this.value);
        }
      }
    },
    tooltip: {
        shared: true,
        crosshairs: true
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        },
        series: {
            marker: {
                enabled: true
            }
        }
    },
    credits: {
        enabled: false
    },
        
});
}

    $(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "analysis/get-run-io",
        dataType: "text",
        success: function(data) {
            memory(data);
        }
     });
});


/*
-------------------------------------------------------------------------------
Pipeline timeine
-------------------------------------------------------------------------------
*/






$(document).ready(function() {
 $.ajax({
    url: '/analysis/get-run-events',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        
        
        Highcharts.chart('run-timeline', {
            credits: {enabled : false},
	    chart: {
		zoomType: 'x',
		type: 'timeline'
	    },
	    xAxis: {
		type: 'datetime',
		visible: false
	    },
	    yAxis: {
		gridLineWidth: 1,
		title: null,
		labels: {
		    enabled: false
		}
	    },
	    legend: {
		enabled: false
	    },
	    title: {
		text: 'Workflow timeline'
	    },
	    subtitle: {
		text: ''
	    },
	    tooltip: {
		style: {
		    width: 300
		}
	    },
	    series: [{
		dataLabels: {
		    allowOverlap: false,
		    format: '<span style="font-weight: bold;" > ' +
		        '{point.x:%d %b %Y}</span><br/>{point.label}'
		},
		marker: {
		    symbol: 'circle'
		},
		data: data
	    }]
});

    }
  });
 });

/*
-------------------------------------------------------------------------------
Workflow Run Status
-------------------------------------------------------------------------------
*/


$(document).ready(function() {
 $.ajax({
    url: '/analysis/get-pipe-status',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        Highcharts.chart('pipe-status', {
            credits: {enabled : false},
	    chart: {
		type: 'pie'
	    },
	    title: {
		text: ''
	    },
	    tooltip: {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b><br/> Count: {point.y}'
	    },
	    plotOptions: {
		pie: {
		    allowPointSelect: true,
		    cursor: 'pointer',
		    dataLabels: {
		        enabled: true,
		        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
		    }
		}
	    },
	    series: [{
		name: 'Percentage',
		colorByPoint: true,
		data: data
	    }]
	});
    }
  });
 });


/*
-------------------------------------------------------------------------------
Workflow status by version
-------------------------------------------------------------------------------
*/



$(document).ready(function() {
 $.ajax({
    url: '/analysis/get-pipe-ver-status',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        Highcharts.chart('pipe-ver-status', {
	    credits: {enabled : false},
	    title: {
		text: ''
	    },
	    accessibility: {
		point: {
		    valueDescriptionFormat: '{index}. {point.from} to {point.to}, {point.weight}.'
		}
	    },
	    xAxis: {categories:['Pipelines', 'version', 'status']},
	    series: [{
	        showInLegend: false,
		keys: ['from', 'to', 'weight','color'],
		data: data,
		type: 'sankey',
		name: 'Count'
	    }]

	});
    }
  });
 });
 

/*
-------------------------------------------------------------------------------
Run runtime by workflows
-------------------------------------------------------------------------------
*/
 
function runRuntime(data){

// convert json to 2D list
var cat = [];
data.forEach(function(item) {
  cat.push(item[0]);
});


Highcharts.chart('run-runtime', {
    credits: {enabled : false},
    chart:  { type: 'boxplot' },
    title:  { text: 'Runtime' },
    legend: { enabled: true   },
    xAxis:  { categories: cat },
    yAxis:  { 
        title: { text: 'Hours'}
    },
    series: [{
        name: 'Workflows',
        data: data,
        colorByPoint: true,
        showInLegend: false,
    }],
    tooltip: {
                headerFormat: '<b>Workflow: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' hr<br/>' +
                           'Q3: ' + this.q3  + ' hr<br/>' +
                           'Median: ' + this.median + ' hr<br/>' +
                           'Q1: ' + this.q1 + ' hr<br/>' +
                           'Min: ' + this.low + ' hr<br/>'
                }
    },
     plotOptions: {
        boxplot: {
            //boxDashStyle: 'Dash',
            fillColor: '#dddddd',
            lineWidth: 4,
            //medianColor: '#0C5DA5',
            //medianDashStyle: 'ShortDot',
            medianWidth: 4,
            //stemColor: '#A63400',
            //stemDashStyle: 'dot',
            stemWidth: 4,
            //whiskerColor: '#3D9200',
            //whiskerLength: '20%',
            whiskerWidth: 4
        }
    },
        
        

    });
}
 
 
 $(document).ready(function() {
 $.ajax({
    url: '/analysis/get-run-runtime',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        runRuntime(data);
    }
  });
 });
 

 /*
-------------------------------------------------------------------------------
Run runtime vs process counts
-------------------------------------------------------------------------------
*/

Highcharts.setOptions({
    colors: ['rgba(5,141,199,0.5)', 'rgba(80,180,50,0.5)', 'rgba(237,86,27,0.5)']
});



 $.ajax({
    url: '/analysis/runtime-process-count',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        Highcharts.chart('runtime-pc-count', {
            credits: {enabled : false},
	    chart: {
		type: 'bubble',
		plotBorderWidth: 1,
		zoomType: 'xy'
	    },
	    tooltip: {
            pointFormat: 'Runtime: {point.x} hr <br/> Memory: {point.y} GB <br/> Processes: {point.z}'
        },

	    title: {
		text: 'Workflow runtime vs. memory consumed'
	    },
	     subtitle: {
        	text: 'Workflow run (each bubble) runtime vs. memory with process count (bubble size)'
    	   },

	    xAxis: {
		title: {
                text: 'Runtime (hours)'
            }
	    },

	    yAxis: {
		title: {
                text: 'Memory (GB)'
            }
	    },

	    series: [ {
		data: data,
		//sizeBy: 'width',
		//name: 'Size by width'
		showInLegend: false,
	    }]

	});
    }
  });
  


 /*
-------------------------------------------------------------------------------
Run I/O by workflows
-------------------------------------------------------------------------------
*/
 
function runIO(data, div){

// convert json to 2D list
var cat = [];
data.forEach(function(item) {
  cat.push(item[0]);
});


Highcharts.chart(div, {
    credits: {enabled : false},
    chart:  { type: 'boxplot' },
    title:  { text: div },
    legend: { enabled: true   },
    xAxis:  { categories: cat },
    yAxis:  { 
        title: { text: 'TB'}
    },
    series: [{
        name: 'Workflows',
        data: data,
        colorByPoint: true,
        showInLegend: false,
    }],
    tooltip: {
                headerFormat: '<b>Workflow: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' TB<br/>' +
                           'Q3: ' + this.q3  + ' TB<br/>' +
                           'Median: ' + this.median + ' TB<br/>' +
                           'Q1: ' + this.q1 + ' TB<br/>' +
                           'Min: ' + this.low + ' TB<br/>'
                }
    },
     plotOptions: {
        boxplot: {
            //boxDashStyle: 'Dash',
            fillColor: '#ffffff',
            lineWidth: 4,
            //medianColor: '#0C5DA5',
            //medianDashStyle: 'ShortDot',
            medianWidth: 4,
            //stemColor: '#A63400',
            //stemDashStyle: 'dot',
            stemWidth: 4,
            //whiskerColor: '#3D9200',
            //whiskerLength: '20%',
            whiskerWidth: 4
        }
    },
        
        

    });
}
 
 // Run disk read
 $(document).ready(function() {
 $.ajax({
    url: '/analysis/get-run-io-read',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        runIO(data,"read");
    }
  });
  
  // Run disk write
 $.ajax({
    url: '/analysis/get-run-io-write',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        runIO(data,"write");
    }
  });
  
 });





