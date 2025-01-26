from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
import json,os
from keyboards.for_start import get_tags_keyboard
from aiogram.fsm.context import FSMContext
from states.states import UserStates

file_json = "tags.json"
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Что будем делать с тегами?", reply_markup=get_tags_keyboard())

@router.message(F.text.lower() == "просмотр тегов")
async def answer_look(message: Message):
    if os.path.exists(file_json):
        if os.path.getsize(file_json) > 0:
            await message.answer("Вот тебе список тегов:", reply_markup=get_tags_keyboard())
            full_result = ""
            with open(file_json, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Загружаем данные из файла
            for item in data:
                id_value = item.get("id")
                name_value = item.get("name")
                full_result += (f"{id_value}:{name_value}\n")
            await message.answer(full_result)
        

        else: await message.answer("Файл есть, но нет каких-либо тегов. Сначала добавьте тег с помощью кнопки \"Добавить тег\"", reply_markup=get_tags_keyboard())
    else:
        await message.answer("Самого файла нет. Сначала добавьте тег с помощью кнопки \"Добавить тег\"", reply_markup=get_tags_keyboard())
    

@router.message(F.text.lower() == "добавить тег")
async def answer_add(message: Message, state: FSMContext):
    await message.answer("Введите название тега", reply_markup=get_tags_keyboard())
    await state.set_state(UserStates.waiting_for_add)

@router.message(F.text.lower() == "удалить тег")
async def answer_dell(message: Message, state: FSMContext):
    if os.path.exists(file_json):
        if os.path.getsize(file_json) > 0:
            await message.answer("Введите номер тега, который надо удалить", reply_markup=get_tags_keyboard())
            await state.set_state(UserStates.waiting_for_delete)
        else: await message.answer("Файл есть, но нет каких-либо тегов. Сначала добавьте тег с помощью кнопки \"Добавить тег\"", reply_markup=get_tags_keyboard())
    else:
        await message.answer("Самого файла нет. Сначала добавьте тег с помощью кнопки \"Добавить тег\"", reply_markup=get_tags_keyboard())

@router.message(UserStates.waiting_for_add)
async def add_tags(message: Message, state: FSMContext):
    if os.path.getsize(file_json) > 0:
        with open(file_json, "r", encoding="utf-8") as file:
            id_tags = json.load(file)
        new_id = max(id_tags_max["id"] for id_tags_max in id_tags) + 1
    else:
        id_tags = []
        new_id = 0
    new_record = {"id": new_id, "name": message.text}
    id_tags.append(new_record)
    with open(file_json, "w", encoding="utf-8") as file:
        json.dump(id_tags, file, ensure_ascii=False, indent=4)
    await message.answer(f"Новая запись с id={new_id} и именем {message.text} добавлена в tags.json")
    await state.clear()  # Завершаем состояние

#Здесь обработка удаления тега

@router.message(UserStates.waiting_for_delete)
async def dell_tags(message: Message, state: FSMContext):
    target_id = int(message.text)
    with open(file_json, "r", encoding="utf-8") as file:
        id_tags = json.load(file)
    found = False
    for item in id_tags:
        if item.get("id") == target_id:
            found = True
            await message.answer(f"Найден тег с id ={item.get('id')} и именем {item.get('name')}. Он удален")
            id_tags.remove(item)
            with open(file_json, "w", encoding="utf-8") as file:
                json.dump(id_tags, file, ensure_ascii=False, indent=4)
            await state.clear()  # Завершаем состояние
            break
    if not found:
        await message.answer(f"Тег с id = {message.text} не найден")
        await state.clear()  # Завершаем состояние

