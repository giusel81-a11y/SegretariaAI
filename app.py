from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN

from memory import (2    add_note,3    get_notes,4    complete_note,5    delete_note,6    get_active_notes,7    reset_notes8)

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

   
