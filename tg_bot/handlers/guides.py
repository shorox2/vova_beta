from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InputFile
from tg_bot.keyboards.inline import ikb_choice, cb, ikb_simple_choice, ikb_obrez
from aiogram.dispatcher.storage import FSMContext
from tg_bot.misc.states import AnswerStateGroup
import asyncio

async def send_guide_cmd(message: types.Message):
    await message.answer(text='Забирай)',
                         reply_markup=ReplyKeyboardRemove())
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action='upload_document')
    await message.bot.send_document(chat_id=message.from_user.id,
                                    document=open('tg_bot/ГайдВовы.pdf', 'rb'),
                                    protect_content=True,
                                    reply_markup=ikb_choice)

async def choice_yes_cmd(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer('Оставь обратную связь')
    await AnswerStateGroup.desc.set()
    await call.answer()

async def choice_no_cmd(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.bot.send_chat_action(chat_id=call.message.chat.id,
                                        action='record_video_note')
    await asyncio.sleep(3)
    await call.message.bot.send_video_note(chat_id=call.message.chat.id,
                                      video_note='DQACAgIAAxkBAAICD2VrT9mFwnwiVJWLx26bGmXUU9gFAAJxOQACDTNZS8UTGR84WsAAATME',
                                      reply_markup=ReplyKeyboardRemove())
    await call.message.answer('После ознакомления с гайдом',
                              reply_markup=ikb_obrez)



async def question_cmd(message: types.Message, state: FSMContext):
    await message.answer(f'Благодарю тебя за отзыв!\n'
                    'Кстати, сейчас есть уникальная возможность присоединиться к моему 2-х недельному детокс-марафону!\n'
                    'Этот марафон создан для того, чтобы в короткие сроки освободить организм от токсинов,'
                    'сбалансировать питание и обогатить его всеми необходимыми питательными веществами')

    await message.answer(f'Что ты получишь за 14 дней в марафоне:\n'
                          '- Сбросишь лишний вес\n'
                          '- Улучшишь общее состояние организма\n'
                          '- Внедришь новые полезные привычки в свою жизнь\n'
                          '- Получишь заряд энергии и бодрости\n'
                          'Хочешь узнать подробнее?',
                          reply_markup=ikb_simple_choice)
    await state.finish()


def register_guide_command(dp: Dispatcher):
    dp.register_message_handler(send_guide_cmd, Text(equals='ПОЛУЧИТЬ ГАЙД'))
    dp.register_callback_query_handler(choice_yes_cmd, cb.filter(action='yes'))
    dp.register_callback_query_handler(choice_no_cmd, cb.filter(action='no'))
    dp.register_message_handler(question_cmd, state = AnswerStateGroup.desc)
