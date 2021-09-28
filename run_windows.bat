python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -r requirements/dev_windows.txt

set FLASK_ENV=development

flask psql create
flask psql init

flask run
