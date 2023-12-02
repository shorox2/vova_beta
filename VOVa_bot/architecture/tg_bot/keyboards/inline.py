from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('ikb', 'action')
light_cb = CallbackData('simple', 'action')


ikb_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да, я уже изучил гайд', callback_data=cb.new('yes'))],
    [InlineKeyboardButton(text="Нет, еще не открывал", callback_data=cb.new('no'))]
])

ikb_simple_choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text='Да, расскажи про тарифы', callback_data=light_cb.new('yes')), InlineKeyboardButton(text="Нет", callback_data=light_cb.new('no'))]
])

ikb_obrez = InlineKeyboardMarkup(row_width=1,inline_keyboard=[
    [InlineKeyboardButton(text='Жми сюда!', callback_data=cb.new('yes'))]
])