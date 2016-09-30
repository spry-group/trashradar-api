# Installation steps for macOS

```
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.pip
```

# Run the API

```
    docker run --name trashradar-api-mongo -p 27017:27017 --rm mongo
    source venv/bin/activate
    python run.py
```