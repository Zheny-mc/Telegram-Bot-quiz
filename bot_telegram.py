from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tokens import bot_token
from dto import DataBase

async def on_startup(_):
    print('Бот вышел в онлайн!')

bot = Bot(bot_token())
dp = Dispatcher(bot)
db = DataBase()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = db.get_user(message.chat.id)

    if user['is_passed']:
        await message.answer('Вы уже проходили эту викторину.')

    # if user['is_passing']:
    #     return

    db.set_user(message.chat.id, {'question_index': 0, 'is_passing': True})

    user = db.get_user(message.chat.id)
    post = get_question_message(user)
    if post is not None:
        await message.answer(post['text'], reply_markup=post['keyboard'])


def get_question_message(user):
    if user['question_index'] == db.question_counts:
        return

    question = db.get_question(user['question_index'])

    if question is None:
        return

    text = f'Вопрос №{user["question_index"]+1}\n\n{question["title"]}'

    keyboard = InlineKeyboardMarkup()
    for ans_i, answer in enumerate(question['answers']):
        keyboard.row(InlineKeyboardButton(text=answer, callback_data=f'?ans&{ans_i}') )

    return {
        "text": text,
        "keyboard": keyboard
    }

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



