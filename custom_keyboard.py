from telebot import types


def make_navigator(without_button=None):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    if without_button == 'right':
        button_prev = types.InlineKeyboardButton('←', callback_data='prev')
        inline_keyboard.add(button_prev)
        return inline_keyboard
    elif without_button == 'left':
        button_next = types.InlineKeyboardButton('→', callback_data='next')
        inline_keyboard.add(button_next)
        return inline_keyboard
    else:
        button_next = types.InlineKeyboardButton('→', callback_data='next')
        button_prev = types.InlineKeyboardButton('←', callback_data='prev')
        inline_keyboard.add(button_prev, button_next)
        return inline_keyboard


def button_open_in_spotify(artist_url):
    inline_keyboard = types.InlineKeyboardMarkup()
    open_in_spotify = types.InlineKeyboardButton('Открыть на Spotify', url=artist_url)
    inline_keyboard.add(open_in_spotify)
    return inline_keyboard