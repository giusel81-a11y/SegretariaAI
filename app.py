from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN
from memory import add_note, get_notes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao Giuseppe! 👋\n\n"
        "Sono la tua Segretaria AI.\n\n"
        "Comandi disponibili:\n"
        "/add attività\n"
        "/list\n"
        "/today"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Scrivi qualcosa dopo /add"
        )
        return

    add_note(text)

    await update.message.reply_text(
        f"✅ Attività salvata:\n{text}"
    )


async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = get_notes()

    if not notes:
        await update.message.reply_text(
            "Nessuna attività salvata."
        )
        return

    message = "📋 Attività:\n\n"

    for i, note in enumerate(notes, start=1):
        message += f"{i}. {note}\n"

    await update.message.reply_text(message)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = get_notes()

    if not notes:
        await update.message.reply_text(
            "Oggi non hai attività registrate."
        )
        return

    message = "🎯 Priorità di oggi:\n\n"

    for note in notes:
        message += f"• {note}\n"

    await update.message.reply_text(message)


import asyncio


async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_notes))
    app.add_handler(CommandHandler("today", today))

    print("Bot avviato...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
``
