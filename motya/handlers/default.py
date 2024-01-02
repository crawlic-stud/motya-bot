from aiogram import types, Router


router = Router(name="default")


@router.message()
async def save_message(_: types.Message):
    pass
