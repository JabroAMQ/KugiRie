import time

import requests
from requests.exceptions import RequestException

class Query:
    def __init__(self):
        self._URL = 'https://graphql.anilist.co'
        self._session = requests.Session()
        self._retries_times = 3
        self._retry_after = 5

    def execute(self, query: str, variables: dict) -> dict:
        """
        Execute a GraphQL query against the Anilist API.
        This is a placeholder function; you should implement the actual API call.
        """
        for attemp_number in range(self._retries_times):
            try:
                response = self._session.post(self._URL, json={'query': query, 'variables': variables})
                response.raise_for_status()
                data = response.json()['data']
                return data

            except RequestException as e:
                # If we got a 404 error, we raise a ValueError with a specific message
                if response is not None and response.status_code == 404:
                    raise ValueError(f'Not Found Error: {e}')
            
                # If we are in the last loop iteration and we couldn't retrieved the data, we raise the error
                if attemp_number == self._retries_times - 1:
                    raise e

                # Wait for the Retry-After time if the status code is 429 (timed out)
                if response is not None and response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    time.sleep(retry_after)
                # Otherwise, we got an unknown error: print the error message and wait some default seconds...
                else:
                    #print(f'Error: {e}\nWaiting for {self._retry_after} seconds (default)...')
                    time.sleep(self._retry_after)
                continue