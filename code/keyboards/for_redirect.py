from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_redirect_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить пост", callback_data="Отправить пост")
    kb.button(text="Отмена", callback_data="Отмена")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)