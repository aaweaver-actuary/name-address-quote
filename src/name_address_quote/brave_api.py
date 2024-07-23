import requests
from dotenv import load_dotenv, find_dotenv
import os
from dataclasses import dataclass
import json

load_dotenv(find_dotenv())

BRAVE_API_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"


@dataclass
class BraveRequest:
    """A class to represent a Brave API request."""

    _api_stem: str = BRAVE_API_ENDPOINT
    _timeout: int = 5

    @property
    def timeout(self) -> int:
        """Get the timeout for the Brave API request."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        """Set the timeout for the Brave API request."""
        self._timeout = value if value > 0 else 5

    @property
    def headers(self) -> dict:
        """Get the headers for the Brave API request."""
        brave_api_key = os.getenv("BRAVE_SEARCH_API_KEY")

        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": brave_api_key,
        }

    def url(self, query: str) -> str:
        """Get the URL for the Brave API request."""
        return f"{self._api_stem}?q={query.replace(' ', '+')}"

    def request(self, query: str) -> requests.Response:
        """Search the Brave API for the given query."""
        return requests.get(self.url(query), headers=self.headers, timeout=self.timeout)

    def request_json(self, query: str) -> dict:
        """Search the Brave API for the given query and return the JSON response."""
        return json.loads(self.request(query).content.decode("utf-8"))


@dataclass
class BraveResult:
    """A class to represent a Brave API result."""

    request: BraveRequest
    query: str

    def __post_init__(self):
        """Initialize the BraveResult object."""
        self._response = self.request.request_json(self.query)

    @property
    def response(self) -> dict:
        """Get the response from the Brave API."""
        return self._response

    @property
    def results(self) -> list:
        """Get the results from the Brave API response."""
        return self.response.get("web", {}).get("results", [])

    def top(self, n: int = 3) -> list:
        """Get the top n results from the Brave API response."""
        return self.results[:n]
