from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard


admin_router = Router()


class Test(StatesGroup):
    #Шаги состояний
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'Test:name': 'Введите название заново:',
        'Test:description': 'Введите описание заново:',
        'Test:price': 'Введите стоимость заново:',
        'Test:image': 'Этот стейт последний, поэтому...',
    } # Write: keys: (Test:...)


# Realization №1 (mine)

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    states_list = list(Test.__states__) # Change "Test" to your StatesGroup Class
    current_index = states_list.index(current_state)

    if current_index > 0:
        previous_state = states_list[current_index - 1]
        await state.set_state(previous_state)
        await message.answer(Test.texts[previous_state.state], reply_markup=types.ReplyKeyboardRemove())
    else:
        await state.clear()
        await message.answer("Вы вернулись в начало", reply_markup=your_KB)
        
        
        
# Realization №2 (Not mine) - Him - https://www.youtube.com/@PythonHubStudio

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

  
    if current_state == Test.name: # Change "Test" to your StatesGroup Class
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return
    previous = None
    for step in Test.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {Test.texts[previous.state]}")
            return
        previous = step


