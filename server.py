import marks

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from bs4 import beautifulsoup

login = ''
password = ''
TOKEN = "5379058684:AAFD4kCxjJDJrhVuqAdbYbceNlGD3nasObw"


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

inline_kb_full = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Мои оценки', callback_data='btn1'))\
    .add(InlineKeyboardButton('Расписание звонков', callback_data='btn2'))\
    .add(InlineKeyboardButton('Расписание уроков', callback_data='btn3'))

inline_kb_nl = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Следущая неделя', callback_data='next'))\
    .add(InlineKeyboardButton('Предыдущая неделя', callback_data='last'))\
    .add(InlineKeyboardButton('Показать оценки', callback_data='btn4'))\
    .add(InlineKeyboardButton('Показать домашнее задание', callback_data='btn5'))\
    .add(InlineKeyboardButton('Назад', callback_data='n'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет!\nЯ умный телеграм-бот "Мой дневник" \nВыбери что тебе нужно',
                        reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if login == '':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Введите логин в формате\n/log *ваш логин*')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, marks.marks(login, password), reply_markup=inline_kb_nl)


@dp.message_handler(commands=['log'])
async def cmd_name(message: types.Message, command: {}):
    global login
    if command.args:
        login = command.args
        await message.answer("Введите пароль в формате\n/pas *ваш пароль*")
    else:
        await message.answer("Пожалуйста, укажи свой логин после команды /log!")


@dp.message_handler(commands=['pas'])
async def cmd_name(message: types.Message, command: {}):
    global password
    if command.args:
        password = command.args
        try:
            await message.answer(marks.marks(login, password), reply_markup=inline_kb_nl)
        except:
            await message.answer("Пожалуйста, укажи верные данные для edu.tatr\nПопробуй снова")
    else:
        await message.answer("Пожалуйста, укажи свой пароль после команды /pas!")


@dp.callback_query_handler(lambda c: c.data == 'last')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.last_w(login, password),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'next')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.next_w(login, password),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'btn4')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.marks(login, password, obj='mark'),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'btn5')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.marks(login, password, obj='task'),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'n')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Что тебе нужно?", reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'btn2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Расписание в разработке')


@dp.callback_query_handler(lambda c: c.data == 'btn3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Расписание в разработке')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)