from re import search
import requests
from dotenv import load_dotenv, find_dotenv
import os
from sys import argv

load_dotenv(find_dotenv())


def main():
    if len(argv) < 2:
        print("Usage: python test.py <search_query>")
        return

    search_query = argv[1]

    brave_api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    BRAVE_API_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
    BRAVE_SEARCH_URL = f"{BRAVE_API_ENDPOINT}?q={search_query.replace(' ', '+')}"

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_api_key,
    }

    response = requests.get(BRAVE_SEARCH_URL, headers=headers)

    print(type(response.content))
    print(response.content.decode("utf-8"))
    # response_json = response.json()
    # for result in response_json["results"]:
    #     print(f"Title: {result['title']}")
    #     print(f"URL: {result['url']}")
    #     print(f"Snippet: {result['snippet']}")
    #     print("\n")


if __name__ == "__main__":
    main()
