from typing import List

from aiogram.dispatcher.filters import Filter
from aiogram import types


class Reaction(Filter):
    def __init__(
        self,
        patterns: List[str],
        strict: bool = False
    ) -> None:
        super().__init__()
        self.patterns = patterns
        self.strict = strict

    async def check(self, message: types.Message) -> bool:
        msg = message.text.lower()

        if self.strict:
            is_pattern = any(pattern in msg.split() for pattern in self.patterns)
        else:
            is_pattern = any(pattern in msg for pattern in self.patterns)

        return is_pattern
