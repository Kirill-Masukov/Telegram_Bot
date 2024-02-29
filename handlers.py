import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from utils import api_weather, save_history
from keyboard import weather_kb


class ChooseWeather(StatesGroup):
    GET_CITY = State()
    GET_WEATHER = State()


router = Router()


@router.message(Command('help'))
async def command_help(message: Message):
    await message.answer('Я бот, предоставляющий метеорологические данные о городах')


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await message.answer(text=f'Привет, {message.from_user.full_name}!'
                              f'\nНапиши мне название города, метеорологические данные о котором ты хочешь узнать')
    await state.set_state(ChooseWeather.GET_CITY)


@router.message(ChooseWeather.GET_CITY)
async def get_city(message: Message, state: FSMContext):
    city = message.text
    data = api_weather(city)
    if data['cod'] == '404':
        await message.reply("\U00002620 Ошибка!!! Такого города нет \U00002620\nВведите название города повторно")
    else:
        await state.update_data(data=data)
        await state.update_data(history=[])
        await state.set_state(ChooseWeather.GET_WEATHER)
        await message.answer('Какую информацию о городе хочешь узнать?', reply_markup=weather_kb)


@router.message(ChooseWeather.GET_WEATHER, F.text == 'Температура')
async def get_temp(message: Message, state: FSMContext):
    data = (await state.get_data())
    city = data["name"]
    cur_weather = data["main"]["temp"]
    await message.reply(
        f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"В городе: {city}\nТемпература: {cur_weather}C°")
    history = (await state.get_data())['history']
    history.append(f'Температура: {cur_weather}C°')
    await state.update_data(history=history)


@router.message(ChooseWeather.GET_WEATHER, F.text == 'Влажность')
async def get_humidity(message: Message, state: FSMContext):
    data = (await state.get_data())
    city = data["name"]
    humidity = data["main"]["humidity"]
    await message.reply(
        f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"В городе: {city}\nВлажность: {humidity}%")
    history = (await state.get_data())['history']
    history.append(f'Влажность: {humidity}%')
    await state.update_data(history=history)


@router.message(ChooseWeather.GET_WEATHER, F.text == 'Давление')
async def get_pressure(message: Message, state: FSMContext):
    data = (await state.get_data())
    city = data["name"]
    pressure = data["main"]["pressure"]
    await message.reply(
        f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"В городе: {city}\nДавление: {pressure} мм.рт.ст")
    history = (await state.get_data())['history']
    history.append(f'Давление: {pressure} мм.рт.ст')
    await state.update_data(history=history)


@router.message(ChooseWeather.GET_WEATHER, F.text == 'Продолжительность дня')
async def get_length_day(message: Message, state: FSMContext):
    data = (await state.get_data())
    city = data["name"]
    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
     data["sys"]["sunrise"])
    await message.reply(
        f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"В городе: {city}\nПродолжительность дня: {length_of_the_day}\n"
        f"Восход: {sunrise_timestamp}\n Закат: {sunset_timestamp}")
    history = (await state.get_data())['history']
    history.append(f'Продолжительность дня: {length_of_the_day}, Восход: {sunrise_timestamp},'
                   f'Закат: {sunset_timestamp}')
    await state.update_data(history=history)


@router.message(ChooseWeather.GET_WEATHER, F.text == 'Сброс')
async def reset(message: Message, state: FSMContext):
    await message.answer('***Хорошего дня***', reply_markup=ReplyKeyboardRemove())
    data = (await state.get_data())
    city = data["name"]
    user = message.from_user.full_name
    day_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    history = ' '.join(data['history'])
    text = f'Пользователь: {user}, Дата: {day_time}, Город: {city}, {history}'
    save_history(text)
    await state.clear()
