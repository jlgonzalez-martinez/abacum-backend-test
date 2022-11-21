# abacum-backend-test

## Run modes:
1.- PostgreSQL:
- Stores the data in a transactions table in PostgreSQL.
- To set it it's neccesary to change the backend config to ```sqlalchemy```.

2.- Pandas:
- Stores the data in a transactions pandas dataframe to use pandas like the test suggests (Like we are persisting it in the filesystem it will have concurrency problems).
- To set it it's neccesary to change the backend config to ```pandas```.

## Installation:

1.- Local:
- [Install poetry](https://python-poetry.org/docs/)
- Run ```poetry install``` to create the python environment.
- Run ```tox -p``` to: Format code with black, Flake8 linting, Unit tests, Integration tests, and Create the helm chart.
- Run ```docker-compose -f .deployment/docker-compose.yml up -d postgres``` to deploy the postgres database.
- Run ```poetry run uvicorn transactions.entrypoints.fastapi_application:app --port 8000```to deploy the application.
- Now you can access to the openapi in http://localhost:8000/docs
- Also, you can load the csv with the command ```poetry run python entrypoins/cli_application.py sample-data.csv``` 
2.- Docker-compose:
- Run ```docker-compose -f .deployment/docker-compose.yml build````
- Run ```docker-compose -f .deployment/docker-compose.yml up -d```
- Now you can access to the openapi in http://localhost:8000/docs
- Also, you can load the csv with the command ```docker-compose -f .deployment/docker-compose.yml run --rm api python transactions/entrypoints/cli_application.py sample-data.csv``` 


3.- Kubernetes & Helm:
- Run ```docker build -t abacum-api .``` to build the docker image of the api.
- After configuring kubernetes with docker-desktop you can run  ```helm install abacum -f .deployment/helm/values/00-local-sqlalchemy-values.yaml abacum-0.1.0.tgz``. Also, there is another values file for ```.deployment/helm/values/00-local-pandas-values.yaml``` for pandas repository.
- Now you can access to the openapi in http://localhost/docs

