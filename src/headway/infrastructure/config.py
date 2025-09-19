from dataclasses import dataclass
from pathlib import Path

import yaml
from environs import Env

from headway.infrastructure.database.sql.config import SQLConfig


@dataclass
class AIConfig:
    base_url: str
    api: str
    model: str
    language: str
    prompt_messages: list[str]


@dataclass
class Config:
    db: SQLConfig
    ai: AIConfig


def get_ai_config(env: Env, config_path: Path = Path("config.yml")) -> AIConfig:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return AIConfig(
        base_url=config["ai"]["base_url"],
        api=env.str("AI_API"),
        model=config["ai"]["model"],
        language=config["ai"]["language"],
        prompt_messages=config["ai"]["prompt_messages"],
    )


def get_config(
        db: SQLConfig,
        ai: AIConfig,
) -> Config:
    return Config(
        db=db,
        ai=ai
    )
