import os

import requests


def test(api_key: str, uid: str):
    # Define the URL and headers
    url = f"http://localhost/status/{uid}"
    headers = {
        "Content-Type": "application/json",  # Example header
        "Authorization": f"Bearer {api_key}"   # Example header
    }

    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("GET request successful!")
        print("Response JSON:")
        print(response.json())
    else:
        print("GET request failed with status code:", response.status_code)


if __name__ == "__main__":
    api_key = os.environ["API_KEY"]
    uid = os.environ["ORDER_UID"]
    test(api_key=api_key, uid=uid)
