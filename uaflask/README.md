# uaflask

## 설치
```bash
pip install flask flask-sqlalchemy flask-migrate flask-login flask-wtf python-dotenv email-validator
```

## 인증서 만들기
```bash
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -keyout certs/key.pem -out certs/cert.pem
```

## 실행
```bash
python uaflask.py
```
