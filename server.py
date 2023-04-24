import marks
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.contrib.fsm_storage.memory import MemoryStorage


class UserState(StatesGroup):
    loqin = State()
    password = State()
    url_active = State()
    loqin2 = State()
    password2 = State()


bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

inline_kb_full = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton('Мои оценки', callback_data='btn1'))\
    .add(InlineKeyboardButton('Расписание звонков', callback_data='btn2'))\
    .add(InlineKeyboardButton('Табель оценок', callback_data='btn3'))\


inline_kb_nl = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton('Следущая страница', callback_data='next'))\
    .add(InlineKeyboardButton('Предыдущая страница', callback_data='last'))\
    .add(InlineKeyboardButton('Показать домашнее задание', callback_data='btn5'))\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu'))

inline_kb_nl2 = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton('Следущая страница', callback_data='next'))\
    .add(InlineKeyboardButton('Предыдущая страница', callback_data='last'))\
    .add(InlineKeyboardButton('Показать оценки', callback_data='btn4'))\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu'))

inline_kb_nl3 = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton('Показать средний балл', callback_data='btn6'))\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu'))

inline_kb_nl4 = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton('Показать оценки', callback_data='btn7'))\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu'))

inline_kb_nl5 = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton('Понедельник', callback_data='btn8'))\
    .add(InlineKeyboardButton('Другие дни', callback_data='btn9'))\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu1'))

inline_kb_nl6 = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton('Вернуться на главную', callback_data='menu1'))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Здраствуйте!\nЯ телеграм-бот "Мой дневник" \nВыберите что вам нужно',
                        reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(url_active='https://edu.tatar.ru/user/diary/week')
    data = await state.get_data()
    if data != {'url_active': 'https://edu.tatar.ru/user/diary/week'}:
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'], obj='mark'),
                               reply_markup=inline_kb_nl)
        await UserState.url_active.set()
    else:
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, 'Введите ваш логин от Edu-tatar')
        await UserState.loqin.set()


@dp.message_handler(state=UserState.loqin)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Отлично! Теперь введите ваш пароль.")
    await UserState.next()


@dp.message_handler(state=UserState.password)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        await message.answer(f"Логин: {data['login']}\n"
                             f"Пароль: {data['password']}")
        await message.answer(marks.marks(data['login'], data['password'], obj='mark'), reply_markup=inline_kb_nl)
        await UserState.next()
    except:
        await message.answer("Пожалуйста, укажите верные данные для Edu-tatar\nПопробуй снова")
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
        await callback_query.message.delete()
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
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                        data['url_active'], obj='mark'),
                               reply_markup=inline_kb_nl)
    except:
        await bot.send_message(callback_query.from_user.id, 'Еще недоступно')


@dp.callback_query_handler(lambda c: c.data == 'btn4', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                    data['url_active'], obj='mark'),
                           reply_markup=inline_kb_nl)


@dp.callback_query_handler(lambda c: c.data == 'btn5', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, marks.marks(data['login'], data['password'],
                                                                    data['url_active'], obj='task'),
                           reply_markup=inline_kb_nl2)


@dp.callback_query_handler(lambda c: c.data == 'menu', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Выберите что вам нужно", reply_markup=inline_kb_full)
    data = await state.get_data()
    data['url_active'] = 'https://edu.tatar.ru/user/diary/week'


@dp.callback_query_handler(lambda c: c.data == 'menu1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Выберите что вам нужно", reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'btn2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Выберите день недели', reply_markup=inline_kb_nl5)


@dp.callback_query_handler(lambda c: c.data == 'btn8')
async def process_callback_button1(
            callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Понедельник:\n 1) 08:35 - 09:15 \n '
                                                        '2) 09:20 - 10:00 \n 3) 10:10 - 10:50 \n '
                                                        '4) 11:05 - 11:45 \n 5) 11:55 - 12:35 \n '
                                                        '6) 12:40 - 13:20 \n Вторая смена: \n '
                                                        '1) 13:25 - 14:05 \n 2) 14:15 - 14:55 \n '
                                                        '3) 15:05 - 15:45 \n 4) 15:50 - 16:30 \n '
                                                        '5) 16:35 - 17:15 \n 6) 17:20 - 18:00', reply_markup=inline_kb_nl6)


@dp.callback_query_handler(lambda c: c.data == 'btn9')
async def process_callback_button1(
            callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Другие дни:\n 1) 08:00 - 08:40 \n '
                                                        '2) 08:45 - 09:25 \n 3) 09:35 - 10:15 \n '
                                                        '4) 10:30 - 11:10 \n 5) 11:20 - 12:00 \n '
                                                        '6) 12:05 - 12:45 \n 7) 12:50 - 13:30 \n '
                                                        'Вторая смена: \n 1) 13:30 - 14:10 \n '
                                                        '2) 14:20 - 15:00 \n 3) 15:05 - 15:45 \n '
                                                        '4) 15:50 - 16:30 \n 5) 16:35 - 17:15 \n '
                                                        '6) 17:20 - 18:00', reply_markup=inline_kb_nl6)


@dp.callback_query_handler(lambda c: c.data == 'btn3')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data != {}:
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, marks.tab(data['login'], data['password'], obj='marks'),
                               reply_markup=inline_kb_nl3)
        await UserState.url_active.set()
    else:
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, 'Введите ваш логин от Edu-tatar')
        await UserState.loqin2.set()


@dp.message_handler(state=UserState.loqin2)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Отлично! Теперь введите ваш пароль.")
    await UserState.next()


@dp.message_handler(state=UserState.password2)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        await message.answer(f"Логин: {data['login']}\n"
                             f"Пароль: {data['password']}")
        await message.answer(marks.tab(data['login'], data['password'], obj='marks'), reply_markup=inline_kb_nl3)
        await UserState.url_active.set()
    except:
        await message.answer("Пожалуйста, укажите верные данные для Edu-tatar\nПопробуй снова")
        await state.finish()
        await message.answer('Введите ваш логин')
        await UserState.loqin2.set()


@dp.callback_query_handler(lambda c: c.data == 'btn6', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, marks.tab(data['login'], data['password'], obj='average'),
                           reply_markup=inline_kb_nl4)


@dp.callback_query_handler(lambda c: c.data == 'btn7', state=UserState.url_active)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, marks.tab(data['login'], data['password'], obj='marks'),
                           reply_markup=inline_kb_nl4)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
