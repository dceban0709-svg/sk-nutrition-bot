import logging
import json
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "8749841265:AAE5rTjLly5NqSa7ee0AeaOSwT31L1UdWDc"

DATA_FILE = "user_data.json"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Хранение данных в файле ---

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

user_data = load_data()

# --- Команда /start ---

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user_data[str(message.from_user.id)] = {}
    save_data(user_data)

    await message.answer(
        "👋 Вас приветствует Бот спорт комплекса Шериф!\n\n"
        "Вместе с нами мы поможем вам достичь тело вашей мечты\n"
        "и получить здоровое долголетие.\n\n"
        "Анализ ваших данных будет проведён.\n"
        "Давайте начнём. Как вас зовут?"
    )

# --- Обработка сообщений ---

@dp.message_handler()
async def handle_message(message: types.Message):
    uid = str(message.from_user.id)
    data = user_data.setdefault(uid, {})

    # --- 1) имя ---
    if "name" not in data:
        data["name"] = message.text
        save_data(user_data)
        await message.answer(f"Приятно познакомиться, {data['name']}!\n\nСколько вам лет?")
        return

    # --- 2) возраст ---
    if "age" not in data:
        data["age"] = message.text
        save_data(user_data)
        await message.answer("Понял. Какая у вас масса тела (в кг)?")
        return

    # --- 3) масса ---
    if "weight" not in data:
        data["weight"] = message.text
        save_data(user_data)
        await message.answer("Хорошо. Какой у вас рост (в см)?")
        return

    # --- 4) рост ---
    if "height" not in data:
        data["height"] = message.text
        save_data(user_data)
        await message.answer(
            "Отлично. Какова ваша основная цель?\n"
            "👉 похудение\n"
            "👉 набор массы\n"
            "👉 поддержание формы"
        )
        return

    # --- 5) цель ---
    if "goal" not in data:
        data["goal"] = message.text
        save_data(user_data)
        await message.answer(
            "Супер. Теперь расскажите о предпочтениях в мясе:\n"
            "🥩 говядина\n"
            "🍗 курица\n"
            "🐟 рыба\n"
            "или что-то ещё?"
        )
        return

    # --- 6) предпочтения ---
    if "preferences" not in data:
        data["preferences"] = message.text
        save_data(user_data)
        await message.answer("Есть ли у вас аллергии? Если да — перечислите их.")
        return

    # --- 7) аллергии ---
    if "allergies" not in data:
        data["allergies"] = message.text
        save_data(user_data)

        await message.answer(
            "Спасибо за информацию! 🙌\n\n"
            "Мы обработаем данные и подготовим персональный план питания.\n"
            "В течение некоторого времени файл с планом будет отправлен вам.\n\n"
            "Если хотите начать заново — /start"
        )
        return

    # если пользователь пишет дальше
    await message.answer("Данные уже собраны. Если хотите начать заново — /start")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
