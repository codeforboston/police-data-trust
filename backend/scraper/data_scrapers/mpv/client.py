import requests


class Mpv_Client:
    def run(self):
        dataset_url = (
            "https://docs.google.com/spreadsheets/d/"
            + "1g7CNEDnjk5dH412wmVTAG6XtgWyS2Vax10-BbfsBp0U/export?format=csv"
        )
        dataset_path = "backend/scraper/data_scrapers/scraper_data/mpv.csv"
        print("Downloading dataset")
        r = requests.get(dataset_url, stream=True)
        with open(dataset_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
