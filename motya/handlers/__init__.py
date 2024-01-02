from . import (
    accept_file,
    basic,
    help,
    commands,
    answers,
    games,
    reactions,
    replies,
    default,
    rating,
)
from config import dp


dp.include_router(accept_file.router)
dp.include_router(basic.router)
dp.include_router(help.router)
dp.include_router(games.router)
dp.include_router(commands.router)
dp.include_router(answers.router)
dp.include_router(reactions.router)
dp.include_router(replies.router)
dp.include_router(default.router)
dp.include_router(rating.router)
