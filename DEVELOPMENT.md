# Working with docker-compose

`docker-compose up` will launch the configuration in docker-compose.yml, which provides redis and postgres allowing you
to run django on your localhost. Use this when working on the backend.

You should generally use `up` and `stop` for day to day development. This is the least overhead approach to starting and
stopping the environment.

The data volume for postgres is persistent. You will need to remove the volume use `docker volume rm` if you want to 
initiate a completely new database.