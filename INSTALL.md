# Installation Instructions for linux/macOS

```
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.pip
```

## On Mac

```
    brew install gdal
```

## On linux

```
    sudo apt-get install libgdal-dev
```

## Test

### Configure the environment

Set the environment variables in `trashradar-api/trashradar/.env`.

### Run the tests

        cd trashradar-api
        python manage test  
