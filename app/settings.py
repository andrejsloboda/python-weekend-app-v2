from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_user: str
    db_password: str
    db_port: int
    db_database: str
    redis_key_prefix: str
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int
    redis_decode_responses: bool
    currency_rate_url: str
    regiojet_base_url: str
    regiojet_location_url: str
    flixbus_base_url: str
    flixbus_location_url: str


    class Config:
        env_file = './.env'


settings = Settings()


