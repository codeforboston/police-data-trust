import requests
import time
import logging
import re
from bs4 import BeautifulSoup
from typing import Any, Optional, List, AnyStr


class ScraperMixin:
    """
    A mixin class that provides scraping functionality.

    Attributes:
        headers_list (list): A list of headers to be used in requests.
        proxy_list (list): A list of proxies to be used in requests.
        rate_limit (int): The rate limit in seconds between consecutive
        requests.
        logger (logging.Logger): The logger object for logging errors and
        messages.
    """

    def __init__(self):
        self.headers_list = []
        self.proxy_list = []
        self.rate_limit = 5
        self.logger = logging.getLogger(__name__)

    def fetch(self, url: str, retries: int = 3) -> Optional[str]:
        """
        Fetches the content of a given URL.

        Args:
            url (str): The URL to fetch.
            retries (int, optional): The number of retries in case of failure.
            Defaults to 3.

        Returns:
            Optional[str]: The content of the URL as a string, or None if
            fetching failed.
        """
        for i in range(retries):
            try:
                # Randomize the headers to avoid getting blocked by the server
                response = requests.get(url)
                if response.status_code == 200:
                    return response.text
                else:
                    self.logger.error(
                        f"Error fetching {url}: {response.status_code}"
                    )
            # If there is an error, let's wait for a while before trying again
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if i < retries - 1:  # no need to wait on the last iteration
                    time.sleep(self.rate_limit)  # wait before retrying
        return None

    def find_urls(self, url: str, pattern: Any) -> List[AnyStr]:
        """
        Finds URLs matching a given pattern on a web page.

        Args:
            url (str): The URL of the web page to search.
            pattern (re.Pattern[Any]): The regular expression pattern to match.

        Returns:
            list[str]: A list of URLs matching the pattern.
        """
        response = self.fetch(url)
        if not response:
            self.logger.error(f"Could not fetch {url}")
            return []
        soup = BeautifulSoup(response, "html.parser")
        return [
            link["href"]
            for link in soup.find_all("a", href=pattern)
            if link["href"]
        ]
