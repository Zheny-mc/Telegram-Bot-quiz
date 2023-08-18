from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tokens import bot_token
from dto import DataBase, TextAndKeyboard

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
        return

    if user['is_passing']:
        return

    db.set_user(message.chat.id, {'question_index': 0, 'is_passing': True})

    user = db.get_user(message.chat.id)
    post = get_question_message(user)
    if post is not None:
        await message.answer(post.text, reply_markup=post.keyboard)

@dp.callback_query_handler(Text(startswith='?ans'))
async def answered(query: types.CallbackQuery):
    user = db.get_user(query.message.chat.id)
    if user is None or not user['is_passing'] or user['is_passed']:
        return

    arg = int(query.data.split('&')[1])
    user["answers"].append(arg)
    db.set_user(query.message.chat.id, {"answers": user["answers"]})

    post: TextAndKeyboard = get_answered_message(user)
    if post is not None:
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=post.text,
                                    reply_markup=post.keyboard)

@dp.callback_query_handler(Text(startswith='?next'))
async def c_next(query: types.CallbackQuery):
    user = db.get_user(query.message.chat.id)

    if user is None or user["is_passed"] or not user["is_passing"]:
        return

    user["question_index"] += 1
    db.set_user(query.message.chat.id, {"question_index": user["question_index"]})

    post = get_question_message(user)
    if post is not None:
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=post.text,
                                    reply_markup=post.keyboard)

def get_final_grade(user):
    ''' Получить итоговая оценка '''
    count = 0
    for i_q, question in enumerate(db.questions.find({})):
        if question['is_right'] == user['answers'][i_q]:
            count += 1

    percents = round( 100 * count / db.question_counts )

    smile = "\U0001F642"
    if percents < 40:
        smile = "\U0001F913"
    elif percents < 60:
        smile = "\U0001F9D0"
    elif percents < 90:
        smile = "\U0001F60E"

    text = f"Вы правильно ответили на {percents}% вопросов {smile}"
    db.set_user(user['chat_id'], {'is_passing': False, 'is_passed': True})

    return TextAndKeyboard(text, None)


def get_question_message(user):
    if user['question_index'] == db.question_counts:
        return get_final_grade(user)

    question = db.get_question(user['question_index'])

    if question is None:
        return

    text = f'Вопрос №{user["question_index"]+1}\n\n{question["title"]}'

    keyboard = InlineKeyboardMarkup()
    for ans_i, answer in enumerate(question['answers']):
        keyboard.row(InlineKeyboardButton(text=answer, callback_data=f'?ans&{ans_i}') )

    return TextAndKeyboard(text, keyboard)


def get_answered_message(user):
    question = db.get_question(user['question_index'])
    text = f'Вопрос №{user["question_index"]+1}\n\n{question["title"]}\n'

    for ans_i, answer in enumerate(question['answers']):
        text += answer

        if ans_i == question['is_right']:
            text += ' \U00002714'
        elif ans_i == user['answers'][-1]:
            text += ' \U0000274C'

        text += '\n'
    keyboard = InlineKeyboardMarkup().row(InlineKeyboardButton(text='Далее', callback_data=f'?next'))

    return TextAndKeyboard(text, keyboard)





executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



