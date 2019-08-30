# django-html-parser-sibdev
This application will parse some html parameters
Tested on Python 3.7.4

1. Local Install

git clone https://github.com/OffyGhost/django-html-parser-sibdev
cd django-html-parser-sibdev
python -m venv env
env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate

# [Create admin]
python manage.py createsuperuser

2. Django Web Server & URL Parser

python manage.py run_parser --port 80
# In fact its run 'python manage.py runserver 0.0.0.0:PORT --insecure') and parser in multithread