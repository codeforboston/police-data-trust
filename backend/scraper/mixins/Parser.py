from bs4 import BeautifulSoup, Tag
from typing import Union
import logging


class ParserMixin:
    """
    A mixin class for parsing HTML using BeautifulSoup.

    Args:
        logger (Union[logging.Logger, None], optional): The logger instance to
        use for logging. Defaults to None.

    Attributes:
        logger (logging.Logger): The logger instance used for logging.

    Methods:
        _find_and_extract: Finds and extracts text from an HTML element.

    """

    def __init__(self, logger: Union[logging.Logger, None] = None):
        self.logger = logger or logging.getLogger(__name__)

    def _find_and_extract(
        self,
        soup: Union[BeautifulSoup, Tag],
        tag: str,
        class_: str,
        error_message: str,
        replace_text: Union[str, None] = None,
    ) -> Union[str, None]:
        """
        Finds and extracts text from an HTML element.

        Args:
            soup (Union[BeautifulSoup, Tag]): The BeautifulSoup object or Tag to
            search within.
            tag (str): The HTML tag to search for.
            class_ (str): The CSS class of the HTML element to search for.
            error_message (str): The error message to log if the element is not
            found.
            replace_text (Union[str, None], optional): The text to replace
            in the extracted text. Defaults to None.

        Returns:
            Union[str, None]: The extracted text, or None if the element is
            not found.

        """
        element = soup.find(tag, class_=class_)
        if not element:
            self.logger.warning(error_message)
            return None
        text = element.text
        if replace_text:
            text = text.replace(replace_text, "")
        return text
