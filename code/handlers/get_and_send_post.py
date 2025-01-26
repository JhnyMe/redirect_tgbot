from aiogram import Router, F
from aiogram.types import Message
from states.states import UserStates
from aiogram import Bot
from keyboards.for_redirect import get_redirect_keyboard
from aiogram.fsm.context import FSMContext
import json
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


router = Router()
file_json = "tags.json"


@router.message(F.media_group_id)
async def message_with_media(message: Message, state: FSMContext):
    await message.answer("Это пост с многими медиа воедино", reply_markup=None)
    if message.caption:
            await message.answer("Это пост с текстом")
    else:
            await message.answer("Это пост только с медиа")

@router.message(F.video)
async def message_with_photo(message: Message, state: FSMContext):
    if message.forward_from or message.forward_from_chat:
        if message.caption:
            await message.answer("Это пост с видео и текстом", reply_markup=None)
            await message.answer("Введите номер тега, который нужно добавить")
            await state.update_data(video_id=message.video.file_id, caption=message.caption)
            await state.set_state(UserStates.waiting_for_send_video)
        else:
            await message.answer("Это пост только с видео", reply_markup=None)
            await message.answer("Введите номер тега, который нужно добавить")
            await state.set_state(UserStates.waiting_for_send_video)

@router.message(F.photo)
async def message_with_photo(message: Message, state: FSMContext):
    if message.caption:
        await message.answer("Это пост с картинкой и текстом", reply_markup=None)
    else:
        await message.answer("Это пост только с картинкой", reply_markup=None)

@router.message(F.document)
async def message_with_photo(message: Message, state: FSMContext):
    if message.caption:
        await message.answer("Это пост с документом и текстом", reply_markup=None)
    else:
        await message.answer("Это пост только с документом", reply_markup=None)

@router.message(F.sticker)
async def message_with_sticker(message: Message, state: FSMContext):
    await message.answer("Это стикер!", reply_markup=None)

@router.message(F.animations)
async def message_with_gif(message: Message, state: FSMContext):
    await message.answer("Это GIF!", reply_markup=None)


@router.message(UserStates.waiting_for_send_video)
async def send_post(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    video_id = data.get("video_id")
    caption_text = data.get("caption")
    target_id = int(message.text)
    with open(file_json, "r", encoding="utf-8") as file:
        id_tags = json.load(file)
    found = False
    for item in id_tags:
        if item.get("id") == target_id:
            found = True
            await message.answer(f"Найден тег с id ={item.get('id')} и именем {item.get('name')}. И он был добавлен к тексту. Пост выглядит вот так:")
            new_caption = caption_text + f"\n\n#{item.get('name')}"
            await state.update_data(new_caption=new_caption)
            await message.answer_video(video=video_id, caption=new_caption)
            await message.answer("Отправляем?", reply_markup=get_redirect_keyboard())
            break
    if not found:
        await message.answer(f"Тег с id = {message.text} не найден. Введите его еще раз")
        await state.set_state(UserStates.waiting_for_send)

@router.callback_query(UserStates.waiting_for_confirmation)
async def handle_confirmation(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    video_id = data.get("video_id")
    new_caption = data.get("new_caption")

    if callback.data == "Отправить пост":
        # Отправляем пост в канал
        await bot.send_video(chat_id="@jhnymtestchannel", video=video_id, caption=new_caption)
        await callback.message.answer("Пост успешно отправлен в канал!")
        await state.clear()  # Завершаем состояние
    elif callback.data == "Отмена":
        await callback.message.answer("Отправка отменена. Введите новый тег.")
        await state.set_state(UserStates.waiting_for_send_video)  # Возвращаемся в состояние ожидания ввода тега

    await callback.answer()  # Подтверждаем обработку callback



@router.message(F.text)
async def message_with_text(message: Message, state: FSMContext):
    if message.forward_from or message.forward_from_chat:
        await message.answer("Это текстовое пересланное сообщение!")
    else:
        await message.answer("Сообщение с текстом написано просто Вами")