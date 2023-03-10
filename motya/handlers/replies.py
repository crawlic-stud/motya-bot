import random

from aiogram import types

from config import dp
from filters.motya_command import MotyaCommand
from utils.tools import words_after, roll_chance


@dp.message_handler(MotyaCommand(["прив", "дарова", "дороу", "ку"]))
async def send_hello(message: types.Message):
    answer = random.choice(['ку', 'дороу', 'салам', 'привет'])
    await message.reply(answer)

    
@dp.message_handler(MotyaCommand(["пока", "бб"], strict=True))
async def send_bye(message: types.Message):
    answer = random.choice(['бб', 'пока', 'покеда', 'давай'])
    await message.reply(answer)
    
    
@dp.message_handler(MotyaCommand(["иди"], strict=True))
async def send_not_going(message: types.Message):
    await message.reply("не пойду")
    

@dp.message_handler(MotyaCommand(["молодец", "умница", "лучший"]))
async def send_thank_you(message: types.Message):
    answer = random.choice(['спасибо', 'ты тоже', 'хехех', 'вау', 'да ну...'])
    await message.reply(answer)


@dp.message_handler(MotyaCommand(["как дела"]))
async def send_whats_up(message: types.Message):
    answer = random.choice(['норм все', 'все хорошо', 'я в тильте', 'супер', 'все четко'])
    await message.reply(answer)
    
    
@dp.message_handler(MotyaCommand(["ты"], strict=True))
async def send_maybe_you(message: types.Message):
    user_id = message.from_user.id
    answer = f'а может <a href="tg://user?id={user_id}">ты</a> {words_after(message.text, "ты")}?'
    await message.reply(answer)
    