from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import dp
from filters.motya_command import MotyaCommand
from utils.games import HangmanGame, WordleGame, get_word


class GameState(StatesGroup):
    hangman = State()
    wordle = State()


@dp.message_handler(MotyaCommand(["отмена", "стоп"], strict=True), state="*")
async def cancel_game(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("отменил игру.")


@dp.message_handler(MotyaCommand(["виселица", "игра"], strict=True), state="*")
async def start_hangman_game(message: types.Message, state: FSMContext):
    await message.reply(
        "поиграем в виселицу! чтобы закончить, скажи: <i>мотя отмена</i> или <i>мотя стоп</i>"
    )
    async with state.proxy() as data:
        word = get_word(message.chat.id, 10)
        data["game"] = HangmanGame(word.lower())
        await GameState.hangman.set()
    await message.answer(data["game"].render())
    await message.answer("отправь первую букву, чтобы угадать, что написано :з")


@dp.message_handler(state=GameState.hangman)
async def run_hangman_game(message: types.Message, state: FSMContext):
    if len(message.text) > 1:
        return
    letter = message.text.lower()
    async with state.proxy() as data:
        game: HangmanGame = data["game"]
        if letter in game.wrong_letters or letter in game.guessed_letters:
            await message.reply("эту букву уже угадывали!")

        elif letter in game.word:
            await message.reply("верно!")
            game.guessed_letters.add(letter)
        else:
            await message.reply("неверно!")
            game.step += 1

        await message.answer(game.render())

        if game.lost:
            await state.finish()
            await message.answer(
                "вы проиграли \('o')/\nчтоб сыграть еще раз напишите: <i>мотя игра</i> или <i>мотя виселица</i>"
            )
        elif game.won:
            await state.finish()
            await message.answer(
                "вы победили !!!!!!\nчтоб сыграть еще раз напишите: <i>мотя игра</i> или <i>мотя виселица</i>"
            )


@dp.message_handler(MotyaCommand(["вордл", "wordle"], strict=True), state="*")
async def start_wordle_game(message: types.Message, state: FSMContext):
    await message.reply(
        "поиграем в wordle! чтобы закончить, скажи: <i>мотя отмена</i> или <i>мотя стоп</i>"
    )
    async with state.proxy() as data:
        word = get_word(message.chat.id, 6)
        data["game"] = WordleGame(word.lower())
        await GameState.wordle.set()
    await message.answer(f"отправь первое слово длиной {len(word)} букв, чтобы начать!")


@dp.message_handler(state=GameState.wordle)
async def run_wordle_game(message: types.Message, state: FSMContext):
    guess = message.text.lower().strip()
    async with state.proxy() as data:
        game: WordleGame = data["game"]
        if len(guess) != len(game.word):
            await message.reply(f"отправь слово длиной {len(game.word)}!")
            return
        game.prev_guesses.append(guess)
        await message.reply(game.render())

        if guess == game.word:
            await state.finish()
            await message.reply("урааа! победа!")

        elif game.lost:
            await state.finish()
            await message.answer(
                f"вы проиграли, правильно было: {game.word.upper()}\nчтоб сыграть еще раз напишите: <i>мотя вордл</i>"
            )
