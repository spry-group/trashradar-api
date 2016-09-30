API_NAME = "trashradar"

CACHE_CONTROL = "max-age=20"
CACHE_EXPIRES = 20
MONGO_DBNAME = "trashradar"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
PUBLIC_ITEM_METHODS = ["GET"]
RESOURCE_METHODS = ["GET"]

accounts_schema = {
    "username": {
        "type": "string",
        "required": True,
        "unique": True
    },
    "password": {
        "type": "string",
        "required": True
    },
    "phone": {
        "type": "string",
        "required": True
    }
}

accounts = {
    "additional_lookup": {
        "url": "regex('[\w]+')",
        "field": "username",
    },
    "datasource": {
        "projection": {
            "password": 0,
            "salt": 0
        }
    },
    "cache_control": "",
    "cache_expires": 0,
    "schema": accounts_schema,
    "public_methods": ["POST", "GET"],
    "resource_methods": ["POST", "GET"]
}

DOMAIN = {
    "accounts": accounts,
    "events": {},
}
