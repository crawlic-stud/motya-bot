from aiogram import types
from aiogram.filters import Filter


class Reaction(Filter):
    def __init__(self, patterns: list[str], strict: bool = False) -> None:
        super().__init__()
        self.patterns = patterns
        self.strict = strict

    async def __call__(self, message: types.Message) -> bool:
        msg = message.text.lower() if message.text else ""

        if self.strict:
            is_pattern = any(pattern in msg.split() for pattern in self.patterns)
        else:
            is_pattern = any(pattern in msg for pattern in self.patterns)

        return is_pattern
