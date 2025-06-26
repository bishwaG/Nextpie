
## Nextpie API

Nextpie’s API will be accessible at [http://127.0.0.1:5000/api/v1.0](http://127.0.0.1:5000/api/v1.0) if the application is running locally on that address and port. If you are running Nextpie on a different host or port, the API endpoint will be available at
```
http://<host-or-ip>:<port>/api/v1.0
```
This endpoint includes a [Swagger-based API interface](https://swagger.io/), which allows you to explore and test the available API methods directly through your browser.

By default, Nextpie provides an API key for the admin user stored in its SQLite database:
```
jWCr-uqJB9fO9s1Lj2QiydXs4fFY2M
```
To try out the API:

1. Open the Swagger interface in your browser.
2. Click the "Authorize" button.
3. Paste the API key when prompted.
4. For example, you can call the /get-groups endpoint to retrieve a list of all research groups stored in Nextpie.

> Note: Replace <host-or-ip>:<port> with the actual IP address or domain and the port number where your Nextpie instance is running.
