from dataclasses import dataclass

from environs import Env

from headway.infrastructure.database.sql.config import SQLConfig


@dataclass
class Config:
    db: SQLConfig


def get_config(db: SQLConfig) -> Config:
    return Config(
        db=db
    )
