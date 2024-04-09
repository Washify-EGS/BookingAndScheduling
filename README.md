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



### Start Virtual Environment

In order to start the virtual environment, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
### Create database

Pull MySQL image from Docker Hub with:
```bash
$ docker pull mysql:latest
```

Create the container:
```bash
$ docker run --name bookings -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
```

Check if the container is running with:
```bash
$ docker ps 
```


To create/reset the database and its data, run the following command:

```bash
python3 database.py 
```

Host ip is optional, default is set to 172.17.0.2 

Check if it is using another ip address with: 

```bash
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bookings 
```




### Run the Application

In order to run the application, run the following command:

```bash
uvicorn main:app --reload
```

