
// form reset ------------------------------------------------------------------
document.getElementById("reset-button").addEventListener("click", function() {
        //if (confirm("Are you sure you want to reset the form?")) {
            document.getElementById("form_upload").reset();
        //}
    });


// function to remove texts ----------------------------------------------------
const fileInput = document.getElementById("fileInput");
const textInputs = document.querySelectorAll("input[type='text']");

// Function to clear content letter by letter with flashing effect
function clearContentWithFlashing(inputField) {
    let currentValue = inputField.value;
    let index = currentValue.length;
    let isOrange = false;  // Toggle for flashing effect

    // Start flashing effect
    const flashInterval = setInterval(() => {
        inputField.style.backgroundColor = isOrange ? "white" : "orange"; // Toggle between red and white
        isOrange = ! isOrange;
    }, 250); // Flash every x ms

    // Interval to remove one character at a time
    const textRemoveInterval = setInterval(() => {
        if (index > 0) {
            inputField.value = currentValue.substring(0, index - 1); // Remove one letter
            index--;
        } else {
            clearInterval(textRemoveInterval); // Stop text removal
            clearInterval(flashInterval); // Stop flashing effect
            inputField.style.backgroundColor = "white"; // Reset background to normal
        }
    }, 300); // Adjust this to control the speed (milli seconds)
}

// document ready function
$(document).ready(function() {
    
    //submit
    $('form').submit(function (e) {
    
        
        var form_data = new FormData();
        form_data.append("workflowName", $("#workflowName").val());
        form_data.append("workflowVer", $("#workflowVer").val());
        form_data.append("groupName", $("#groupName").val());
        form_data.append("projectName", $("#projectName").val());
        
        if($("#reportFile")[0].files.length >0){
        	form_data.append('reportFile', $('#reportFile').prop('files')[0]);
		textInputs.forEach(input => {
                clearContentWithFlashing(input);  // Clear content of each input field letter by letter
            });
	}

	// for trace files
	var ins = document.getElementById('traceFiles').files.length;
	for (var x = 0; x < ins; x++) {
		//form_data.append("myfile2[]", document.getElementById('traceFiles').files[x]);
		form_data.append('traceFile[]', $('#traceFiles').prop('files')[x]);
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
                 //data = JSON.stringify(data)
                 console.log("AJAX success!"); 
                 console.log(data); 
                 $('#message').show();
                 $("#message").html(data.message);
		 //$('#form_upload').trigger("reset");
		 //$('#progressbar').val(0)
		 //$('.percent').html(0)
		 
		
		const messageDiv = $("#message");
		const messageText = $("#message-text");

		messageText.html(data);
		

		if (data.response === "warning") {
		  messageDiv.removeClass("alert-info alert-success alert-danger alert-warning");
		  messageDiv.addClass("alert alert-warning alert-dismissible fade show");
		} else if (data.response === "success") {
		  messageDiv.removeClass("alert-info alert-success alert-danger alert-warning");
		  messageDiv.addClass("alert alert-success alert-dismissible fade show");
		} else if (data.response === "error") {
		  messageDiv.removeClass("alert-info alert-success alert-danger alert-warning");
		  messageDiv.addClass("alert alert-danger alert-dismissible fade show");
		}

		messageDiv.fadeIn();
		 
		 
            
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


        
// for displaying report file after loading a file.
document.getElementById("reportFile").addEventListener("change", function(event) {
    const file = event.target.files[0]; // Get the selected file

    if (file) {   	
    	textInputs.forEach(input => {
                clearContentWithFlashing(input);  // Clear content of each input field letter by letter
            });
    	
        const reader = new FileReader();

        // Define what happens when reading is complete
        reader.onload = function(e) {
            document.getElementById("file-header-1").textContent = "Report file : " + file.name;
            document.getElementById("output-1").textContent = e.target.result; // Display file content
            document.getElementById("report-file-view").style.display = "block";
        };

        reader.onerror = function() {
            console.error("Error reading file!");
        };

        reader.readAsText(file); // Read file as text
    }
});



// for displaying trace file after loading a file.
document.getElementById("traceFiles").addEventListener("change", function(event) {
    const file = event.target.files[0]; // Get the selected file

    if (file) {
        const reader = new FileReader();

        // Define what happens when reading is complete
        reader.onload = function(e) {
            const fileContent = e.target.result; // File content as text
            const lines = fileContent.split("\n"); // Split the content by line
            // Get the first 10 lines
            const first10Lines = lines.slice(0, 10).join("\n");

            let file = event.target.files[0];
            document.getElementById("file-header-2").textContent = "Trace file (first 10 lines) : " + file.name;
            document.getElementById("output-2").textContent = first10Lines; // Display file content
            document.getElementById("trace-file-view").style.display = "block";
        };

        reader.onerror = function() {
            console.error("Error reading file!");
        };

        reader.readAsText(file); // Read file as text
    }
});
