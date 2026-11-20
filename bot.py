
import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))
HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")

REGIONS = {
    "01": "Республика Адыгея",
    "02": "Республика Башкортостан",
    "05": "Республика Дагестан",
    "06": "Республика Ингушетия",
    "07": "Кабардино-Балкарская Республика",
    "09": "Карачаево-Черкесская Республика",
    "15": "Республика Северная Осетия — Алания",
    "16": "Республика Татарстан",
    "20": "Чеченская Республика",
    "23": "Краснодарский край",
    "26": "Ставропольский край",
    "50": "Московская область",
    "61": "Ростовская область",
    "77": "Москва",
    "78": "Санкт-Петербург",
    "93": "Краснодарский край",
    "95": "Чеченская Республика",
    "123": "Краснодарский край",
    "177": "Москва",
    "199": "Москва",
    "777": "Москва",
}

LETTERS = "АВЕКМНОРСТУХ"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "DOMINION запущен.\n\n"
        "Отправь российский госномер автомобиля.\n"
        "Например: А123ВС05"
    )


async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.upper().replace(" ", "").replace("-", "")

    pattern = rf"^[{LETTERS}]\d{{3}}[{LETTERS}]{{2}}\d{{2,3}}$"

    if not re.fullmatch(pattern, number):
        await update.message.reply_text(
            "Неверный формат номера.\n"
            "Пример правильного формата: А123ВС05"
        )
        return

    region = number[-2:] if len(number) == 8 else number[-3:]

    # Для трёхзначных кодов сначала проверяем полный код.
    region_name = REGIONS.get(region)

    if not region_name and len(region) == 3:
        region_name = REGIONS.get(region[-2:])

    if region_name:
        result = region_name
    else:
        result = "Регион пока отсутствует в справочнике."

    await update.message.reply_text(
        f"DOMINION\n\n"
        f"Номер: {number}\n"
        f"Регион: {result}\n\n"
        f"Марка и модель: пока не определяются."
    )


def main():
    if not BOT_TOKEN or not HOST:
        raise RuntimeError("Не заданы BOT_TOKEN или RENDER_EXTERNAL_HOSTNAME")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number)
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=f"https://{HOST}/telegram",
    )


if __name__ == "__main__":
    main()
