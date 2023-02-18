from aiogram import executor


if __name__ == "__main__":
    import handlers
    from config import dp 

    executor.start_polling(dp, skip_updates=True)
    