from dataclasses import field, dataclass

from environs import Env


@dataclass
class SQLConfig:
    TYPE: str
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    DRIVER: str
    ECHO: bool
    POOL_SIZE: int = field(default=8)

    @property
    def url(self) -> str:
        if self.NAME:
            return f"{self.TYPE}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
        return f"{self.TYPE}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}"

    @property
    def url_with_driver(self) -> str:
        return f"{self.TYPE}+{self.DRIVER}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"


def get_sql_config(env: Env) -> SQLConfig:
    return SQLConfig(
        TYPE=env.str("TYPE"),
        HOST=env.str("HOST"),
        PORT=env.int("PORT"),
        USER=env.str("USER"),
        PASS=env.str("PASS"),
        NAME=env.str("NAME"),
        DRIVER=env.str("DRIVER"),
        ECHO=env.bool("ECHO"),
        POOL_SIZE=env.int("POOL_SIZE"),
    )
