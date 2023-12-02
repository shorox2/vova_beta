from aiogram import types, Dispatcher
from tg_bot.misc.states import DatingStateGroup, AnswerStateGroup, TarifStateGroup
from aiogram.dispatcher.storage import FSMContext



async def check_name_cmd(message: types.Message, state: FSMContext):
    await message.answer('Напиши фамилию и имя через пробел\nПример: Владимир Самодуров')

async def check_age_cmd(message: types.Message, state: FSMContext):
    await message.answer('Похоже ты ошибся, напиши свой возраст пожалуйста')

async def check_desc_cmd(message: types.Message, state: FSMContext):
    await message.answer('Как-то маловато, можешь чуть поподробнее')

async def check_tarif_cmd(message: types.Message, state: FSMContext):
    await message.answer('Выбери тарифный план пожалуйста')


def register_check_command(dp: Dispatcher):
    dp.register_message_handler(check_name_cmd,lambda message: not message.text or len(message.text.split(' ')) != 2 ,state=DatingStateGroup.name)
    dp.register_message_handler(check_age_cmd, lambda message: not message.text.isdigit() or float(message.text) < 0 or float(message.text) > 100, state=DatingStateGroup.age)
    dp.register_message_handler(check_desc_cmd, lambda message: not message.text or len(message.text) < 3 or len(message.text.split(' ')) < 2, state= DatingStateGroup.desc )
    dp.register_message_handler(check_desc_cmd, lambda message: not message.text or len(message.text) < 3 or len(message.text.split(' ')) < 2, state= AnswerStateGroup.desc)
    dp.register_message_handler(check_tarif_cmd, lambda message: not message.text or message.text.split(' ')[0] != 'Тариф' and message.text != 'Я пoдумаю 💩', state = TarifStateGroup.answer)