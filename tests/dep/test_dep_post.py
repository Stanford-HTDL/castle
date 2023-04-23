import os

import requests


def test(base_url: str, api_key: str):
    url = f"{base_url}/process"
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
        print(response)


if __name__ == "__main__":
    base_url: str = os.environ["BASE_URL"]
    api_key = os.environ["API_KEY"]
    test(base_url=base_url, api_key=api_key)
