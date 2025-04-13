import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()

import database


API_TOKEN = '7383378706:AAEHT3fKEW7DT3AsV5JsqMxH5S00bzPaFZs'
bot = Bot(token=API_TOKEN)


user_languages = {}

waiting_for_feedback = State() 

ADMIN_ID =  1169513021

async def on_startup():
    await database.setup_database()

@dp.message(Command("start"))
async def start(message: types.Message):
    user_languages[message.from_user.id] = "uz"  # 🔧 Default til: O'zbek

    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'zbek🇺🇿", callback_data="uz")],
        [InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"),
         InlineKeyboardButton(text="English🇺🇸", callback_data="en")]
    ])

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 Foydalanuvchi @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}) botni ishga tushirdi."
    )

    await message.answer(
        "Iltimos tilni tanlang: \n Выберите язык: \n Please choose your language:",
        reply_markup=inline_markup
    )

    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="/serial"), KeyboardButton(text="/kino")]
    ])

    await message.answer("@TvMoonuz_bot", reply_markup=reply_markup)


@dp.callback_query(F.data.in_(["uz", "ru", "en"]))
async def handle_language_selection(call: CallbackQuery):
    user_languages[call.from_user.id] = call.data
    await show_main_menu(call)

async def show_main_menu(call: CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Kino", callback_data="category_movies")],
        [InlineKeyboardButton(text="📺 Serial", callback_data="category_series")]
    ])

    messages = {
        "uz": "Nimani ko‘rmoqchisiz?",
        "ru": "Что вы хотите посмотреть?",
        "en": "What would you like to watch?"
    }

    await call.message.edit_text(messages[language], reply_markup=markup)


@dp.callback_query(F.data == "category_series")
async def show_series_selection(call: CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    genres = await database.get_series_genres(language)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, callback_data=f"series_{key}")]
        for key, name in genres.items()]
    )
    messages = {
        "uz": "Serial janrini tanlang:",
        "ru": "Выберите жанр сериала:",
        "en": "Choose a series genre:"
    }
    await call.message.edit_text(messages[language], reply_markup=markup)


@dp.callback_query(F.data.startswith("series_"))
async def handle_series_selection(call: CallbackQuery):
    genre_key = call.data.split("_")[1]
    language = user_languages.get(call.from_user.id, "uz")
    series = await database.get_series_by_genre(language, genre_key)

    if not series:
        messages = {
            "uz": "Bu janrda serillar yo‘q.",
            "ru": "В этом жанре нет сериала.",
            "en": "No series found in this genre."
        }
        await call.answer(messages[language], show_alert=True)
        return

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=title.strip(), url=link.strip())]
        for s in set(series) if (parts := s.split(" - ")) and len(parts) == 2
        for title, link in [parts]]
    )

    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish"},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена"},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel"}
    }

    markup.inline_keyboard.append([
        InlineKeyboardButton(text=buttons_text[language]["back"], callback_data="category_series"),
        InlineKeyboardButton(text=buttons_text[language]["cancel"], callback_data="cancel")
    ])

    messages = {
        "uz": "Mavjud seriallar:",
        "ru": "Доступные сериалы:",
        "en": "Available series:"
    }
    await call.message.edit_text(messages[language], reply_markup=markup)


@dp.callback_query(F.data == "category_movies")
async def show_genre_selection(call: CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    genres = await database.get_movie_genres(language)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, callback_data=f"genre_{key}")]
        for key, name in genres.items()]
    )
    messages = {
        "uz": "Kino janrini tanlang:",
        "ru": "Выберите жанр фильма:",
        "en": "Choose a movie genre:"
    }
    await call.message.edit_text(messages[language], reply_markup=markup)


@dp.callback_query(F.data.startswith("genre_"))
async def handle_genre_selection(call: CallbackQuery):
    genre_key = call.data.split("_")[1]
    language = user_languages.get(call.from_user.id, "uz")
    movies = await database.get_movies_by_genre(language, genre_key)

    if not movies:
        messages = {
            "uz": "Bu janrda kinolar yo‘q.",
            "ru": "В этом жанре нет фильмов.",
            "en": "No movies found in this genre."
        }
        await call.answer(messages[language], show_alert=True)
        return

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=title.strip(), url=link.strip())]
        for m in set(movies) if (parts := m.split(" - ")) and len(parts) == 2
        for title, link in [parts]]
    )

    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish"},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена"},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel"}
    }

    markup.inline_keyboard.append([
        InlineKeyboardButton(text=buttons_text[language]["back"], callback_data="category_movies"),
        InlineKeyboardButton(text=buttons_text[language]["cancel"], callback_data="cancel")
    ])

    messages = {
        "uz": f"🎬 Kino janri: {genre_key}",
        "ru": f"🎬 Фильмы в жанре {genre_key}",
        "en": f"🎬 Movies in the {genre_key} genre"
    }
    await call.message.edit_text(messages[language], reply_markup=markup)


def latin_to_cyrillic(text):
    replacements = {
        "ya": "я", "yu": "ю", "yo": "ё", "ch": "ч", "sh": "ш", "o'": "ў", "g'": "ғ", "e": "э",
        "a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к",
        "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т",
        "u": "у", "v": "в", "x": "х", "y": "й", "z": "з"
    }
    for latin, cyrillic in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = text.replace(latin, cyrillic)
    return text

def cyrillic_to_latin(text):
    replacements = {
        "я": "ya", "ю": "yu", "ё": "yo", "ч": "ch", "ш": "sh", "ў": "o'", "ғ": "g'", "э": "e",
        "а": "a", "б": "b", "д": "d", "ф": "f", "г": "g", "ҳ": "h", "и": "i", "ж": "j", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "қ": "q", "р": "r", "с": "s", "т": "t",
        "у": "u", "в": "v", "х": "x", "й": "y", "з": "z"
    }
    for cyrillic, latin in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = text.replace(cyrillic, latin)
    return text



@dp.message(F.text.regexp(r"(?i)^(?!\/).{3,}$"))
async def plain_text_search(message: types.Message):
    query = message.text.strip().lower()  # Qidiruvni kichik harflarga aylantiramiz
    language = user_languages.get(message.from_user.id, "uz")

    # Transliteratsiyalar
    query_latin = cyrillic_to_latin(query)
    query_cyrillic = latin_to_cyrillic(query)

    # Har uch variantda qidiruv: asl, lotin, kirill
    results = await database.search_movies_and_series(language, query)
    if not results:
        results = await database.search_movies_and_series(language, query_cyrillic)
    if not results:
        results = await database.search_movies_and_series(language, query_latin)

    response_messages = {
        "uz": {"found": "🔍 Natijalar:\n", "not_found": "😕 Hech narsa topilmadi."},
        "ru": {"found": "🔍 Результаты:\n", "not_found": "😕 Ничего не найдено."},
        "en": {"found": "🔍 Results:\n", "not_found": "😕 Nothing found."}
    }

    if not results:
        await message.answer(response_messages[language]["not_found"])
    else:
        unique_results = set(results)
        result_text = response_messages[language]["found"] + "\n\n".join(unique_results)
        await message.answer(result_text)

    # Admin log
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔍 @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}) matnli qidiruv berdi: {query}"
    )



@dp.message(Command("kino"))
async def movie(message: types.Message):
    language = user_languages.get(message.from_user.id, "uz")
    movie_genres = await database.get_movie_genres(language)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, callback_data=f"genre_{key}")]
        for key, name in movie_genres.items()]
    )
    messages = {
        "uz": "Kino janrini tanlang:",
        "ru": "Выберите жанр фильма:",
        "en": "Choose a movie genre:"
    }
    await message.answer(messages[language], reply_markup=markup)


@dp.message(Command("serial"))
async def series(message: types.Message):
    language = user_languages.get(message.from_user.id, "uz")
    series_genres = await database.get_series_genres(language)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=name, callback_data=f"series_{key}")]
        for key, name in series_genres.items()]
    )
    messages = {
        "uz": "Serial janrini tanlang:",
        "ru": "Выберите жанр сериала:",
        "en": "Choose a series genre:"
    }
    await message.answer(messages[language], reply_markup=markup)

@dp.message(Command("myid", "profile"))
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    language = user_languages.get(user_id, "uz")

    lang_display = {
        "uz": "O'zbek 🇺🇿",
        "ru": "Русский 🇷🇺",
        "en": "English 🇺🇸"
    }

    await message.answer(
        f"🆔 ID: `{user_id}`\n"
        f"🌐 Tanlangan til: {lang_display.get(language, 'Noma’lum')}",
        parse_mode="Markdown"
    )

@dp.message(Command("language"))
async def change_language(message: types.Message):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O'zbek🇺🇿", callback_data="uz")],
        [InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"),
         InlineKeyboardButton(text="English🇺🇸", callback_data="en")]
    ])

    await message.answer(
        "🌐 Iltimos, yangi tilni tanlang:\nВыберите новый язык:\nPlease choose a new language:",
        reply_markup=inline_markup
    )


@dp.callback_query(F.data == "cancel")
async def cancel_handler(call: CallbackQuery):
    await call.message.delete()


@dp.message(Command("clear"))
async def clear_messages(message: types.Message):
    for i in range(message.message_id, message.message_id - 100, -1):
        try:
            await bot.delete_message(message.chat.id, i)
        except Exception:
            continue


@dp.message(Command("help"))
async def help_command(message: types.Message):
    language = user_languages.get(message.from_user.id, "uz")
    messages = {
        "uz": "/start - Botni yangilaydi\n/movie - Kinolar janrini chiqaradi\n/series - Serial janrlarini chiqaradi\n/search <nom> - Kino yoki serialni topadi\n/clear - Oxirgi xabarlarni o‘chiradi",
        "ru": "/start - Обновляет бота\n/movie - Показывает жанры фильмов\n/series - Показывает жанры сериалов\n/search <name> - Находит фильм или сериал\n/clear - Очищает последние сообщения",
        "en": "/start - Updates bot\n/movie - Shows movie genres\n/series - Shows series genres\n/search <name> - Finds a movie or series\n/clear - Clears recent messages"
    }
    await message.answer(messages[language])


# /request komandasiga javob
@dp.message(Command("request"))
async def request_feedback(message: types.Message, state: FSMContext):
    language = user_languages.get(message.from_user.id, "uz")
    messages = {
        "uz": "Taklif va Fikirlaringizni yozib qoldiring:",
        "ru": "Оставьте свои предложения и мнения:",
        "en": "Leave your suggestions and opinions:"
    }
    await message.answer(messages[language])
    await state.set_state(FeedbackStates.waiting_for_feedback)

# Fikrni olish
@dp.message(F.state == FeedbackStates.waiting_for_feedback)
async def handle_feedback(message: types.Message, state: FSMContext):
    user_feedback = message.text
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Yangi fikr:\n👤 @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id})\n\n📝 {user_feedback}"
    )
    await message.answer("✅ Fikringiz adminlarga yuborildi. Rahmat!")
    await state.clear()


async def main():
    await on_startup()

    dp.message.register(handle_feedback, F.state == FeedbackStates.waiting_for_feedback)

    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
