from distutils.sysconfig import PREFIX
from aiogram import types
from aiogram.filters import Filter

from models import CommandInfo

# almost all bot commands starts with this prefix
COMMAND_PREFIX = "мотя"
motya_commands: list[CommandInfo] = []


class MotyaCommand(Filter):
    def __init__(
        self, commands: list[str], description: str | None = None, strict: bool = False
    ) -> None:
        super().__init__()
        self.commands = commands
        self.strict = strict
        if description:
            motya_commands.append(CommandInfo(COMMAND_PREFIX, commands, description))

    async def __call__(self, message: types.Message) -> bool:
        msg = message.text.lower() if message.text else ""

        is_prefixed = msg.startswith(COMMAND_PREFIX)
        if self.strict:
            msg = msg.replace(COMMAND_PREFIX, "").strip()
            is_command = is_prefixed and any(
                command in msg.split() for command in self.commands
            )
        else:
            is_command = is_prefixed and any(
                command in msg for command in self.commands
            )

        return is_command


class MotyaQuestion(MotyaCommand):
    def __init__(
        self, commands: list[str], description: str, strict: bool = False
    ) -> None:
        super().__init__(commands, description, strict)

    async def __call__(self, message: types.Message) -> bool:
        is_command = await super().__call__(message)
        return is_command and (message.text.endswith("?") if message.text else False)
