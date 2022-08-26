import requests


class Counted_Client:
    def run(self):
        url = (
            "https://interactive.guim.co.uk/2015/"
            + "the-counted/thecounted-data.zip"
        )
        r = requests.get(url)
        return r
