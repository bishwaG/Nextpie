/*
-------------------------------------------------------------------------------
D O C U M E N T   R E A D Y    F U N C T I O N
-------------------------------------------------------------------------------
*/
// Function for monthly run bar plot
function monthly(data, plot_type, div, main_title, yaxis_title, unit)
{
	Highcharts.chart(div, {
	    chart: { type: plot_type },
	    title: { text: main_title },
	    subtitle: { text: '' },
	    xAxis: {
		categories: [
		    'January','February','March','April','May','June',
		    'July','August','September','October','November','Decmber'
		],
		crosshair: true
	    },
	    yAxis: {
		min: 0,
		title: {
		    text: yaxis_title
		}
	    },
	    plotOptions: {
		bar: {
		    dataLabels: {
		        enabled: true
		    }
		}
	    },
	    tooltip: {
		headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
		pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
		    '<td style="padding:0"><b>{point.y} '+unit+'</b></td></tr>',
		footerFormat: '</table>',
		shared: true,
		useHTML: true
	    },
	    plotOptions: {
		column: {
		    pointPadding: 0.2,
		    borderWidth: 0
		}
	    },
	    credits: {
                enabled: false
            },
	    series: data,
	});
}



function monthlyStatus(data){
Highcharts.chart('month-status', {
    chart: { type: 'column' },
    title: { text: 'Workflow status of current year'},
    xAxis: {
        categories: [
		    'January','February','March','April','May','June',
		    'July','August','September','October','November','Decmber'
		]
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Count'
        },
        stackLabels: {
            enabled: true,
            style: {
                fontWeight: 'bold',
                color: ( // theme
                    Highcharts.defaultOptions.title.style &&
                    Highcharts.defaultOptions.title.style.color
                ) || 'gray'
            }
        }
    },
    legend: {
        align: 'right',
        x: -30,
        verticalAlign: 'top',
        y: 25,
        floating: true,
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || 'white',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: true
            }
        }
    },
    series: data
});

}
// DB counts
 $.ajax({
    url: '/info/db',
    type: 'GET',
    async: true,
    dataType: "json",
    success: function (data) {
        $("#groups").html( data[0]["groups"] );
        $("#projects").html( data[0]["projects"] );
        $("#runs").html( data[0]["runs"] );
        $("#processes").html( data[0]["processes"] );
    }
  });


// Get monthly run counts
$.ajax({
url: 'analysis/monthly/runs',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {
    //monthlyRuns(data);
    monthly(data, plot_type="column", div="month-run", main_title="Workflow/pipeline runs", yaxis_title="Count", unit="");
}
});

// Get monthly footprint
$.ajax({
url: 'analysis/monthly/disk',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {
    //monthlyDisk(data);
    monthly(data, plot_type="column", div="month-disk", main_title="Data footprint", yaxis_title="Terabytes", unit="TB");
}
});


// Get monthly memory usage
$.ajax({
url: 'analysis/monthly/memory',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {
    //monthlyMemory(data);
    monthly(data, plot_type="column", div="month-memory", main_title="Memory usage", yaxis_title="Terabytes", unit="TB");
}
});

// Get monthly workflow status
$.ajax({
url: 'analysis/monthly/status',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {
    monthlyStatus(data);
}
});

// Get monthly projects
$.ajax({
url: 'analysis/monthly/projects',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {
    monthly(data, plot_type="column", div="month-projects", main_title="Analysis projects", yaxis_title="count", unit="");
}
});

// Dashboard's top statistics
$.ajax({
url: 'info/this-year-runs',
type: 'GET',
async: true,
dataType: "json",
success: function (data) {

  // yearly runs ---------------------------------------------------------------
	var arr = ["yearly-runs", "monthly-runs", "yearly-foot"];
	for(i in arr){
    console.log(arr[i]);
		var div_val  = "#"+arr[i];
		var div_per  = "#"+arr[i]+"-per";
		var div_prog = "#"+arr[i]+"-progress";

		var mydata,mydata_per;

		if(arr[i] == "yearly-runs"){
			mydata = data["runs_this_year"];
			mydata_per = data["year_percent_change"];

		}else if(arr[i] == "monthly-runs"){
			mydata = data["runs_this_month"];
			mydata_per = data["month_percent_change"];

		}else if(arr[i] == "yearly-foot"){
			mydata = data["footprint_this_year"];
			mydata_per = data["footprint_percent_change"];
		}
		// set value
		$(div_val).html(mydata);

		// negative percent: DOWN ARROW, NO PROGRESS BAR
		if(mydata_per < 0){
			$(div_val).html("<i class=\"feather icon-arrow-down text-c-red f-30 m-r-10\"></i>"+mydata);
			$(div_per).html(mydata_per+"%");
			$(div_prog).css("width", 0 +"%");
		// positive percent: UP ARROW, PROGRESS BAR
		}else if(mydata_per>0){
			$(div_val).html("<i class=\"feather icon-arrow-up text-c-green f-30 m-r-10\"></i>"+mydata);
			$(div_per).html(mydata_per+"%");

			// for percent above 100
			if(mydata_per >= 100)
				$(div_prog).css("width", 100 +"%");
			else if (mydata_per < 100)
				$(div_prog).css("width", mydata_per +"%");
		}

}

}


});
