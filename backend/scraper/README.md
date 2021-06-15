The mapping_police_violence.py script should be able to run by itself, independent of the server and database.
The following are required and can be downloaded with pip install:

    * Python 3.8
    * Numpy
    * Pandas
    * openpyxl
    * xlsxwriter

To run, call the script from the head of the repository. You may see several warnings about mixed types. The script could also take several minutes.

If the script finishes successfully, there should be a full_database.xlsx file in the head of your repository. This should hold all the data that the scraper was able to get. There should be four tabs: report, incident, victim, and death
