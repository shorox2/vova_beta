from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_guide = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = KeyboardButton('ПОЛУЧИТЬ ГАЙД')
kb_guide.add(kb1)

kb_tarifics = ReplyKeyboardMarkup(resize_keyboard=True)
kb11 = KeyboardButton('Тариф 1')
kb21 = KeyboardButton('Тариф 2')
kb31 = KeyboardButton('Тариф 3')
kb41 = KeyboardButton('Я пoдумаю 💩')
kb_tarifics.add(kb11).add(kb21).add(kb31).add(kb41)