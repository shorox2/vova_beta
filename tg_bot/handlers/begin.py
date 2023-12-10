import gspread_asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from tg_bot.misc.states import DatingStateGroup
from aiogram.dispatcher.storage import FSMContext
from tg_bot.keyboards.reply import kb_guide
from gspread_asyncio import AsyncioGspreadClient
import asyncio
from tg_bot.services.google_shets import fill_in_data


async def start_cmd(message: types.Message):

    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action='record_video_note')
    google_client_manager = message.bot.get('google_client_manager')
    google_client: AsyncioGspreadClient = await google_client_manager.authorize()
    await asyncio.sleep(3)
    await message.bot.send_video_note(chat_id=message.from_user.id,
                                      video_note='DQACAgIAAxkBAAICD2VrT9mFwnwiVJWLx26bGmXUU9gFAAJxOQACDTNZS8UTGR84WsAAATME')
    await message.delete()
    await DatingStateGroup.name.set()


async def wait_name_cmd(message: types.Message, state: FSMContext):
    key = '1Ab1VawH0nBD2CX30p_Mg0eBQtfBa6udwALWdPfiok1g'
    await state.update_data(
        spreadsheet=key
    )
    async with state.proxy() as data:
        data['FIO'] = message.text
        data['id'] = str(message.from_user.id)
        if message.from_user.username == None:
            data['f_name'] = '-'
        else:
            data['f_name'] = message.from_user.username

    await DatingStateGroup.next()
    await message.answer('Отлично, а теперь напиши мне свой возраст')

async def wait_age_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await DatingStateGroup.next()
    await message.answer('Расскажи, пожалуйста, кратко почему тебя заинтересовала тема правильного питания и фитнеса?')

async def wait_desc_cmd(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action='typing')
    google_client_manager = message.bot.get('google_client_manager')
    google_client: AsyncioGspreadClient = await google_client_manager.authorize()
    async with state.proxy() as data:
        data['desc'] = message.text
        fdata = (data['id'], data['f_name'],data['FIO'] ,data['age'], data['desc'])
    data_fsm = await state.get_data()
    key = data_fsm.get('spreadsheet')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.get_worksheet(0)
    await fill_in_data(worksheet, fdata)
    await state.reset_state(with_data=False)
    await message.answer(f'Благодарю тебя за ответы! Вот обещанные рецепты смузи.\n'
                         'Я уверен, что ты сможешь легко приготовить их самостоятельно всего за 10-15 минут в день,'
                         'а польза от них будет огромной!\nНаслаждайся вкусными и полезными напитками и заботься о своем здоровье!'
                         '\nПомни, что здоровое питание - это основа хорошего самочувствия и энергии на весь день.',
                         reply_markup=kb_guide)



def register_begin_command(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart())
    dp.register_message_handler(wait_name_cmd, state=DatingStateGroup.name)
    dp.register_message_handler(wait_age_cmd, state=DatingStateGroup.age)
    dp.register_message_handler(wait_desc_cmd, state=DatingStateGroup.desc)

