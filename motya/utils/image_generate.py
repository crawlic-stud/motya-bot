import io

from aiogram import types

from config import image_api


async def reply_with_image(
    message: types.Message, prompt: str, caption: str | None = None
):
    motya_prompt = (
        f"{prompt}\n"
        "стиль: детский рисунок, кривые линии, простой рисунок, разноцветный рисунок, карандашный рисунок, "
        "неразборчивый рисунок, неряшливый рисунок, неаккуратный рисунок, набросок"
    )
    image_bytes = await image_api.generate_image(motya_prompt)
    if image_bytes:
        f = types.InputFile(io.BytesIO(image_bytes), filename="motyadraw.png")
        await message.reply_photo(f, caption=caption)
    else:
        await message.reply("не получилось(")
