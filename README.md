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


First create a docker network:
```bash
docker network create bookings-network
```

Pull MySQL image from Docker Hub with:
```bash
docker pull mysql:latest
```

Create the container:

```bash
docker run --name bookings -e MYSQL_ROOT_PASSWORD=password --net bookings-network -d mysql:latest
```

Check if the MySQL server is ready for connections (might have to wait 1-2 minutes):
```bash
docker logs bookings
```

## Build and Run the api

To build the Docker image, navigate to the directory containing the Dockerfile and run:

```bash
docker build -t booking-api .
```

Once the image is built, you can run it as a container using:

```bash
docker run --name booking-api-container --net bookings-network -p 8000:8000 booking-api
```

