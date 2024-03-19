# uadjango

## 설치
```bash
pip install django djangorestframework python-dotenv "psycopg[binary,pool]" "redis[hiredis]"
```

## 인증서 만들기
```bash
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -keyout certs/key.pem -out certs/cert.pem
```

## 실행
```bash
python manage.py runserver
```
