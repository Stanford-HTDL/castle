import os

import requests


def test(url: str, api_key: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Define the data to be sent in the request body
    data = {
        "start": "string",
        "stop": "string",
        "id": "string",
    }

    # Send the POST request with headers and data
    response = requests.post(url, headers=headers, json=data)

    # Check the response status code
    if response.status_code == 200:
        print("POST request successful!")
        print("Response JSON:")
        print(response.json())
    else:
        print("POST request failed with status code:", response.status_code)


if __name__ == "__main__":
    url: str = os.environ["URL"]
    api_key = os.environ["API_KEY"]
    test(url=url, api_key=api_key)
