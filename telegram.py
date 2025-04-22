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

class BroadcastState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()

API_TOKEN = '7383378706:AAEHT3fKEW7DT3AsV5JsqMxH5S00bzPaFZs'
bot = Bot(token=API_TOKEN)


user_languages = {}

waiting_for_feedback = State() 

ADMIN_ID =  1169513021
user_list = set()

async def on_startup():
    await database.setup_database()


user_list = set()  # Barcha foydalanuvchilar
joined_users = set()  # Botga kirgan foydalanuvchilar
left_users = set()  # Botdan chiqib ketgan foydalanuvchilar

# Statistika komandasi
@dp.message(Command('stat'))
async def show_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz.")
        return

    # Statistikani ko'rsatish
    total_users = len(user_list)  # Foydalanuvchilar soni
    joined = len(joined_users)  # Kirgan foydalanuvchilar soni
    left = len(left_users)  # Chiqib ketgan foydalanuvchilar soni

    # Statistika natijasi
    stats_message = f"Botda jami foydalanuvchilar soni: {total_users}\n"
    stats_message += f"Kirgan foydalanuvchilar soni: {joined}\n"
    stats_message += f"Chiqib ketgan foydalanuvchilar soni: {left}"

    await message.answer(stats_message)

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
    parts = call.data.split("_")
    genre_key = parts[1]
    page = int(parts[3]) if len(parts) > 3 and parts[2] == "page" else 1  # Page calculation

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

    # Remove duplicates
    seen = set()
    unique_series = []
    for s in series:
        if s not in seen:
            seen.add(s)
            unique_series.append(s)
    series = unique_series

    # Pagination
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    page_series = series[start:end]

    # Generate inline keyboard with series titles and links
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title.strip(), url=link.strip())]
            for s in page_series if (parts := s.split(" - ")) and len(parts) == 2
            for title, link in [parts]
        ]
    )

    # Buttons for pagination
    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish", "next": "➡ ", "prev": "⬅ "},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена", "next": "➡ ", "prev": "⬅ "},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel", "next": "➡ ", "prev": "⬅ "}
    }

    nav_buttons = []
    if start > 0:  # Previous page button
        nav_buttons.append(InlineKeyboardButton(
            text=buttons_text[language]["prev"],
            callback_data=f"series_{genre_key}_page_{page - 1}"
        ))
    if end < len(series):  # Next page button
        nav_buttons.append(InlineKeyboardButton(
            text=buttons_text[language]["next"],
            callback_data=f"series_{genre_key}_page_{page + 1}"
        ))

    if nav_buttons:
        markup.inline_keyboard.append(nav_buttons)

    # Adding back and cancel buttons
    markup.inline_keyboard.append([
        InlineKeyboardButton(text=buttons_text[language]["back"], callback_data="category_series"),
        InlineKeyboardButton(text=buttons_text[language]["cancel"], callback_data="cancel")
    ])

    # Send message with available series and pagination
    messages = {
        "uz": f"Mavjud seriallar (sahifa {page}):",
        "ru": f"Доступные сериалы (страница {page}):",
        "en": f"Available series (page {page}):"
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
    parts = call.data.split("_")
    genre_key = parts[1]
    page = int(parts[3]) if len(parts) > 3 and parts[2] == "page" else 1

    language = user_languages.get(call.from_user.id, "uz")
    movies = await database.get_movies_by_genre(language, genre_key)

    # Tartibni saqlab dublikatlarni olib tashlash
    seen = set()
    unique_movies = []
    for m in movies:
        if m not in seen:
            seen.add(m)
            unique_movies.append(m)
    movies = unique_movies

    if not movies:
        messages = {
            "uz": "Bu janrda kinolar yo‘q.",
            "ru": "В этом жанре нет фильмов.",
            "en": "No movies found in this genre."
        }
        await call.answer(messages[language], show_alert=True)
        return

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    page_movies = movies[start:end]

    markup = InlineKeyboardMarkup(inline_keyboard=[])

    for m in page_movies:
        if (parts := m.split(" - ")) and len(parts) == 2:
            title, link = parts
            markup.inline_keyboard.append([InlineKeyboardButton(text=title.strip(), url=link.strip())])

    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish", "next": "➡ ", "prev": "⬅ "},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена", "next": "➡ ", "prev": "⬅ "},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel", "next": "➡ ", "prev": "⬅ "}
    }

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(
            text=buttons_text[language]["prev"],
            callback_data=f"genre_{genre_key}_page_{page - 1}"
        ))
    if end < len(movies):
        nav_buttons.append(InlineKeyboardButton(
            text=buttons_text[language]["next"],
            callback_data=f"genre_{genre_key}_page_{page + 1}"
        ))
    if nav_buttons:
        markup.inline_keyboard.append(nav_buttons)

    markup.inline_keyboard.append([
        InlineKeyboardButton(text=buttons_text[language]["back"], callback_data="category_movies"),
        InlineKeyboardButton(text=buttons_text[language]["cancel"], callback_data="cancel")
    ])

    messages = {
        "uz": f"🎬 Kino janri: {genre_key} (sahifa {page})",
        "ru": f"🎬 Фильмы в жанре {genre_key} (страница {page})",
        "en": f"🎬 Movies in the {genre_key} genre (page {page})"
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

    # Reklama yuborish
@dp.message(Command("reklama"))
async def reklama(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Sizda bu amalni bajarish huquqi yo‘q.")
        return

    if not message.text.split()[1:]:
        await message.answer("ℹ️ Reklama matnini yozing. Masalan: /reklama Yangilik!")
        return

    reklama_matni = " ".join(message.text.split()[1:])  # Reklama matnini ajratib olish
    user_ids = await get_all_user_ids()  # Bazadan foydalanuvchilarni olish
    count = 0

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=reklama_matni)
            count += 1
        except Exception as e:
            print(f"❌ {user_id} ga yuborilmadi: {e}")  # Xatolikni konsolga chiqarish
            continue

    await message.answer(f"✅ {count} ta foydalanuvchiga reklama yuborildi.")



async def main():
    await on_startup()

    dp.message.register(handle_feedback, F.state == FeedbackStates.waiting_for_feedback)

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())



