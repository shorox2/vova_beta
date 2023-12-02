from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from tg_bot.misc.states import DatingStateGroup
from aiogram.dispatcher.storage import FSMContext
from tg_bot.keyboards.reply import kb_guide
import asyncio


async def start_cmd(message: types.Message):
    # await message.answer_video_note()
    await message.delete()
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action='record_video_note')
    await asyncio.sleep(3)
    await message.bot.send_video_note(chat_id=message.from_user.id,
                                      video_note='DQACAgIAAxkBAAICD2VrT9mFwnwiVJWLx26bGmXUU9gFAAJxOQACDTNZS8UTGR84WsAAATME')
    await DatingStateGroup.name.set()

async def wait_name_cmd(message: types.Message, state: FSMContext):
    await message.answer('Отлично, а теперь напиши мне свой возраст')
    await DatingStateGroup.next()

async def wait_age_cmd(message: types.Message, state: FSMContext):
    await message.answer('Расскажи, пожалуйста, кратко почему тебя заинтересовала тема правильного питания и фитнеса?')
    await DatingStateGroup.next()

async def wait_desc_cmd(message: types.Message, state: FSMContext):
    await message.answer(f'Благодарю тебя за ответы! Вот обещанные рецепты смузи.\n'
                         'Я уверен, что ты сможешь легко приготовить их самостоятельно всего за 10-15 минут в день,'
                         'а польза от них будет огромной!\nНаслаждайся вкусными и полезными напитками и заботься о своем здоровье!'
                         '\nПомни, что здоровое питание - это основа хорошего самочувствия и энергии на весь день.',
                         reply_markup=kb_guide)
    await state.finish()


def register_begin_command(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart())
    dp.register_message_handler(wait_name_cmd, state=DatingStateGroup.name)
    dp.register_message_handler(wait_age_cmd, state=DatingStateGroup.age)
    dp.register_message_handler(wait_desc_cmd, state=DatingStateGroup.desc)

