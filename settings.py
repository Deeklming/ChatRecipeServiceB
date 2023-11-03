from pydantic_settings import BaseSettings, SettingsConfigDict
import os

### env
class SettingsDev(BaseSettings):
    DEBUG: bool
    PORT: int
    HOST_IP: str
    SECRET_KEY: str
    FIREBASE_KEY_PATH: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str
    REDIS_ADDRESS: str
    REDIS_PORT: int
    MARIADB_HOST: str
    MARIADB_ROOT_PASSWORD: str
    MARIADB_PORT: int
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env.dev")

class SettingsProd(BaseSettings):
    DEBUG: bool
    PORT: int
    HOST_IP: str
    SECRET_KEY: str
    FIREBASE_KEY_PATH: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str
    REDIS_ADDRESS: str
    REDIS_PORT: int
    MYSQL_HOST: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env.prod")


class LoadSettings():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self._mode = os.getenv("YXSMODE", "dev")
            if self._mode == 'dev':
                self._config = SettingsDev()
            elif self._mode == 'prod':
                self._config = SettingsProd()
            cls._init = True

    def get_config(self):
        return self._config


### db
