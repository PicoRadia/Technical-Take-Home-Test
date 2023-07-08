import requests

class UtilityRateFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://developer.nrel.gov/api/utility_rates/v3"

    def get_utility_rate(self, address):
        params = {
            "api_key": self.api_key,
            "address": address,
            "format": "json"
        }

        try:
            response = requests.get(self.base_url, params=params)
            print('hola')
            data = response.json()

            if "outputs" in data and "residential" in data["outputs"]:
                return data["outputs"]["residential"]
            else:
                return "Utility rate not found"

        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            return "Error occurred during API request"
