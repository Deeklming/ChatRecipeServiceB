from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import LoadSettings

config = LoadSettings().get_config()

SQLALCHEMY_DATABASE_URL = \
    f"mariadb://{config.MARIADB_USER}:{config.MARIADB_PASSWORD}@{config.MARIADB_HOST}/{config.MARIADB_DATABASE}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

if engine.connect():
    print("데이터베이스 연결 성공")
else:
    print("데이터베이스 연결 실패")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
