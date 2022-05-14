# Autocomplete  / Search Service

# Using docker

## Prerequisites
To setup your local environment, you need install Docker Engine and docker-compose. You can follow the instructions [here](#How-to-install-Docker) to install.

### How to install Docker

Docker Engine is available on a variety of [MacOS](https://docs.docker.com/docker-for-mac/install/)

### How to install docker-compose

Docker compose is available on [MacOs](https://docs.docker.com/compose/install/)


### Running services

If you have already set up your local environment and have a **.env** file with the development variables set, this command builds the image *autocomplete* if not exists and starts *autocomplete* and *db* services:

```shell
$ docker-compose up -d
```
Load the URL http://localhost:8000/ into your browser.

**Note**: The network *internal* so that the containers can be seen


## How to rebuild the docker image

In case you want the changes you have been testing to remain permanently in a new docker image you can rebuild the image, run this command:

```shell
$ docker-compose build
$ docker-compose up -d
```

After the build, you can remove the previous image with:

```shell
$ docker image prune -f
```

## Container shell access 

The docker exec command allows you to run commands inside a Docker container. The following command line will give you a bash shell inside your containers: `docker exec -it <container_name> <command>`

#### Example
```shell
$ docker exec -it autocomplete /bin/bash
```


## Running test
```shell
$ docker exec -it autocomplete test
```


# Using Conda
```shell
conda env create -f environment.yml
```

# Using VirtualEnv
create [virtual enviroment](https://help.dreamhost.com/hc/es/articles/115000695551-Instalar-y-usar-virtualenv-con-Python-3)

install dependencies 
```shell
pip install -r requirements.txt
```

# For conda and virtualEnv is also required install PostgreSQL 
[Download](https://www.postgresql.org/download/) and install postgress

setup and create database and change the database URL on the .env file

## Migrate database
```shell
python manage.py migrate
```

## Run services
```shell
python manage.py runserver
```


# Relevant Files

## Search engine

search_app.services.autocomplete_engine.ScoreService


In The search engine its possible change precision of the location score changing env 
DISTANCE_NORMALIZING_SIZE

Increasing this value will decrease the precision  of location based score, increasing its final score.

min value 1 
## Filters 

search_app.api.drf.filters.CustomSearchFilter