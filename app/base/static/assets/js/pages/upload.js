$(document).ready(function() {
    
    //$('#login').click(function() {
    $('form').submit(function (e) {
    
        var form_data = new FormData();
        form_data.append('myfile', $('#reportFile').prop('files')[0]);  
	
	
	// for trace files
	var ins = document.getElementById('traceFiles').files.length;		
	for (var x = 0; x < ins; x++) {
		//form_data.append("myfile2[]", document.getElementById('traceFiles').files[x]);
		form_data.append('myfile2[]', $('#traceFiles').prop('files')[x]);
	}
	
				
        $.ajax({
            xhr: function() {
		var xhr = new window.XMLHttpRequest();
		xhr.upload.addEventListener("progress", function(evt) {
		    if (evt.lengthComputable) {
		       // show working... in message
		        $('#message').show();
		        $("#message").html("Working..");
		        var percentComplete = (evt.loaded / evt.total) * 100;
		        // Place upload progress bar visibility code here
		        var percentVal = percentComplete.toFixed(0) + '%';
		        $('#progressbar').show();
		        $('#progressbar').val(percentComplete)
		        $('.percent').html(percentVal)
		    }
		}, false);
		return xhr;
	    },
	    
            type: "POST",
            url: '/submit-data',
            data: form_data, //$('form').serialize(),
            contentType: false,
            processData: false,
            dataType: 'json',
            
            //data: {
            //    username: $(".username").val(),
            //    password: $(".password").val()
            //},
            success: function(data)
            {
                 data = JSON.stringify(data)
                 console.log(data); 
                 $('#message').show();
                 $("#message").html(data);
		 //$('#form_upload').trigger("reset");
		 //$('#progressbar').val(0)
		 //$('.percent').html(0)
            },
            complete: function(xhr, textStatus) 
            {
            	console.log("AJAX Request complete -> ", xhr, " -> ", textStatus);
            },
            error: function (request, status, error) {
                $('#message').show();
        	$("#message").html(request.responseText);
            }
            
        });
        
        
        // block the traditional submission of the form.
        e.preventDefault(); 
    });



// Inject our CSRF token into our AJAX request.
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
                }
            }
        })
    });
