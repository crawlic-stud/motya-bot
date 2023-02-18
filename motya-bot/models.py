from dataclasses import dataclass, asdict


@dataclass
class MessageData:
    user_id: int
    text: str
        
    def dict(self):
        return asdict(self)
    