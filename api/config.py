from pydantic import BaseSettings


class SettingsEnv(BaseSettings):
    class Config:
        env_file = ".env"


class ApiSettings(SettingsEnv):
    env: str
    ap_host: str
    ap_port: int


class DBSettings(SettingsEnv):
    db_user: str
    db_pass: str
    db_host: str
    db_test_host: str
    db_port: int
    db_database: str


class AuthSettings(SettingsEnv):
    auth_algo: str
    auth_secret: str
    auth_token_expire_days: int
