## Nextpie API

Nextpie's API end point is avaialable via URL `http://127.0.0.1:5000/api/v1.0` if Nextpie is running under `http://127.0.0.1:5000`. If you have run Nextpie in a different IP address and a port, the endpoint is available as `http://host-or-ip-address:port/api/v1.0`. The endpoint has Swagger API interface which can be used to test it.


### API call using Nextpie's API interface

Nextpie has Swagget API interface to the API entry point `http://host-or-ip-address:port/api/v1.0`. Nextpie has a default API key `jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M` for the `admin` user in it's SQLite database. To try out the API you should click "Authorize" button and provide the API key. As an example, you run "/get-groups" to get all the research groups from Nextpie.


### API call using curl

Following is an example of `GET` API call using `curl` in a Linux terminal.

```bash
curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1.0/get-groups' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M'
```

It above command will return the following output (stripped).

```
[
  {
    "id": 1, 
    "name": "research_group_A"
  }, 
  {
    "id": 3, 
    "name": "research_group_CD"
  }, 
.
.
.
.
]
```

Following is an example to perform `POST` API call using `curl`.

```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1.0/get-data-footprint-montly-TB?Year=2023' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M' \
  -d ''
```



### API call using Python
Following is an example for perform same API call using Python.

```python
import requests

## HTTP header with API key
my_headers = {'X-API-KEY' : 'jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M'}

## make the API call
response = requests.get("http://127.0.0.1:5000/api/v1.0/get-groups", headers=my_headers)

## print the response
print(response.json())
```


Following is an example to perform `POST` API call using Python.

```python
import requests

## HTTP header with API key
my_headers = {'X-API-KEY' : 'jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M'}

## make the API call
response = requests.post('http://127.0.0.1:5000/api/v1.0/get-data-footprint-montly-TB', data = {'Year':'2023'}, headers=my_headers)

## print the response
print(response.json())
```

### API call using Java

Create a file named `RestfulAPIClient.java` containing the following code.

```java
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class RestfulAPIClient {

    public static void main(String[] args) throws IOException {
        // API endpoint URL
        String endpointUrl = "http://127.0.0.1:5000/api/v1.0/get-data-footprint-montly-TB";
        
        // POST data
        String postData = "Year=2023";
        
        // API key
        String apiKey = "jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M";
        
        // Set up the HTTP connection
        URL url = new URL(endpointUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        
        // Set the request method to POST
        connection.setRequestMethod("POST");
        
        // Set the API key as an HTTP header
        connection.setRequestProperty("X-API-KEY", apiKey);
        
        // Enable output and input streams for POST data
        connection.setDoOutput(true);
        connection.setDoInput(true);
        
        // Write POST data to the connection
        try (DataOutputStream outputStream = new DataOutputStream(connection.getOutputStream())) {
            outputStream.writeBytes(postData);
            outputStream.flush();
        }
        
        // Read the response from the connection
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            // Print the response
            System.out.println("Response: " + response.toString());
        }
        
        // Close the connection
        connection.disconnect();
    }
}

```

Now, compile the Java code and execute it by running th following commands in a terminal.

```bash
## complie bytecode
javac RestfulAPIClient.java

## execute
java RestfulAPIClient
```

### API call using C

Create a file named `api.c` containing the following code.

```c
#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

int main(void) {
    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_ALL);
    
    // Create a new CURL handle
    curl = curl_easy_init();
    if (curl) {
        // Set the API endpoint URL
        curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:5000/api/v1.0/get-data-footprint-montly-TB");

        // Set the API key as an HTTP header
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "X-API-KEY: jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set the POST data
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "Year=2023");

        // Perform the request
        res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        // Clean up
        curl_easy_cleanup(curl);
        
        // Free the headers
        curl_slist_free_all(headers);
    }
    
    // Cleanup libcurl
    curl_global_cleanup();

    return 0;
}
```

Now, compile and run the C code.

```c
## compile the code
gcc -o api api.c -lcurl

## run the code
./api
```

