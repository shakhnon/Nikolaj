from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TARGET_GROUP_ID = os.getenv('TARGET_GROUP_ID')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f'👋 Hello, {user.first_name}!\n'
        f'Send me a photo and I will forward it to the target group.\n'
        f'Use /help to see all available commands.'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "📋 Available commands:\n"
        "/start — start interacting with the bot\n"
        "/help — show this help message\n"
        "/status — check if the bot is running\n"
        "/setgroup <group_id> — change the target group (admin only)\n"
        "/info — show your user information\n"
    )


def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("✅ The bot is online and ready to forward photos!")


def setgroup(update: Update, context: CallbackContext) -> None:
    global TARGET_GROUP_ID

    admin_id = os.getenv('ADMIN_ID')
    user_id = str(update.effective_user.id)

    if user_id != admin_id:
        update.message.reply_text("🚫 You don't have permission to change the target group.")
        return

    if len(context.args) != 1:
        update.message.reply_text("⚠️ Use the command like this: /setgroup <group_id>")
        return

    TARGET_GROUP_ID = context.args[0]
    update.message.reply_text(f"✅ Target group updated: {TARGET_GROUP_ID}")


def info(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f"👤 User info:\n"
        f"Name: {user.first_name}\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username if user.username else 'not set'}"
    )


def handle_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1].file_id
    caption = update.message.caption

    try:
        context.bot.send_photo(chat_id=TARGET_GROUP_ID, photo=photo, caption=caption)
        update.message.reply_text('📤 Photo has been successfully forwarded to the group!')
    except Exception as e:
        update.message.reply_text(f"❌ Failed to forward the photo: {e}")


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("setgroup", setgroup))
    dispatcher.add_handler(CommandHandler("info", info))

    # Photo handler
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
