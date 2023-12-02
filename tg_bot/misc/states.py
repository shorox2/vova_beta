from aiogram.dispatcher.filters.state import StatesGroup, State

class DatingStateGroup(StatesGroup):
    name = State()
    age = State()
    desc = State()

class AnswerStateGroup(StatesGroup):
    desc = State()

class TarifStateGroup(StatesGroup):
    answer = State()