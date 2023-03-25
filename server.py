import marks
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.contrib.fsm_storage.memory import MemoryStorage


class UserState(StatesGroup):
    loqin = State()
    password = State()
    url_active = State()


bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

inline_kb_full = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Мои оценки', callback_data='btn1'))\
    .add(InlineKeyboardButton('Расписание звонков', callback_data='btn2'))

inline_kb_nl = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Следущая неделя', callback_data='next'))\
    .add(InlineKeyboardButton('Предыдущая неделя', callback_data='last'))\
    .add(InlineKeyboardButton('Показать домашнее задание', callback_data='btn5'))\
    .add(InlineKeyboardButton('Назад', callback_data='n'))

inline_kb_nl2 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Следущая неделя', callback_data='next'))\
    .add(InlineKeyboardButton('Предыдущая неделя', callback_data='last'))\
    .add(InlineKeyboardButton('Показать оценки', callback_data='btn4'))\
    .add(InlineKeyboardButton('Назад', callback_data='n'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Привет!\nЯ умный телеграм-бот "Мой дневник" \nВыбери что тебе нужно',
                        reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data != {}:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'], obj='mark'),
                               reply_markup=inline_kb_nl)
        await UserState.url_active.set()
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Введите ваш логин')
        await UserState.loqin.set()


@dp.message_handler(state=UserState.loqin)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Отлично! Теперь введите ваш пароль.")
    await UserState.next()


@dp.message_handler(state=UserState.password)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.update_data(url_active='https://edu.tatar.ru/user/diary/week')
    data = await state.get_data()
    try:
        await message.answer(f"Логин: {data['login']}\n"
                             f"Пароль: {data['password']}")
        await message.answer(marks.marks(data['login'], data['password'], obj='mark'), reply_markup=inline_kb_nl)
        await UserState.next()
    except:
        await message.answer("Пожалуйста, укажи верные данные для edu.tatar\nПопробуй снова")
        await state.finish()
        await message.answer('Введите ваш логин')
        await UserState.loqin.set()


@dp.callback_query_handler(lambda c: c.data == 'last', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    try:
        await state.update_data(url_active=marks.last_w(data['login'], data['password'], data['url_active']))
        data = await state.get_data()
        await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                        data['url_active'], obj='mark'),
                               reply_markup=inline_kb_nl)
    except:
        await bot.send_message(callback_query.from_user.id, 'Уже недоступно')


@dp.callback_query_handler(lambda c: c.data == 'next', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data = await state.get_data()
    try:
        await state.update_data(url_active=marks.next_w(data['login'], data['password'], data['url_active']))
        data = await state.get_data()
        await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                        data['url_active'], obj='mark'),
                               reply_markup=inline_kb_nl)
    except:
        await bot.send_message(callback_query.from_user.id, 'Еще недоступно')


@dp.callback_query_handler(lambda c: c.data == 'btn4', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                    data['url_active'], obj='mark'),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'btn5', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                    data['url_active'], obj='task'),
                           reply_markup=inline_kb_nl2)


@dp.callback_query_handler(lambda c: c.data == 'n', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Что тебе нужно?", reply_markup=inline_kb_full)
    data = await state.get_data()
    data['url_active'] = 'https://edu.tatar.ru/user/diary/week'


@dp.callback_query_handler(lambda c: c.data == 'btn2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Расписание в разработке')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)