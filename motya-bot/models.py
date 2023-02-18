from typing import List

from aiogram.dispatcher.filters import Filter
from aiogram import types

from dataclasses import dataclass, asdict


COMMAND_PREFIX = "мотя"


class MotyaCommand(Filter):
    def __init__(
        self, 
        commands: List[str], 
        strict: bool = False
     ) -> None:
        super().__init__()
        self.commands = commands
        self.strict = strict
        
    async def check(self, message: types.Message) -> bool:
        msg = message.text.lower()
        
        is_prefixed = msg.startswith(COMMAND_PREFIX) 
        if self.strict:
            msg = msg.replace(COMMAND_PREFIX, "").strip()
            is_command = is_prefixed and any(command in msg.split() for command in self.commands)
        else:
            is_command = is_prefixed and any(command in msg for command in self.commands)
            
        return is_command
                

@dataclass
class MessageData:
    user_id: int
    text: str
        
    def dict(self):
        return asdict(self)
    