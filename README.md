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

To run create/reset the database and its data, run the following command:

```bash
python3 database.py
```

### Run the Application

In order to run the application, run the following command:

```bash
uvicorn main:app --reload
```

