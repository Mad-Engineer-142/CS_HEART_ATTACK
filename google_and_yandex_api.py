import requests
import xml.etree.ElementTree as ET
import os
from main import root
from github import GitHub
import requests
from dotenv import load_dotenv
from exceptions import RequireParamsException
from service import BaseService

load_dotenv()

def google_search(query, api_key="AIzaSyA9EP8V1Oha5iHKajZd5OqF5u1lOUFDfbE", cse_id="80e9187121ae74b37"):
    # URL for Google Custom Search JSON API
    url = "https://www.googleapis.com/customsearch/v1"

    # Parameters for the API request
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query
    }

    # Make the API request
    response = requests.get(url, params=params)
    response.raise_for_status()

    # Process and return the search results
    search_results = response.json()
    return search_results.get("items", [])

def yandex_search(query):
    # URL for Yandex.XML
    url = "https://yandex.com/search/xml"

    # Parameters for the API request
    params = {
        "user": "Иорин&l10n=ru",
        "key": "dn2tqbltrks2tdg1cl8i",
        "query": query,
        "l10n": "en",  # Localization
        "sortby": "rlv.order%253Ddescending" ,
        "filter":"strict",  # ,
        "groupby":"attr%253D.mode%253Dflat.groups-on-page%253D10.docs-in-group%253D1",
        "apikey":"AQVNyUOYNX0hm0N-uZo41y6iOod23JF35i9G812v",
        "folderid":"b1grca5sr0toqv32dnno"
        
        
    }

    # Make the API request
    response = requests.get(url, params=params)
    response.raise_for_status()

    # Parse XML response
    root = ET.fromstring(response.content)
    results = []
    for doc in root.findall(".//doc"):
        title = doc.find("title").text
        url = doc.find("url").text
        results.append({"title": title, "link": url})

    return results

def main():
    # Your unique HTML code or text
    print("Введите тест: ")
    unique_html_or_text = input()
    # Google API key and Custom Search Engine ID
    # google_api_key = "AIzaSyA9EP8V1Oha5iHKajZd5OqF5u1lOUFDfbE"
    # google_cse_id = "80e9187121ae74b37"

    # Yandex user and API ke
    git__api = GitHub()
    git_resoult = git__api.search(unique_html_or_text)
    # Perform the searches
    google_results = google_search(unique_html_or_text)
    yandex_results = yandex_search(unique_html_or_text)
    

    # Display the results
    print("Google Search Results:")
    for result in google_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print("")

    print("Yandex Search Results:")
    for result in yandex_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print("")
        
    print("Git Search Results:")
    for url in git_resoult:
        print(f"URL: {url}")
        print("")



'''

<script async src="https://cse.google.com/cse.js?cx=80e9187121ae74b37">
</script>
<div class="gcse-search"></div>

'''
if __name__ == "__main__":
    main()