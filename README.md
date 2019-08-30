# django-html-parser-sibdev [test task]

This application will parse some html parameters<br>
Tested on Windows 32bit Python 3.7.4

1. Local Install

git clone https://github.com/OffyGhost/django-html-parser-sibdev<br>
cd django-html-parser-sibdev<br>
python -m venv env<br>
env\Scripts\activate<br>
python -m pip install --upgrade pip<br>
pip install -r requirements.txt<br>
python manage.py migrate<br>
python manage.py createsuperuser

2. Run app: Django Web Server & URL Parser

python manage.py run_parser --port 80

# In fact its run 'python manage.py runserver 0.0.0.0:PORT --insecure') and parser in multithread
