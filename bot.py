-import logging
 import json
+import logging
 import os
+from typing import Any, Dict, List
+
 from aiogram import Bot, Dispatcher, executor, types
 
 API_TOKEN = "8749841265:AAGqnsaVjsULD-FT8GqSv98Ipx5dFSf1Bkg"
-
+ADMIN_ID = 8519909049
 DATA_FILE = "user_data.json"
 
 logging.basicConfig(level=logging.INFO)
 
 bot = Bot(token=API_TOKEN)
 dp = Dispatcher(bot)
 
-# --- Хранение данных в файле ---
+QUESTIONNAIRE: List[Dict[str, str]] = [
+    {
+        "key": "name",
+        "prompt": "Как вас зовут?",
+    },
+    {
+        "key": "age",
+        "prompt": "Сколько вам лет?",
+    },
+    {
+        "key": "sex",
+        "prompt": "Ваш пол?",
+    },
+    {
+        "key": "height",
+        "prompt": "Какой у вас рост (см)?",
+    },
+    {
+        "key": "weight",
+        "prompt": "Какая у вас масса тела (кг)?",
+    },
+    {
+        "key": "goal",
+        "prompt": (
+            "Какая ваша главная цель на ближайшие 2–3 месяца?\n"
+            "(например: снижение веса, набор массы, поддержание, улучшение самочувствия)"
+        ),
+    },
+    {
+        "key": "activity",
+        "prompt": (
+            "Какой у вас уровень активности?\n"
+            "(сидячая работа, 1–2 тренировки/неделя, 3–5, ежедневно)"
+        ),
+    },
+    {
+        "key": "training",
+        "prompt": "Какие у вас тренировки и как часто вы тренируетесь?",
+    },
+    {
+        "key": "schedule",
+        "prompt": "Как обычно проходит ваш день и в какие часы вам удобно есть?",
+    },
+    {
+        "key": "medical",
+        "prompt": (
+            "Есть ли диагнозы, заболевания ЖКТ, щитовидки, диабет, приём лекарств "
+            "или другие важные медицинские особенности?"
+        ),
+    },
+    {
+        "key": "allergies",
+        "prompt": "Есть ли аллергии или непереносимости? Перечислите.",
+    },
+    {
+        "key": "food_preferences",
+        "prompt": "Какие продукты вы любите, а какие не едите (религиозные, этические, вкусовые причины)?",
+    },
+    {
+        "key": "bad_habits",
+        "prompt": "Есть ли вредные привычки (алкоголь, курение, сладкое на ночь, переедание)?",
+    },
+    {
+        "key": "water_sleep",
+        "prompt": "Сколько в среднем пьёте воды и сколько спите?",
+    },
+    {
+        "key": "budget",
+        "prompt": "Есть ли бюджет или ограничения по времени на готовку?",
+    },
+    {
+        "key": "readiness",
+        "prompt": "Насколько вы готовы соблюдать план по шкале от 1 до 10? Что может помешать?",
+    },
+]
+
 
-def load_data():
+# --- Хранение данных в файле ---
+def load_data() -> Dict[str, Dict[str, Any]]:
     if os.path.exists(DATA_FILE):
         with open(DATA_FILE, "r", encoding="utf-8") as f:
             return json.load(f)
     return {}
 
-def save_data(data):
+
+def save_data(data: Dict[str, Dict[str, Any]]) -> None:
     with open(DATA_FILE, "w", encoding="utf-8") as f:
         json.dump(data, f, ensure_ascii=False, indent=4)
 
+
 user_data = load_data()
 
-# --- Команда /start ---
 
+def get_next_question_key(data: Dict[str, Any]) -> str:
+    for item in QUESTIONNAIRE:
+        if item["key"] not in data:
+            return item["key"]
+    return ""
+
+
+def get_prompt_by_key(key: str) -> str:
+    for item in QUESTIONNAIRE:
+        if item["key"] == key:
+            return item["prompt"]
+    return ""
+
+
+def format_user_card(uid: str, info: Dict[str, Any]) -> str:
+    lines = [f"🗂 Карточка пользователя {uid}"]
+    for item in QUESTIONNAIRE:
+        key = item["key"]
+        title = key.replace("_", " ").capitalize()
+        value = info.get(key, "—")
+        lines.append(f"• {title}: {value}")
+    return "\n".join(lines)
+
+
+# --- Команда /start ---
 @dp.message_handler(commands=["start"])
 async def cmd_start(message: types.Message):
-    user_data[str(message.from_user.id)] = {}
+    uid = str(message.from_user.id)
+    user_data[uid] = {"step": 0}
     save_data(user_data)
 
     await message.answer(
-        "👋 Вас приветствует Бот спорт комплекса Шериф!\n\n"
-        "Вместе с нами мы поможем вам достичь тело вашей мечты\n"
-        "и получить здоровое долголетие.\n\n"
-        "Анализ ваших данных будет проведён.\n"
-        "Давайте начнём. Как вас зовут?"
+        "👋 Привет! Я помогу собрать полную анкету для персонального плана питания.\n\n"
+        "Я задам ключевые вопросы про цели, здоровье, режим и пищевые привычки.\n"
+        "Это займёт 5–10 минут и сильно повысит точность рекомендаций.\n\n"
+        f"Начнём ✨\n\n{QUESTIONNAIRE[0]['prompt']}"
     )
 
-# --- Обработка сообщений ---
 
-@dp.message_handler()
-async def handle_message(message: types.Message):
+@dp.message_handler(commands=["status"])
+async def cmd_status(message: types.Message):
     uid = str(message.from_user.id)
-    data = user_data.setdefault(uid, {})
-
-    # --- 1) имя ---
-    if "name" not in data:
-        data["name"] = message.text
-        save_data(user_data)
-        await message.answer(f"Приятно познакомиться, {data['name']}!\n\nСколько вам лет?")
+    data = user_data.get(uid)
+    if not data:
+        await message.answer("Анкета ещё не начата. Нажмите /start")
         return
 
-    # --- 2) возраст ---
-    if "age" not in data:
-        data["age"] = message.text
-        save_data(user_data)
-        await message.answer("Понял. Какая у вас масса тела (в кг)?")
-        return
+    answered = sum(1 for q in QUESTIONNAIRE if q["key"] in data)
+    total = len(QUESTIONNAIRE)
+    await message.answer(f"Ваш прогресс: {answered}/{total}. Продолжайте отвечать в этом чате 💬")
 
-    # --- 3) масса ---
-    if "weight" not in data:
-        data["weight"] = message.text
-        save_data(user_data)
-        await message.answer("Хорошо. Какой у вас рост (в см)?")
-        return
 
-    # --- 4) рост ---
-    if "height" not in data:
-        data["height"] = message.text
-        save_data(user_data)
-        await message.answer(
-            "Отлично. Какова ваша основная цель?\n"
-            "👉 похудение\n"
-            "👉 набор массы\n"
-            "👉 поддержание формы"
-        )
+# --- Админ-доступ и просмотр данных ---
+@dp.message_handler(commands=["data"])
+async def cmd_data(message: types.Message):
+    if message.from_user.id != ADMIN_ID:
+        await message.answer("У вас нет доступа.")
         return
 
-    # --- 5) цель ---
-    if "goal" not in data:
-        data["goal"] = message.text
-        save_data(user_data)
-        await message.answer(
-            "Супер. Теперь расскажите о предпочтениях в мясе:\n"
-            "🥩 говядина\n"
-            "🍗 курица\n"
-            "🐟 рыба\n"
-            "или что-то ещё?"
-        )
+    data = load_data()
+    if not data:
+        await message.answer("Данных пока нет.")
         return
 
-    # --- 6) предпочтения ---
-    if "preferences" not in data:
-        data["preferences"] = message.text
-        save_data(user_data)
-        await message.answer("Есть ли у вас аллергии? Если да — перечислите их.")
+    lines = ["📊 Анкеты пользователей:"]
+    for uid, info in data.items():
+        answered = sum(1 for q in QUESTIONNAIRE if q["key"] in info)
+        lines.append(f"• ID {uid}: заполнено {answered}/{len(QUESTIONNAIRE)}")
+
+    lines.append("\nЧтобы открыть карточку: /user <id>")
+    await message.answer("\n".join(lines))
+
+
+@dp.message_handler(commands=["user"])
+async def cmd_user(message: types.Message):
+    if message.from_user.id != ADMIN_ID:
+        await message.answer("У вас нет доступа.")
         return
 
-    # --- 7) аллергии ---
-    if "allergies" not in data:
-        data["allergies"] = message.text
-        save_data(user_data)
+    target_uid = message.get_args().strip()
+    if not target_uid:
+        await message.answer("Используйте формат: /user <id>")
+        return
 
-        await message.answer(
-            "Спасибо за информацию! 🙌\n\n"
-            "Мы обработаем данные и подготовим персональный план питания.\n"
-            "В течение некоторого времени файл с планом будет отправлен вам.\n\n"
-            "Если хотите начать заново — /start"
-        )
+    data = load_data()
+    info = data.get(target_uid)
+    if not info:
+        await message.answer("Пользователь не найден.")
         return
 
-    # если пользователь пишет дальше
-    await message.answer("Данные уже собраны. Если хотите начать заново — /start")
+    await message.answer(format_user_card(target_uid, info))
 
 
-if __name__ == "__main__":
-    executor.start_polling(dp, skip_updates=True)
-# --- Админ-доступ и просмотр данных ---
+# --- Обработка сообщений ---
+@dp.message_handler()
+async def handle_message(message: types.Message):
+    uid = str(message.from_user.id)
+    data = user_data.get(uid)
 
-ADMIN_ID = 8519909049
+    if not data:
+        await message.answer("Чтобы начать анкету, нажмите /start")
+        return
 
-@dp.message_handler(commands=["data"])
-async def cmd_data(message: types.Message):
-    # Проверяем, что это админ
-    if message.from_user.id != ADMIN_ID:
-        await message.answer("У вас нет доступа.")
+    next_key = get_next_question_key(data)
+    if not next_key:
+        await message.answer(
+            "Спасибо! Вся нужная информация уже собрана ✅\n"
+            "Я передал(а) анкету специалисту. Если хотите заполнить заново — /start"
+        )
         return
 
-    data = load_data()
+    data[next_key] = message.text.strip()
+    save_data(user_data)
 
-    if not data:
-        await message.answer("Данных пока нет.")
+    next_key = get_next_question_key(data)
+    if not next_key:
+        await message.answer(
+            "Отличная работа, анкета полностью заполнена 🙌\n\n"
+            "На основе ответов можно составить персональный план питания.\n"
+            "Если захотите обновить данные позже — /start"
+        )
         return
 
-    # Формируем текст для вывода
-    text = "📊 Анкеты пользователей:\n\n"
-    for uid, info in data.items():
-        text += f"ID: {uid}\n"
-        for k, v in info.items():
-            text += f"{k}: {v}\n"
-        text += "\n---\n\n"
+    await message.answer(
+        "Принято 👍\n"
+        f"{get_prompt_by_key(next_key)}"
+    )
+
 
-    await message.answer(text or "Нет данных.")
+if __name__ == "__main__":
+    executor.start_polling(dp, skip_updates=True)
