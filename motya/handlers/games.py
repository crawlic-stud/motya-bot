from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.motya_command import MotyaCommand
from utils.games import HangmanGame, WordleGame, get_word


router = Router(name="games")


class GameState(StatesGroup):
    hangman = State()
    wordle = State()


@router.message(
    MotyaCommand(["отмена", "стоп"], description="отмена игры", strict=True)
)
async def cancel_game(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("отменил игру.")


@router.message(
    MotyaCommand(["виселица", "игра"], description="игра в виселицу", strict=True)
)
async def start_hangman_game(message: types.Message, state: FSMContext):
    await message.reply(
        "поиграем в виселицу! чтобы закончить, скажи: <i>мотя отмена</i> или <i>мотя стоп</i>"
    )
    word = get_word(message.chat.id, 10)
    game = HangmanGame(word.lower())
    await state.update_data({"game": game})
    await state.set_state(GameState.hangman)

    await message.answer(game.render())
    await message.answer("отправь первую букву, чтобы угадать, что написано :з")


@router.message(GameState.hangman)
async def run_hangman_game(message: types.Message, state: FSMContext):
    msg_text = message.text if message.text else ""
    if len(msg_text) > 1:
        return
    letter = msg_text.lower()
    data = await state.get_data()
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
        await state.clear()
        await message.answer(
            "вы проиграли \\('o')/\nчтоб сыграть еще раз напишите: <i>мотя игра</i> или <i>мотя виселица</i>"
        )
    elif game.won:
        await state.clear()
        await message.answer(
            "вы победили !!!!!!\nчтоб сыграть еще раз напишите: <i>мотя игра</i> или <i>мотя виселица</i>"
        )


@router.message(
    MotyaCommand(["вордл", "wordle"], description="игра в wordle", strict=True)
)
async def start_wordle_game(message: types.Message, state: FSMContext):
    await message.reply(
        "поиграем в wordle! чтобы закончить, скажи: <i>мотя отмена</i> или <i>мотя стоп</i>"
    )
    word = get_word(message.chat.id, 6)
    await state.update_data({"game": WordleGame(word.lower())})
    await state.set_state(GameState.wordle)
    await message.answer(f"отправь первое слово длиной {len(word)} букв, чтобы начать!")


@router.message(GameState.wordle)
async def run_wordle_game(message: types.Message, state: FSMContext):
    guess = message.text.lower().strip() if message.text else ""
    data = await state.get_data()
    game: WordleGame = data["game"]
    if len(guess) != len(game.word):
        await message.reply(f"отправь слово длиной {len(game.word)}!")
        return
    game.prev_guesses.append(guess)
    await message.reply(game.render())

    if guess == game.word:
        await state.clear()
        await message.reply("урааа! победа!")

    elif game.lost:
        await state.clear()
        await message.answer(
            f"вы проиграли, правильно было: {game.word.upper()}\nчтоб сыграть еще раз напишите: <i>мотя вордл</i>"
        )
