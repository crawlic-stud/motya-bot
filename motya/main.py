import asyncio

from aiogram import Bot, Dispatcher

from utils.startup import on_startup
from middlewares.message_saver import MessageSaver
from middlewares.random_sender import RandomSender
from config import messages_data, common_db


async def main(dp: Dispatcher, motya: Bot):
    # middleware for saving messages to DB
    dp.message.middleware(MessageSaver(messages_data, common_db))
    dp.message.middleware(RandomSender(common_db, motya))

    await on_startup()
    await dp.start_polling(motya)


if __name__ == "__main__":
    from utils.environment import check_environment

    check_environment()

    import handlers
    from config import dp, motya

    asyncio.run(main(dp, motya))
