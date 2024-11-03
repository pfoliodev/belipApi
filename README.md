# belipApi
Yutopia project for Belib API - Data course

## Installation
In order to run the project, you need to install Python 3.9 and pip.
You need a database to run the project. I used MySQL.
You need to install mysql-connector-python and requests modules.
You can look at the requirement.txt file to see the dependencies.

I used a virtual environment to run the project.
To create the virtual environment, run the following command:
```bash
python -m venv venv
```

I used an venv, all the dependencies are installed in the venv folder. 
To activate the venv, run the following command:
```bash
source venv/bin/activate
```

## Running the project
To insert data into the database, you can run the insertData.py script.
To run the project, you need to run the main.py script.

## API
For the api I used FastAPI and Jinja2 for templating.
To look at the API, you can run the following command:
```bash
uvicorn routes.stations:app --reload
```

You can also run the main.py script to run the project.