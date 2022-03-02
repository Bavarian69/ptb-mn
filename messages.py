from telegram import Update
from telegram.ext import CallbackContext

from config import GROUP_MAIN


def add_footer_meme(update: Update, context: CallbackContext):
    print(update)

    original_caption = update.channel_post.caption if update.channel_post.caption is not None else ''

    update.channel_post.edit_caption(f"{original_caption}\n\n🔰 Subscribe to @MilitaerMemes for more!")

    update.channel_post.forward(chat_id=GROUP_MAIN)


def flag_to_hashtag(update: Update, context: CallbackContext):
    print(update.message.text.find(r"(#+[a-zA-Z0-9(_)]{1,})"))
