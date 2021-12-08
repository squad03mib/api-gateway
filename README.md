[![squad03mib](https://circleci.com/gh/squad03mib/api-gateway.svg?style=svg)](https://app.circleci.com/pipelines/github/squad03mib/api-gateway)
[![codecov](https://codecov.io/gh/squad03mib/api-gateway/branch/main/graph/badge.svg?token=9PCM5V8D0E)](https://codecov.io/gh/squad03mib/api-gateway)
# Message In a Bottle - API Gateway

This is the source code of Message in a Bottle API Gateway, self project of _Advanced Software Engineering_ course, University of Pisa.

## Team info

- The *squad id* is **Squad 3**.
- *Team leader* is [Antonio Pace](https://github.com/pacant) and the other members are [Giulio Piva](https://github.com/gystemd), [Alessandro Cecchi](https://github.com/PaolinoRossi) and [Francesco Carli](https://github.com/fcarli3).

#### Members

| Name and Surname      | Email                           |
| ----------------      | ------------------------------- |
|   Antonio Pace        |   a.pace10@studenti.uipi.it     |
|   Giulio Piva         |   g.piva2@studenti.unipi.it     |
|   Alessandro Cecchi   |   a.cecchi8@studenti.unipi.it   |
|   Francesco Carli     |   f.carli8@studenti.unipi.it    |
|                       |                                 |

## Instructions

### Initialisation

To setup the project initially you have to run these commands inside the project's root.

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.dev.txt`

### Run the project

To run the project you have to setup the flask environment, you can do it by executing the following command:

`export FLASK_ENV=<environment-name>`

and now you can run the application

`flask run`

**WARNING**: the static contents are inside the directory nginx/static, so if you want to run application without nginx you have to copy the static directory inside mib folder.

#### Application Environments

The available environments are:

-   debug
-   development
-   testing
-   production

If you want to run the application you have to startup the redis instance, using the command:

cp env_file_example env_file
export FLASK_ENV=development
flask run

#### Python dotenv

Each time you start a new terminal session, you have to set up all the environment variables that projects requires. When the variables number increases, the procedures needed to run the project becomes uncomfortable.

To solve this problem we have introduced the python-dotenv dependency, but only for development purposes. You can create a file called `.env` that will be interpreted each time that you run the python project. Inside `.env` file you can store all variables that project requires. The `.env` file **MUST NOT** be added to repository and must kept local. 

### Dependencies splitting

Each environment requires its dependency. For example `production` env does not require the testing frameworks. Also to keep the docker image clean and thin we have to split the requirements in multiple files:

-   `requirements.txt` is the base file.
-   `requirements.dev.txt` extends base file and it contains all development requirements.
-   `requirements.prod.txt` extends base file and it contains the production requirements, for example gunicorn and psycopg2.

**IMPORTANT:** the Docker image uses only the production requirements.

### Run tests

To run all the tests, execute the following command:

`python -m pytest`

You can also specify one or more specific test files, in order to run only those specific tests. In case you also want to see the overall coverage of the tests, execute the following command:

`python -m pytest --cov=mib`

In order to know what are the lines of codes which are not covered by the tests, execute the command:

`python -m pytest --cov-report term-missing`

You can also run tests execute the command `tox` from the root project folder.

### Nginx and Gunicorn

Nginx will serve static contents directly and will use gunicorn to serve app pages from flask wsgi. You can start gunicorn locally with the command

`gunicorn --config gunicorn.conf.py wsgi:app`

**WARNING** gunicorn it's not able to read the .env files, so you have to export the variable, for example by issuing the command `source .env`.

### Docker image

This project has the possibility to be built as docker image. To build the image you can launch the command

`docker build . -t gotf`

###  docker-compose

If you want to run the entire project using separate containers and using the production environment you have to:

-   Check configuration file, that is named `env_file`. It contains the project variables.
    
-   Run the command `docker-compose up -d`
    
-   Now you should see all services running and the application frontend available at 127.0.0.1:5000


### Nginx orchestrator

We have created a specific documentation file for [nginx-orchestrator](https://github.com/federicosilvestri/mib-api-gateway/blob/958071829c8cd18a0421d508f5672b9ce1736b7a/nginx-orchestrator/README.md)