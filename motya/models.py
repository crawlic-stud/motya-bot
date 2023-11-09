from dataclasses import asdict, dataclass
from datetime import timedelta
import datetime


@dataclass
class MessageData:
    user_id: int
    text: str
    compiled: bool = False

    def prepare_to_save(self):
        return asdict(self)


@dataclass
class ArgumentTimeElapsed:
    days: int
    hours: int
    minutes: int
    seconds: int

    @classmethod
    def from_timedelta(cls, delta: timedelta):
        total_hours, seconds_remain = divmod(delta.seconds, 60 * 60)
        total_minites, seconds_remain = divmod(seconds_remain, 60)
        return cls(
            days=delta.days,
            hours=total_hours,
            minutes=total_minites,
            seconds=seconds_remain,
        )

    def __str__(self) -> str:
        return (
            f"{self.days} дн. {self.hours} ч. {self.minutes} мин. {self.seconds} сек."
        )


if __name__ == "__main__":
    print(
        ArgumentTimeElapsed.from_timedelta(
            datetime.datetime.now() - datetime.datetime(2023, 11, 1, 1, 19, 0)
        )
    )
