Build the docker:<br />
docker build -t fetch_backend .<br />
Run Docker Container:<br />
docker run -d -p 8000:80 fetch_backend<br />
Test the API url on localhost:<br />
http://127.0.0.1:8000
