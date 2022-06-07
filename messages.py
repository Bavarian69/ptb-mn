import re

from deep_translator import GoogleTranslator
from telegram import Update, InputMediaVideo, InputMediaPhoto, InputMedia, InputMediaAnimation  #upm package(python-telegram-bot)
from telegram.ext import CallbackContext  #upm package(python-telegram-bot)
from lang import languages
import config
from typing import Union

from flag import flags


def flag_to_hashtag_test(update: Update, context: CallbackContext):
    update.message.reply_text(flag_to_hashtag(update.message.text, "tr"))


def flag_to_hashtag(text: str, language: Union[str, None] = None) -> str:

    if not re.compile(r'#\w+').search(text):

        last = None

        text += "\n\n"

        for c in text:

            if not is_flag_emoji(c):
                continue

            if last is None:
                last = c
                continue

            key = last + c

            if key in flags:

                hashtag = flags.get(key)

                if language is not None:
                    hashtag = GoogleTranslator(
                        source='de', target=language).translate(hashtag)

                text += "#" + hashtag.replace(" ", "") + " "

            last = None

    return text


def translate_message(target_lang: str, text: str) -> str:
    translated_text = GoogleTranslator(source='de',
                                       target=target_lang).translate(text)

    return flag_to_hashtag(translated_text, target_lang)


def post_channel_english(update: Update, context: CallbackContext):
    if update.channel_post.media_group_id is None:
        original_post = update.channel_post
        original_caption = update.channel_post.caption_html_urled if update.channel_post.caption is not None else ''

        for lang in languages:
            original_post.copy(
                chat_id=lang.channel_id,
                caption=translate_message(lang.lang_key, original_caption) +
                "\n" + lang.footer)

        update.channel_post.edit_caption(
            flag_to_hashtag(original_caption) +
            "\n🔰 Abonnieren Sie @MilitaerNews\n🔰 Tritt uns bei @MNChat")
        return

    if update.channel_post.media_group_id in context.bot_data:
        for job in context.job_queue.get_jobs_by_name(
                update.channel_post.media_group_id):
            job.schedule_removal()
        print("--- job gone ::::::::")
    else:
        print("--- NEW MG ------------------------")
        context.bot_data[update.channel_post.media_group_id] = []

    if update.channel_post.photo:
        context.bot_data[update.channel_post.media_group_id].append(
            InputMediaPhoto(media=update.channel_post.photo[-1].file_id))
        print(
            "--- PHOTO ----------------------------------------------------------------"
        )
    elif update.channel_post.video:
        context.bot_data[update.channel_post.media_group_id].append(
            InputMediaVideo(media=update.channel_post.video.file_id))

    elif update.channel_post.animation:
        context.bot_data[update.channel_post.media_group_id].append(
            InputMediaAnimation(media=update.channel_post.animation.file_id))

    if update.channel_post.caption is not None:
        print("trans---SINGLE ::: ",
              translate_message("en", update.channel_post.caption))

        context.bot_data[update.channel_post.media_group_id][
            -1].caption = f"{update.channel_post.caption_html_urled}"

        update.channel_post.edit_caption(
            flag_to_hashtag(update.channel_post.caption_html_urled, "de") +
            "\n🔰 Abonnieren Sie @MilitaerNews\n🔰 Tritt uns bei @MNChat")

    context.job_queue.run_once(share_in_other_channels, 20,
                               update.channel_post.media_group_id,
                               str(update.channel_post.media_group_id))


def breaking_news(update: Update, context: CallbackContext):
    update.channel_post.delete()
    context.bot.send_photo(
        chat_id=config.CHANNEL_DE,
        photo=open("res/breaking/mn-breaking-de.png", "rb"),
        caption=flag_to_hashtag(update.text_html_urled) +
        "\n🔰 Abonnieren Sie @MilitaerNews\n🔰 Tritt uns bei @MNChat")

    text = re.sub(re.compile(r"#eilmeldung", re.IGNORECASE), "",
                  update.channel_post.text_html_urled)

    for lang in languages:
        context.bot.send_photo(
            chat_id=lang.channel_id,
            photo=open(f"res/breaking/mn-breaking-{lang.lang_key}.png", "rb"),
            caption="#" + lang.breaking + "\n\n" +
            translate_message(lang.lang_key, text) + "\n" + lang.footer)


def announcement(update: Update, context: CallbackContext):
    update.channel_post.delete()

    text = " 📢\n\n" + re.sub(re.compile(r"#eilmeldung", re.IGNORECASE), "",
                             update.channel_post.text_html)

    msg_de = context.bot.send_photo(chat_id=config.CHANNEL_DE,
                                    photo=open(
                                        "res/announce/mn-announce-de.png",
                                        "rb"),
                                    caption="#MITTEILUNG" + text)
    msg_de.pin()

    for lang in languages:
        msg = context.bot.send_photo(
            chat_id=lang.channel_id,
            photo=open(f"res/announce/mn-announce-{lang.lang_key}.png", "rb"),
            caption="#" + lang.announce +
            translate_message(lang.lang_key, text) + "\n" + lang.footer)
        msg.pin()


def is_flag_emoji(c):
    return "🇦" <= c <= "🇿" or c in ["🏴"]


def share_in_other_channels(context: CallbackContext):
    files: [InputMedia] = []

    print("JOB ::::::::::::: ", context.job.context)
    print("bot-data :::::::::::::::::::::::::::",
          context.bot_data[context.job.context])

    for file in context.bot_data[context.job.context]:
        print(file)
        files.append(file)

    original_caption = files[0].caption

    for lang in languages:

        files[0].caption = translate_message(
            lang.lang_key, original_caption) + "\n" + lang.footer
        context.bot.send_media_group(chat_id=lang.channel_id, media=files)

    print("-- done --")

    del context.bot_data[context.job.context]
