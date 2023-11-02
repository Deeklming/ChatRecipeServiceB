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
    MYSQL_HOST: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

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

class LoadSettings:
    def __init__(self):
        self.mode = os.getenv("YXSMODE", "dev")

    def __call__(self):
        if self.mode == 'dev':
            return SettingsDev()
        elif self.mode == 'prod':
            return SettingsProd()


### db
