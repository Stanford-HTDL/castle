__author__ = "Richard Correro (richard@richardcorrero.com)"

import json
from typing import List


def get_api_keys(api_keys_path: str) -> List[str]:
    # Open the .json file in read mode
    with open(api_keys_path, 'r') as file:
        # Load the JSON data from the file into a Python dictionary
        keys_dict: dict = json.load(file)
    return list(keys_dict.values())


# def validate_api_key(api_key: str, valid_api_keys: List[str]) -> str:
#     # Check if API key is provided
#     if api_key is None:
#         raise HTTPException(status_code=401, detail="API key required")

#     # Validate API key against allowed keys
#     if api_key not in valid_api_keys:
#         raise HTTPException(status_code=403, detail="Invalid API key")

#     # Return the validated API key
#     return api_key
