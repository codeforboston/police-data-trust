import requests


class FF_Client:
    def run(self):
        url = "https://github.com/washingtonpost/\
            data-police-shootings/releases/download/\
                v0.1/fatal-police-shootings-data.csv"
        r = requests.get(url)
        return r
