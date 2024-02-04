# Web Scraping Project
This folder contains a collection of web scrapers for various data sources.

## Project Structure
The main component of the project is the website folder. Each folder contains a source for the scraper.

Here's a brief overview of the files in the current folder:

_mixins_ - a few helpful classes to get you started. As more scrapers are developed these should be more general purpose  
_data_scrapers_ - an old folder that is no longer used  
_notebooks_ - an old folder that is no longer used.  
_websites_ - these folders contain subfolders about the scraper logic. Each folder includes a method that gathers data sequentially (nothing). They each use the scraper mixins to make essential get requests to the server, parse with Beautiful Soup, and return the officer and incident schema.

## Running the Scrapers
To run a scraper, run the flask command `scrape-v2`. You can use __-debug__ to enable debugging to scrape a small amount of each scraper quickly.

## Adding New Scrapers
To add a new scraper to the project, create a new Python file in the scraper folder. This file should define a class for the scraper with methods for retrieving and parsing the web page. See the existing scraper files for examples.

The scraper should return a list of officers and a list of incidents. (more schemas to come). For example:

```python
# read the data from NYPD and merge it with FiftyA
nypd = Nypd()
nypd_officer, nypd_incidents = nypd.extract_data(debug=debug)
```

Next, the script will check if the data is new and, if not, add it to the database.

## Future Improvements
This solution works for the small data we are currently scraping. In the future, different sites may have higher security and require a driver like Selenium, different headers, a reverse proxy, etc... As more and more sites are added, distributing the fetches to a task queue may limit the sequential bottleneck and scale better.


## Testing
The _tests_ directory contains all the testing for the scraper. So far, there are only unit tests; integration tests are to come.