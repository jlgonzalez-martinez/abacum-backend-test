# abacum-backend-test

## Installation:

1.- Local:
- [Install poetry](https://python-poetry.org/docs/)
- Run ```poetry install``` to create the python environment.
- Run ```tox -p``` to: Format code with black, Flake8 linting, Unit tests, Integration tests, and Create the helm chart.
- Run ```docker-compose -f .deployment/docker-compose.yml up -d postgres``` to deploy the postgres database.
- Run ```poetry run uvicorn transactions.entrypoints.fastapi_application:app --port 8000```to deploy the application.

2.- Docker-compose:
- Run ```docker-compose -f .deployment/docker-compose.yml build````
- Run ```docker-compose -f .deployment/docker-compose.yml up -d```

3.- Kubernetes & Helm:
- Run ```docker build -t abacum-api .``` to build the docker image of the api.
- After configuring kubernetes with docker-desktop you can run  ```helm install bgapp -f values/00-local-values.yaml bgapp-0.1.0.tgz```

