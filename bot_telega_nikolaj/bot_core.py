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
    update.message.reply_text(f'Hello, {user.first_name}! Send me an image and I will forward it to another group.')


def handle_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1].file_id
    caption = update.message.caption

    # Send the photo to the target group
    context.bot.send_photo(chat_id=TARGET_GROUP_ID, photo=photo, caption=caption)

    update.message.reply_text('Photo has been forwarded to the group!')


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


