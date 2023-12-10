from dataclasses import dataclass
from typing import List, Any

from environs import Env

#Imports from google-id
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    user_redis: bool

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str

@dataclass
class Miscellaneous:
    scoped_credentials: Any = None

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous

def get_scoped_credentials(credentials, scopes):
    def prepare_credentials():
        return credentials.with_scopes(scopes)
    return prepare_credentials

def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    google_credentials = Credentials.from_service_account_file('tg_bot/vova.json')
    scoped_credentials = get_scoped_credentials(google_credentials, scopes)

    return Config(
        tg_bot=TgBot(
            token= env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            user_redis=env.bool("USE_REDIS")
        ),
        db = DbConfig(
            host=env.str("DB_HOST"),
            password=env.str("DB_PASS"),
            user=env.str("DB_USER"),
            database= env.str("DB_NAME")
        ),
        misc=Miscellaneous(
            scoped_credentials=scoped_credentials
        )
    )

banned_user = [1234567, 23456789]