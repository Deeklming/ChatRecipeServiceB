# uadjango

## 설치
```bash
pip install django djangorestframework email-validator python-dotenv "psycopg[binary,pool]" "redis[hiredis]"
```

## 인증서 만들기
```bash
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -keyout certs/key.pem -out certs/cert.pem
```

## 실행
```bash
django-admin startproject <project name> .
python manage.py startapp <app name>
python manage.py makemigrations <app name>
python manage.py migrate
python manage.py runserver
```
