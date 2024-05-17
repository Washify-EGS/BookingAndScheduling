# Booking and scheduling

### API Structure
```
.
└── booking_api 
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    └── models.py
``` 

## Create database

Pull MySQL image from Docker Hub with:
```bash
docker pull mysql:latest
```

Create the container:

- linux: 
```bash
docker run --name bookings -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
```
- windows/mac:
```bash
docker run -p 3307:3306 --name bookings -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
```


Check if the MySQL server is ready for connections (might have to wait 1-2 minutes):
```bash
docker logs bookings
```

Get the container host ip address with:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bookings 
```


Edit the file 'dbconfig.ini' (If on windows/mac use the first port used on the docker run command and change the host to your local host ip address, which is probably 127.0.0.1):
```bash
[database]
host = 10.139.0.2
database_name = bookings
password = password
port = 3306
```

## Run the app



To build the Docker image, navigate to the directory containing the Dockerfile and run:

```bash
docker build -t booking-api .
```

Once the image is built, you can run it as a container using:

```bash
docker run -d --name booking-api-container -p 8000:8000 booking-api
```
