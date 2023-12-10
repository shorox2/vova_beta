from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from gspread_asyncio import AsyncioGspreadClient

from tg_bot.services.google_shets import create_spreadsheet, add_worksheet, share_spreadsheet, fill_in_data


async def create_spreadsheet_for_user(message: types.Message, state = FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action='typing')
    google_client_manager = message.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()
    key = '1Ab1VawH0nBD2CX30p_Mg0eBQtfBa6udwALWdPfiok1g'

    # async_spreadsheet = await create_spreadsheet(google_client, 'Новый файл')
    # await add_worksheet(async_spreadsheet, 'Новый лист (рабочий)')
    # await share_spreadsheet(google_client,file_id= async_spreadsheet.ss.id, value='sergiowahgame@mail.ru')
    # url = async_spreadsheet.ss.url
    await state.update_data(
        spreadsheet = key
    )
    await message.answer(f'Ваш файл находится тут https://docs.google.com/spreadsheets/d/{key}')

async def get_statistic(message: types.Message, state = FSMContext):
    google_client_manager = message.bot.get('google_client_manager')
    google_client: AsyncioGspreadClient = await google_client_manager.authorize()
    ids = [message.from_user.id, '123456789']
    names = [message.from_user.first_name, 'Shorox']
    desc = ['Описание 1', 'Описание 2']
    data = tuple(zip(ids, names, desc))
    data_fsm = await state.get_data()
    key = data_fsm.get('spreadsheet')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.get_worksheet(0)
    await fill_in_data(worksheet, data)

    await message.answer('Данные были заполнены')

def register_google_command(dp: Dispatcher):
    dp.register_message_handler(create_spreadsheet_for_user, Command('create'))
    dp.register_message_handler(get_statistic, Command('get_stats'))