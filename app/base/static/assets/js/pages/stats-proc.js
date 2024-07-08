
/*=============================================================================
Process disk write
===============================================================================
*/
function procDiskWrite(data){

    // Get categories from first column
    var cat = [];
    data.forEach(function(item) {
        cat.push(item[0]);
    });


    Highcharts.chart('write', {
    credits: {enabled : false},
    chart:  { type: 'boxplot' },
    title:  { text: 'Disk Write' },
    legend: { enabled: true   },
    xAxis:  { categories: cat },
    yAxis: {
        title: { text: 'Gigabyte'}
    },
    series: [{
        name: 'Process',
        data: data,
        colorByPoint: true,
    }],
    tooltip: {
                headerFormat: '<b>Process: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' GB<br/>' +
                           'Q3: ' + this.q3  + ' GB<br/>' +
                           'Median: ' + this.median + ' GB<br/>' +
                           'Q1: ' + this.q1 + ' GB<br/>' +
                           'Min: ' + this.low + ' GB<br/>'
                }
    }

    });
}

/*=============================================================================
Process disk read
===============================================================================
*/
function procDiskRead(data){

    // Get categories from first column
    var cat = [];
    data.forEach(function(item) {
        cat.push(item[0]);
    });


    Highcharts.chart('read', {
    credits: {enabled : false},
    chart:  { type: 'boxplot' },
    title:  { text: 'Disk Read' },
    legend: { enabled: true   },
    xAxis:  { categories: cat },
    yAxis: {
        title: {
            text: 'Gigabyte'
        }
    },
    series: [{
        name: 'Process',
        data: data,
        colorByPoint: true,
    }],
    tooltip: {
                headerFormat: '<b>Process: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' GB<br/>' +
                           'Q3: ' + this.q3  + ' GB<br/>' +
                           'Median: ' + this.median + ' GB<br/>' +
                           'Q1: ' + this.q1 + ' GB<br/>' +
                           'Min: ' + this.low + ' GB<br/>'
                }
    }

    });
}

/*=============================================================================
Process runtime
===============================================================================
*/
function runtime(data){

// convert json to 2D list
var cat = [];
data.forEach(function(item) {
  cat.push(item[0]);
});


Highcharts.chart('runtime', {
credits: {enabled : false},
    chart:  { type: 'boxplot' },
    title:  { text: 'Runtime' },
    legend: { enabled: true   },
    xAxis:  { categories: cat },
    yAxis:  { 
        title: { text: 'Hours'}
    },
    series: [{
        name: 'Process',
        data: data,
        colorByPoint: true,
    }],
    tooltip: {
                headerFormat: '<b>Process: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' hr<br/>' +
                           'Q3: ' + this.q3  + ' hr<br/>' +
                           'Median: ' + this.median + ' hr<br/>' +
                           'Q1: ' + this.q1 + ' hr<br/>' +
                           'Min: ' + this.low + ' hr<br/>'
                }
    }

    });
}

/*=============================================================================
Memory consumer by processes
===============================================================================
*/
function memory(data){

// convert json to 2D list
var cat = [];
data.forEach(function(item) {
  cat.push(item[0]);
});


Highcharts.chart('memory', {
credits: {enabled : false},
    chart:  { type: 'boxplot'},
    title:  { text: 'Peak Memory'},
    legend: { enabled: true },
    xAxis:  { categories: cat},
    yAxis:  {
        title: {text: 'Gigabytes'}
    },
    series: [{
        name: 'Process',
        data: data,
        colorByPoint: true,
    }],
    tooltip: {
                headerFormat: '<b>Process: {point.key}</b><br/>',
                pointFormatter: function () {
                    return 'Max: ' + this.high + ' GB<br/>' +
                           'Q3: ' + this.q3  + ' GB<br/>' +
                           'Median: ' + this.median + ' GB<br/>' +
                           'Q1: ' + this.q1 + ' GB<br/>' +
                           'Min: ' + this.low + ' GB<br/>'
                }
    }

    });
}

/*
-------------------------------------------------------------------------------
Process run status
-------------------------------------------------------------------------------
*/
function procStatus (data) {

Highcharts.chart('proc-status', {
    credits: {enabled : false},
    chart: { type: 'pie'},
    title: { text: 'Process Status'},
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

/*
-------------------------------------------------------------------------------
Project run pipeline status
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




/*
-------------------------------------------------------------------------------
D O C U M E N T   R E A D Y    F U N C T I O N
-------------------------------------------------------------------------------
*/
$(document).ready(function() {
    
    // Process status (COMPLETED, ABORTED, FAILED, SUCCEDED)
     $.ajax({
        url: '/analysis/get-proc-status',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function (data) {
            procStatus(data);
        }
      });
    /*
    // Box plot of peak memory by processes
    $.ajax({
        url: '/analysis/get-each-proc-mem',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function (data) {
            boxPlot(data);
        }
    });
    
    // Process runtime Boxplot
    $.ajax({
        url: '/analysis/get-each-proc-runtime',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function (data) {
            runtime(data);
        }
    });
    
    // Process disk read
     $.ajax({
        url: '/analysis/get-each-proc-Diskread',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function (data) {
            procDiskRead(data);
        }
    });
    // process disk write
     $.ajax({
        url: '/analysis/get-each-proc-Diskwrite',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function (data) {
            procDiskWrite(data);
        }
    });
    */

    // aluvial plot
    $.ajax({
        type: "GET",
        url: "analysis/get-pipe-proc",
        dataType: "json",
        success: function(data) {
            status(data);
            //document.getElementById("global").innerHTML = data;
        }
     });
    
 });
