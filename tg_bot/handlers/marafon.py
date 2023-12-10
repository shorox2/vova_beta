from aiogram import types, Dispatcher
from gspread_asyncio import AsyncioGspreadClient

from tg_bot.keyboards.inline import light_cb
from tg_bot.keyboards.reply import kb_tarifics
from aiogram.dispatcher.storage import FSMContext
from tg_bot.misc.states import TarifStateGroup
from aiogram.types import ReplyKeyboardRemove
import asyncio

from tg_bot.services.google_shets import refactor2_in_data


async def simple_yes_cmd(call: types.CallbackQuery, state: FSMContext):
    await call.message.bot.send_photo(chat_id=call.message.chat.id,
                                      photo='https://sun9-14.userapi.com/impg/kPawoJ5-KnCRBflztCMziAHHUpURRDOarCLKsw/Ck6_iwpMwZo.jpg?size=922x529&quality=96&sign=591e44296bc32189c178f8e5f3e54f12&type=album',
                                      caption='1 тариф')
    await call.message.bot.send_photo(chat_id=call.message.chat.id,
                                      photo='https://sun9-18.userapi.com/impg/D-dAZdItz0S4aSr3zl4KBmFG9n94xF-2qZ07yA/TEVWW36Lgu4.jpg?size=1163x658&quality=96&sign=ae05f8ba6191a766e891199131a68cf8&type=album',
                                      caption='2 тариф')
    await call.message.bot.send_photo(chat_id=call.message.chat.id,
                                      photo='https://sun9-44.userapi.com/impg/lRSdM-oFeP6qDBuwB3JPnZgufOMVVAaXrhiiiQ/bgj84Fhxqqs.jpg?size=995x685&quality=96&sign=72923f64f78a27a67cb77163ba782da1&type=album',
                                      caption='3 тариф',
                                      reply_markup=kb_tarifics)
    await call.answer()
    await TarifStateGroup.answer.set()

# async def simple_no_cmd(call: types.CallbackQuery):
#     await call.message.answer('ЖОПА В МЫЛЕ, МЫ ТАКОГО НЕ ОЖИДАЛИ!')
#     await call.answer()
#

async def tarif_plane_cmd(message: types.Message, state: FSMContext):
    google_client_manager = message.bot.get('google_client_manager')
    google_client: AsyncioGspreadClient = await google_client_manager.authorize()
    async with state.proxy() as data:
        data['tarif'] = message.text
        fdata = (data['id'], data['tarif'])
    if message.text.split(' ')[0] == 'Тариф':
        await message.bot.send_chat_action(chat_id=message.from_user.id,
                                        action='record_video_note')
        await asyncio.sleep(3)
        await message.bot.send_video_note(chat_id=message.from_user.id,
                                          video_note='DQACAgIAAxkBAAICD2VrT9mFwnwiVJWLx26bGmXUU9gFAAJxOQACDTNZS8UTGR84WsAAATME',
                                          reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Конечно, я понимаю, что тебе нужно время,'
                             'чтобы обдумать все. В скором времени я напишу тебе в личные сообщения.'
                             'Если у тебя возникнут вопросы, мы сможем обсудить их вместе!',
                             reply_markup=ReplyKeyboardRemove())
        # Обновить табличку
    data_fsm = await state.get_data()
    key = data_fsm.get('spreadsheet')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.get_worksheet(0)
    await refactor2_in_data(worksheet, fdata)
    await state.finish()


def register_marafoni_command(dp: Dispatcher):
    dp.register_callback_query_handler(simple_yes_cmd, light_cb.filter(action='yes'))
    # dp.register_callback_query_handler(simple_no_cmd, light_cb.filter(action='no'))
    dp.register_message_handler(tarif_plane_cmd, state=TarifStateGroup.answer)