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
```bash
docker run --name bookings -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
```

Check if the container is running with:
```bash
docker ps 
```

Check if the MySQL server is ready for connections (might have to wait 1-2 minutes):
```bash
docker logs bookings
```

Get the container host ip address with:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bookings 
```

To create/reset the database and its data, run the following command:

```bash
python3 database.py 
```

## Run the app

### With Docker


To build the Docker image, navigate to the directory containing the Dockerfile and run:

```bash
docker build -t booking-api .
```

Once the image is built, you can run it as a container using:

```bash
docker run -d --name booking-api-container -p 8000:8000 booking-api
```


### Without Docker

#### Start Virtual Environment

In order to start the virtual environment, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

##### Run the Application

In order to run the application, run the following command:

```bash
uvicorn main:app --reload
```

