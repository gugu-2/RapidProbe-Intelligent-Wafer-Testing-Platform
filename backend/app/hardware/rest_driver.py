import requests

class RESTInstrument:
    def __init__(self, base_url):
        self.base_url = base_url

    def run_test(self, params):
        response = requests.post(f"{self.base_url}/start_test", json=params)
        response.raise_for_status()
        return response.json()
