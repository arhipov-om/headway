from dataclasses import field, dataclass

from environs import Env


@dataclass
class SQLConfig:
    DB_TYPE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER: str
    DB_ECHO: bool
    DB_POOL_SIZE: int = field(default=8)

    @property
    def url(self) -> str:
        if self.DB_NAME:
            return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}"

    @property
    def url_with_driver(self) -> str:
        return f"{self.DB_TYPE}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


def get_sql_config(env: Env) -> SQLConfig:
    return SQLConfig(
        DB_TYPE=env.str("DB_TYPE"),
        DB_HOST=env.str("DB_HOST"),
        DB_PORT=env.int("DB_PORT"),
        DB_USER=env.str("DB_USER"),
        DB_PASS=env.str("DB_PASS"),
        DB_NAME=env.str("DB_NAME"),
        DB_DRIVER=env.str("DB_DRIVER"),
        DB_ECHO=env.bool("DB_ECHO"),
        DB_POOL_SIZE=env.int("DB_POOL_SIZE"),
    )
