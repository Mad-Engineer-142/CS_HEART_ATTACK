import os
import requests
from dotenv import load_dotenv
from exceptions import RequireParamsException
from service import BaseService

load_dotenv()


class GitHub(BaseService):
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {os.getenv('GITHUB_KEY')}"
        }

    def search(self, query):
        if not query:
            raise RequireParamsException()

        response = requests.get("https://api.github.com/search/code",
                                params={"q": query},
                                headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return [item["url"] for item in data["items"]]
        else:
            return {"error": response.json()}