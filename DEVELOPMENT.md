# Working with docker-compose

Inside trashradar-api folder `docker-compose up` will launch the configuration in docker-compose.yml, which provides redis 
and postgres allowing you to run django on your localhost. Use this when working on the backend.

You should generally use `up` and `stop` for day to day development. This is the least overhead approach to starting and
stopping the environment.

The data volume for postgres is persistent. You will need to remove the volume running `docker volume rm` if you want to 
initiate a completely new database.

## Standalone

To run a standalone project you can use inside trashradar-api folder:
 
        docker-compose -f docker-compose.yml up

If you need to run any command, you can use:

        docker exec -ti trashradarapi_django_1 /code/manage.py createsuperuser
