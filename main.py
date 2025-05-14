from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
import os
from script import remove_character, divide_file_content

TOKEN = "TON_TOKEN_ICI"

user_files = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Envoie-moi un fichier .txt pour commencer.")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document
    if file.mime_type != "text/plain":
        update.message.reply_text("Merci d'envoyer un fichier .txt.")
        return

    file_path = f"{file.file_unique_id}.txt"
    file.get_file().download(file_path)
    user_files[update.message.chat_id] = file_path
    update.message.reply_text("Fichier reçu. Envoie /divide N pour diviser ou /remove C pour enlever un caractère.")

def divide(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in user_files:
        update.message.reply_text("Aucun fichier reçu.")
        return

    try:
        num_parts = int(context.args[0])
    except:
        update.message.reply_text("Utilisation : /divide 3")
        return

    with open(user_files[chat_id], encoding="utf-8") as f:
        content = f.read()

    parts = divide_file_content(content, num_parts)

    if isinstance(parts, list):
        for i, part in enumerate(parts):
            part_name = f"part_{i+1}.txt"
            with open(part_name, "w", encoding="utf-8") as pf:
                pf.write(part)
            update.message.reply_document(document=open(part_name, "rb"))
    else:
        update.message.reply_text("Erreur lors de la division.")

def remove(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in user_files:
        update.message.reply_text("Aucun fichier reçu.")
        return

    try:
        char_to_remove = context.args[0]
    except:
        update.message.reply_text("Utilisation : /remove X")
        return

    with open(user_files[chat_id], encoding="utf-8") as f:
        content = f.read()

    new_content = remove_character(content, char_to_remove)
    new_path = f"modified_{chat_id}.txt"
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    update.message.reply_document(document=open(new_path, "rb"))

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("divide", divide))
dp.add_handler(CommandHandler("remove", remove))
dp.add_handler(MessageHandler(Filters.document, handle_file))

updater.start_polling()
updater.idle()
