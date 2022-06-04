import requests

class Counted_Client:
    def __init__(self, content):
        self.content = content

    def run(self):
        url = 'https://interactive.guim.co.uk/2015/the-counted/thecounted-data.zip'
        r = requests.get(url)
        return r