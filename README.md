# YourAccommodation

```
YourAccommodation 은 숙박 예약 프로젝트입니다
```

<br>

## 개발 기간
```
2024.03 ~ 
```

<br>

## View

<br>

## [목차]
1. [링크](#1-링크)
2. [개발 환경](#2-개발-환경)
3. [기능](#3-기능)
4. [프로젝트 설계](#4-프로젝트-설계)

<br>

## 1. 링크

<!-- - [1](https://www.notion.so/) -->

<br>

## 2. 개발 환경 및 세팅
```
각각의 프레임워크로 같은 기능을 개발합니다
```

### 2-1. Flask
```
alembic==1.13.1
async-timeout==4.0.3
blinker==1.7.0
click==8.1.7
colorama==0.4.6
dnspython==2.5.0
email-validator==2.1.0.post1
Flask==3.0.2
Flask-Migrate==4.0.5
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
greenlet==3.0.3
hiredis==2.3.2
idna==3.6
itsdangerous==2.1.2
Jinja2==3.1.3
Mako==1.3.2
MarkupSafe==2.1.5
psycopg==3.1.18
psycopg-binary==3.1.18
psycopg-pool==3.2.1
python-dotenv==1.0.1
redis==5.0.2
SQLAlchemy==2.0.26
typing_extensions==4.9.0
tzdata==2024.1
Werkzeug==3.0.1
WTForms==3.1.2
```

### 2-2. Django
- Django

### 2-3. FastAPI
- FastAPI

### 2-4. Next.js
- Next.js

### 2-5. Docker
```bash
# 커스텀 네트워크 미리 생성
docker network create --driver=bridge --subnet=172.55.0.0/24 --ip-range=172.55.0.0/24 --gateway=172.55.0.1 mynet

# 실행
docker-compose up -d

# 종료
docker-compose down
```
```
docker-compose.yml
```

- Redis
```
cachedb/
redis.conf
```

- PostgreSQL
```
rdb/
rdb.env
rdb_init.sql
```

### 2-6. common
- React
- TailwindCSS

<br>

## 3. 기능

- 회원가입
- 로그인 / 로그아웃
- 프로필
- 검색
- 예약
- 채팅
- 게시판
- 게시글
- 언어
- 사이트 정보

<br>

## 4. 프로젝트 설계

### 4-1. ERD
```
ERD.txt
```
![YourAccommodation ERD](https://github.com/Deeklming/YourAccommodation/assets/71743128/d751ca01-1bce-403b-82b7-625228113d74)

### 4-2. Infra Architecture

<!-- ![YourAccommodation Infra]() -->

### 4-3. 기능 상세
- 로그인
    - 회원가입
    - 로그인 / 로그아웃
- 프로필
    - 유저
        - 개인코드, 클립, 좋아요, 댓글, 팔로잉 목록
    - 사업자
        - 숙박 등록 리스트
- 유저
    - 유저 및 프로필 업데이트
- 채팅
    - 유저
        - 소모임 숙박 예약 채팅
    - 사업자
        - 협업 채팅
- 숙박
    - 검색
    - 게시판
        - 숙박게시글, 평점
    - 예약
        - 체크인 / 체크아웃, 지역, 최종가격
- 언어
    - 한국어, 영어
- 푸터
    - 사이트 정보

<br>

## 개발자

- Deeklming

<br>
