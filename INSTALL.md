# Installation steps for macOS

```
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.pip
```


### Run the tests
        
        py.test --ds=trashradar.settings -x accounts/tests.py  
