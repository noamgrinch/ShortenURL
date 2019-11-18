# ShortenURL
 A web application/service that shortens URL.

### General
This application gets a URL in a POST request and generates a new URL(used for long URL inputs).
It stores the relevant data in the DB:
1. Table "URLs" -> contatins data regarding the generated URLs.
2. Table "Redirections" -> used to gather statistics.
3. Table "Bad Requests" -> for storing data regarding the errors in the server.

To view the statistics add "/stats" to the URL.
