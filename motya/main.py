import asyncio

from aiogram import Bot, Dispatcher

from utils.startup import on_startup


async def main(dp: Dispatcher, motya: Bot):
    await on_startup()
    await dp.start_polling(motya)


if __name__ == "__main__":
    from utils.environment import check_environment

    check_environment()

    import handlers
    from config import dp, motya

    asyncio.run(main(dp, motya))
