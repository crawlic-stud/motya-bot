from dataclasses import dataclass, asdict


@dataclass
class MessageData:
    user_id: int
    text: str
        
    def prepare_to_save(self):
        return asdict(self)
    