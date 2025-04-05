from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
import database




bot = Bot('7383378706:AAEHT3fKEW7DT3AsV5JsqMxH5S00bzPaFZs')
dp = Dispatcher(bot)

user_languages = {}

async def on_startup(dp):
    await database.setup_database()




@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # Inline Keyboard
    inline_markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("O'zbek🇺🇿", callback_data="uz")
    btn2 = InlineKeyboardButton("Русский🇷🇺", callback_data="ru")
    btn3 = InlineKeyboardButton("English🇺🇸", callback_data="en")
    inline_markup.add(btn1)
    inline_markup.add(btn2, btn3)
    
    await message.answer("Iltimos tilni tanlang: \n Выберите язык: \n Please choose your language:", reply_markup=inline_markup)
    
    # Reply Keyboard
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_start = KeyboardButton("/start")
    btn_series = KeyboardButton("/serial")
    btn_movie = KeyboardButton("/kino")
    reply_markup.add(btn_start, btn_series, btn_movie)
    
    await message.answer("@TvMoonuz_bot", reply_markup=reply_markup)




 
@dp.callback_query_handler(lambda call: call.data in ["uz", "ru", "en"])
async def handle_language_selection(call: types.CallbackQuery):
    user_languages[call.from_user.id] = call.data  # Foydalanuvchi tilini saqlash
    await show_main_menu(call)

async def show_main_menu(call: types.CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    markup = InlineKeyboardMarkup()
    btn_movies = InlineKeyboardButton("🎬 Kino", callback_data="category_movies")
    btn_series = InlineKeyboardButton("📺 Serial", callback_data="category_series")
    markup.add(btn_movies, btn_series)

    messages = {
        "uz": "Nimani ko‘rmoqchisiz?",
        "ru": "Что вы хотите посмотреть?",
        "en": "What would you like to watch?"
        
    }
    
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messages[language], reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data == "category_series")
async def show_series_selection(call: types.CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    genres = await database.get_series_genres(language)
    markup = InlineKeyboardMarkup()
    for genre_key, genre_name in genres.items():
        markup.add(InlineKeyboardButton(genre_name, callback_data=f"series_{genre_key}"))
    messages = {
        "uz": "Serial janrini tanlang:",
        "ru": "Выберите жанр сериала:",
        "en": "Choose a series genre:"
               
    }
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messages[language], reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data.startswith("series_"))
async def handle_series_selection(call: types.CallbackQuery):
    genre_key = call.data.split("_")[1]
    language = user_languages.get(call.from_user.id, "uz")
    series = await database.get_series_by_genre(language, genre_key)

     # Kinolar bo'lmasa, foydalanuvchiga tilga mos xabarni yuborish
    if not series:
        # Tilga mos xabarlar
        messages = {
            "uz": "Bu janrda serillar yo‘q.",
            "ru": "В этом жанре нет сериала.",
            "en": "No series found in this genre."
        }
        
        await bot.answer_callback_query(call.id, messages[language], show_alert=True)
        return  

    markup = InlineKeyboardMarkup()

    unique_series = set(series)

    for series in unique_series:
        parts = series.split(" - ")  # Kino nomi va URL orasida `-` bor deb faraz qilamiz
        if len(parts) == 2:
            title, link = parts
            markup.add(InlineKeyboardButton(title.strip(), url=link.strip()))


  # Har bir til uchun tugmalar matni
    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish"},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена"},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel"}
    }

    # Foydalanuvchining tiliga mos tugmalarni yaratamiz
    btn1 = InlineKeyboardButton(buttons_text[language]["back"], callback_data="category_series")
    btn2 = InlineKeyboardButton(buttons_text[language]["cancel"], callback_data="cancel")

    # Tugmalarni markup-ga qo‘shamiz
    markup.row(btn1, btn2)
    

    messages = {
        "uz": "Mavjud seriallar:",
        "ru": "Доступные сериалы:",
        "en": "Available series:"
        
    }
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messages[language], reply_markup=markup)




@dp.callback_query_handler(lambda call: call.data == "category_movies")
async def show_genre_selection(call: types.CallbackQuery):
    language = user_languages.get(call.from_user.id, "uz")
    genres = await database.get_movie_genres(language)
    markup = InlineKeyboardMarkup()
    for genre_key, genre_name in genres.items():
        markup.add(InlineKeyboardButton(genre_name, callback_data=f"genre_{genre_key}"))

    messages = {
        "uz": "Kino janrini tanlang:",
        "ru": "Выберите жанр фильма:",
        "en": "Choose a movie genre:"
             
    }
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messages[language], reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data.startswith("genre_"))
async def handle_genre_selection(call: types.CallbackQuery):
    genre_key = call.data.split("_")[1]
    language = user_languages.get(call.from_user.id, "uz")

    movies = await database.get_movies_by_genre(language, genre_key)
    
    # Kinolar bo'lmasa, foydalanuvchiga tilga mos xabarni yuborish
    if not movies:
        # Tilga mos xabarlar
        messages = {
            "uz": "Bu janrda kinolar yo‘q.",
            "ru": "В этом жанре нет фильмов.",
            "en": "No movies found in this genre."
        }
        
        await bot.answer_callback_query(call.id, messages[language], show_alert=True)
        return  

    markup = InlineKeyboardMarkup()
    
    unique_movies = set(movies)  # Takrorlanishni oldini olish
    
    for movie in unique_movies:
        parts = movie.split(" - ")  # Kino nomi va URL orasida `-` bor deb faraz qilamiz
        if len(parts) == 2:
            title, link = parts
            markup.add(InlineKeyboardButton(title.strip(), url=link.strip()))

    # Har bir til uchun tugmalar matni
    buttons_text = {
        "uz": {"back": "⬅ Orqaga", "cancel": "❌ Bekor qilish"},
        "ru": {"back": "⬅ Назад", "cancel": "❌ Отмена"},
        "en": {"back": "⬅ Back", "cancel": "❌ Cancel"}
    }

    # Foydalanuvchining tiliga mos tugmalarni yaratamiz
    btn1 = InlineKeyboardButton(buttons_text[language]["back"], callback_data="category_movies")
    btn2 = InlineKeyboardButton(buttons_text[language]["cancel"], callback_data="cancel")

    # Tugmalarni markup-ga qo‘shamiz
    markup.row(btn1, btn2)

    # Har bir til uchun janr xabari
    messages = {
        "uz": f"🎬 Kino janri: {genre_key}",
        "ru": f"🎬 Фильмы в жанре {genre_key}",
        "en": f"🎬 Movies in the {genre_key} genre"
    }

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=messages.get(language, messages["uz"]),
        reply_markup=markup
    )


@dp.message_handler(commands=['clear'])
async def clear_messages(message: types.Message):
    for i in range(message.message_id, message.message_id - 3, -1):
        try:
            await bot.delete_message(message.chat.id, i)
        except Exception:
            continue
    
 
@dp.message_handler(commands=['search'])
async def search_movie(message: types.Message):
    query = message.text.replace('/search', '').strip().lower()

    if not query:
        language = user_languages.get(message.from_user.id, "uz")
        messages = {
            "uz": "🔎 Iltimos, qidirayotgan kino yoki serial nomini kiriting.\n\n Masalan: /search Titanik",
            "ru": "🔎 Пожалуйста, введите название фильма или сериала.\n\n например: /search Титаник ",
            "en": "🔎 Please enter the name of the movie or series.\n\n For example: /search Titanic"
        }
        await message.answer(messages[language])
        return

    language = user_languages.get(message.from_user.id, "uz")
    results = await database.search_movies_and_series(language, query)

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
     
@dp.message_handler(commands=['kino'])
async def movie(message: types.Message):
    language = user_languages.get(message.from_user.id, "uz")
    movie_genres = await database.get_movie_genres(language)  # Barcha janrlarni olish

    markup = InlineKeyboardMarkup()
    for genre_key, genre_name in movie_genres.items():
        markup.add(InlineKeyboardButton(genre_name, callback_data=f"genre_{genre_key}"))

    messages = {
        "uz": "Kino janrini tanlang:",
        "ru": "Выберите жанр фильма:",
        "en": "Choose a movie genre:"

    }
    await message.answer(messages.get(language, "Choose a movie genre:"), reply_markup=markup)


@dp.message_handler(commands=['serial'])
async def series(message: types.Message):
    # Foydalanuvchi tilini aniqlash
    language = user_languages.get(message.from_user.id, "uz")
    series_genres = await database.get_series_genres(language)

    # Inline tugmalarini yaratish
    markup = types.InlineKeyboardMarkup()
    for genre_key, genre_name in series_genres.items():
     # Serial nomlarini olish
        markup.add(types.InlineKeyboardButton(genre_name, callback_data=f"series_{genre_key}"))

    messages = {
        "uz": "serial janrini tanlang:",
        "ru": "Выберите жанр фильма:",
        "en": "Choose a series genre:"
    }
    await message.answer(messages.get(language, "Choose a series genre:"), reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "cancel")
async def cancel_handler(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)  # Xabarni o‘chirish
 

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    language = user_languages.get(message.from_user.id, "uz")
    messages = {
        "uz": "/start - Botni yangilaydi\n/movie - Kinolar janrini chiqaradi\n/series - Serial janrlarini chiqaradi\n/search <nom> - Kino yoki serialni topadi\n/clear - Oxirgi xabarlarni o‘chiradi",
        "ru": "/start - Обновляет бота\n/movie - Показывает жанры фильмов\n/series - Показывает жанры сериалов\n/search <name> - Находит фильм или сериал\n/clear - Очищает последние сообщения",
        "en": "/start - Updates bot\n/movie - Shows movie genres\n/series - Shows series genres\n/search <name> - Finds a movie or series\n/clear - Clears recent messages"
        
    }
    await message.answer(messages[language])



              

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)