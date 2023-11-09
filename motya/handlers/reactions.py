import random

from aiogram import types
from config import dp, db
from filters.reaction import Reaction
from utils.tools import roll_chance

LAUGH_CHANCE = 10 / 100


@dp.message_handler(Reaction(["аха", "ахх", "хах", "хха"]))
async def send_hahaha(message: types.Message):
    patterns = ["AXA", "XA", "AX", "ПХ", "BX"]
    patterns_lower = list(map(str.lower, patterns))
    chosen_patterns = random.choice([patterns, patterns_lower])
    laugh = "".join(
        [random.choice(chosen_patterns) for _ in range(random.randint(5, 15))]
    )
    if roll_chance(LAUGH_CHANCE):
        await message.answer(laugh)


@dp.message_handler(Reaction(["ссор", "ругат", "ругал", "поссор", "руган"]))
async def update_arguments_count(message: types.Message):
    arg_time = db.get_days_since_last_argument(message.chat.id)
    db.insert_new_argument(message.chat.id)
    await message.reply(
        "зафиксировал ссору. ну и дураки вы. "
        + f"с прошлой ссоры прошло всего лишь {arg_time}"
    )
