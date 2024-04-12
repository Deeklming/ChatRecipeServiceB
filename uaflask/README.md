# uaflask

## 설치
```bash
pip install flask flask-sqlalchemy flask-migrate python-dotenv email-validator "psycopg[binary,pool]" "redis[hiredis]"
```

## 인증서 만들기
```bash
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -keyout certs/key.pem -out certs/cert.pem
ssh-keygen -t ed25519 -C "name@name.com"
```

## 실행
```bash
python uaflask.py
```
`flask shell` : 현재 플라스크 환경을 가져와 파이썬 쉘을 실행  
`flask db init` : db 초기 구성  
`flask db migrate -m "tagname"` : Model 변경사항을 적용  
`flask db upgrade` : migrate 한 것을 DBMS에 적용  
`flask db downgrade` : 이전 migrate로 복귀

## RDB 명령어
```bash
psql -U postgres #접속
```
`\l` : 데이터베이스 목록
`\d` : 테이블 확인
`\c` : 데이터베이스 선택
