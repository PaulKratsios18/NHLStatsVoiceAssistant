import requests
import json

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        print(response.text)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        data = json.loads(response.text)
        return data['Players']