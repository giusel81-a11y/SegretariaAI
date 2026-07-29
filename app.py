from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN

from memory import (
    add_note,
    get_notes,
    complete_note,
    delete_note,
    get_active_notes
)

import asyncio


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao Giuseppe! 👋\n\n"
        "Sono la tua Segretaria AI.\n\n"
        "Comandi disponibili:\n"
        "/add attività\n"
        "/list\n"
        "/today\n"
        "/done ID\n"
        "/delete ID"
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

    notes = get_active_notes()

    if not notes:
        await update.message.reply_text(
            "Nessuna attività aperta."
        )
        return

    message = "📋 Attività aperte:\n\n"

    for note_id, text in notes:
        message += f"{note_id}. {text}\n"

    await update.message.reply_text(message)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    notes = get_active_notes()

    if not notes:
        await update.message.reply_text(
            "Oggi non hai attività registrate."
        )
        return

    message = "🎯 Priorità di oggi:\n\n"

    for note_id, text in notes:
        message += f"• {text}\n"

    await update.message.reply_text(message)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Uso: /done ID"
        )
        return

    try:
        note_id = int(context.args[0])

        complete_note(note_id)

        await update.message.reply_text(
            f"✅ Attività {note_id} completata"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Errore: {str(e)}"
        )


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Uso: /delete ID"
        )
        return

    try:
        note_id = int(context.args[0])

        delete_note(note_id)

        await update.message.reply_text(
            f"🗑️ Attività {note_id} eliminata"
        )

    except Exception as e:
        await update.message.reply_text(
            f"Errore: {str(e)}"
        )


async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_notes))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("delete", delete))

    print("Bot avviato...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
