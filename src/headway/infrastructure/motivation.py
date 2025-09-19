import json
import logging

from aiohttp import ClientSession

from headway.application.intefaces import IMotivationProvider
from headway.domain.entitites import Motivation
from headway.infrastructure.config import AIConfig


class MotivationProvider(IMotivationProvider):
    def __init__(self, config: AIConfig):
        self.session = ClientSession()
        self.config = config

    async def get_random_motivation(self, task_text: str | None = None) -> Motivation:
        url = self.config.base_url
        headers = {
            'Authorization': f'Bearer {self.config.api}',
        }
        payload = {
            "model": self.config.model,
            "messages": json.loads(
                json.dumps(self.config.prompt_messages)
                .replace("{{ task }}", task_text if task_text else "")
                .replace("{{language }}", self.config.language)
            )
        }
        async with self.session.post(
                url=url,
                headers=headers,
                json=payload
        ) as response:
            data = await response.json()
            logging.debug(data)
            text = data['choices'][0]['message']['content']
            await self.session.close()
            return Motivation.create(text=text, category="affirmation")
