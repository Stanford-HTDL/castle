__author__ = "Richard Correro (richard@richardcorrero.com)"

import json

from fastapi.openapi.utils import get_openapi

from castle.api.main import fastapi_app

if __name__ == "__main__":
    with open('openapi.json', 'w') as f:
        json.dump(get_openapi(
            title=fastapi_app.title,
            version=fastapi_app.version,
            openapi_version=fastapi_app.openapi_version,
            description=fastapi_app.description,
            routes=fastapi_app.routes,
        ), f)
