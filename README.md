# Trashradar-api
The api to let your public servants and community know where there is cleaning to be done.

## Problem
Some public places are used as garbage storage and authorities wait too long to clean them

## Solution
Web/mobile application that help public servants and community to pinpoint trash places and direct authorities to these

## Features
- Save locations
- Upload pictures and link them to locations
- Send tweets to authorities

## First phase
- Build trashradar-api
- Create a simple web front-end application that help us to test and develop the API

## Second phase
- Build mobile application as API client for trashradar-api

## Development

Development on TrashRadar API should be done locally.

### Code Style

We use [PEP8](https://www.python.org/dev/peps/pep-0008/) with 119 as max line length.

        pep8 --max-line-length=119

For workflow we use forks, feature branches, and pull requests from forks.

### Workflow

1. Fork the [team repository](https://github.com/spry-group/trashradar-api)
2. Clone [your fork](https://github.com/{{your github username}}/trashradar-api)
3. Select or create an issue in the [Issue Queue](https://github.com/spry-group/trashradar-api/issues)
4. Create a branch for the issue prepended with the issue number and a short description using _ in place of spaces.
5. Commit changes to the branch.
6. Push branch to your fork.
7. When ready for review, submit pull request, begin the pull request with the issue number.

# Working with docker-compose

`docker-compose up` will launch the configuration in docker-compose.yml, which provides redis and postgres allowing you
to run django on your localhost. Use this when working on the backend.

You should generally use `up` and `stop` for day to day development. This is the least overhead approach to starting and
stopping the environment.

The data volume for postgres is persistent. You will need to remove the volume use `docker volume rm` if you want to 
initiate a completely new database.
