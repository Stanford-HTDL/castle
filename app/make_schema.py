__author__ = "Richard Correro (richard@richardcorrero.com)"

import json

from fastapi.openapi.utils import get_openapi

from castle.main import app

if __name__ == "__main__":
    with open('openapi.json', 'w') as f:
        json.dump(get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        ), f)
