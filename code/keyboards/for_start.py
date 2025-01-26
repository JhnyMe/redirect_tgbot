from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_tags_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Просмотр тегов")
    kb.button(text="Добавить тег")
    kb.button(text="Удалить тег")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)