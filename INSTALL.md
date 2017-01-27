# Installation Instructions for linux/macOS

```
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.pip
```

## Test

### Configure the environment

Set the environment variables in `trashradar-api/trashradar/.env`.

### Run the tests

        cd trashradar-api
        py.test --ds=trashradar.settings -x accounts/tests.py  
