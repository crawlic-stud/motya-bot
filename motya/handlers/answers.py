from aiogram import types, Router
from config import common_db, motya
from filters.motya_command import MotyaCommand
from utils.message_manager import random_sentence_with_start, reply_with_kb


router = Router(name="answers")


async def answer_starts_with(starts: list[str], message: types.Message):
    messages = common_db.get_messages_from_chat(message.chat.id)
    sentence = await random_sentence_with_start(
        starts, messages, message.chat.id, bot=motya
    )
    await reply_with_kb(message, sentence) if sentence else None


@router.message(
    MotyaCommand(["как тебе"], description="отвечаю на вопрос", strict=False),
)
async def question1(m: types.Message):
    await answer_starts_with(["ну", "хз", "супер", "не", "что"], m)


@router.message(
    MotyaCommand(["как"], description="отвечаю на вопрос", strict=True),
)
async def question2(m: types.Message):
    await answer_starts_with(["так", "вот"], m)


@router.message(
    MotyaCommand(["что"], description="отвечаю на вопрос", strict=True),
)
async def question3(m: types.Message):
    await answer_starts_with(["это", "такое"], m)


@router.message(
    MotyaCommand(["почему"], description="отвечаю на вопрос", strict=True),
)
async def question4(m: types.Message):
    await answer_starts_with(["потому"], m)
