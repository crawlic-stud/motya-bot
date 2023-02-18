from aiogram import executor


if __name__ == "__main__":
    from utils.environment import check_environment
    check_environment()
    
    import handlers
    from config import dp 
    
    executor.start_polling(dp, skip_updates=True)
    