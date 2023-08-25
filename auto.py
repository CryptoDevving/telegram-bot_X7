import os
import csv
import random
import time as t

import sentry_sdk
from telegram import *
from telegram.ext import *

from api import index as api
from media import index as media
from data import url, text


sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)


current_button_data = None
users_clicked_current_button = set()
clicked_buttons = set()
first_user_clicked = False
first_user_info = ""
click_counts = {}


async def auto_message_click(context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_button_data, first_user_clicked
    first_user_clicked = False
    if context.bot_data is None:
        context.bot_data = {}
    current_button_data = str(random.randint(1, 100000000))
    context.bot_data["current_button_data"] = current_button_data
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Me!", callback_data=current_button_data)]]
    )
    await context.bot.send_photo(
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        reply_markup=keyboard,
    )
    users_clicked_current_button.clear()
    button_generation_timestamp = t.time()
    context.bot_data["button_generation_timestamp"] = button_generation_timestamp


async def auto_message_endorsement(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    photo_url = f"{url.pioneers}{api.get_random_pioneer_number()}.png"
    caption_text = f"*X7 Finance Xchange Pairs*\n\n{text.endorse}"
    keyboard_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Xchange Alerts", url=f"{url.tg_alerts}")]]
    )
    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=photo_url,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=keyboard_markup,
    )


async def auto_message_volume(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    photo_url = f"{url.pioneers}{api.get_random_pioneer_number()}.png"
    caption_text = f"*Boosting Trading Volume on Xchange*\n\n{text.referral}"
    keyboard_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Add Liquiidty Now", url=f"https://app.x7.finance/#/pool/v2")]]
    )
    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=photo_url,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=keyboard_markup,
    )


def clicks_get():
    click_counts = {}
    try:
        with open("logs/clicks.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                user, clicks = row
                click_counts[user] = int(clicks)
    except FileNotFoundError:
        pass
    return click_counts


def clicks_get_total():
    total_count = 0
    try:
        with open("logs/clicks.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                user, clicks = row
                total_count += int(clicks)
    except FileNotFoundError:
        pass
    return total_count


def get_user_click_total(username):
    click_counts = clicks_get()
    return click_counts.get(username, 0)


def clicks_save(click_counts):
    existing_clicks = clicks_get()
    for user, clicks in click_counts.items():
        if user in existing_clicks:
            existing_clicks[user] += clicks
        else:
            existing_clicks[user] = clicks

    with open("logs/clicks.csv", mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["User", "Clicks"])
        for user, clicks in existing_clicks.items():
            csv_writer.writerow([user, clicks])
    try:
        api.push_github("logs/clicks.csv", "auto: update clicks log")
    except Exception as e:
        sentry_sdk.capture_exception(f"GitHub Push error: {e}")
            

async def replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"{update.effective_message.text}"
    lower_message = message.lower()
    keyword_to_response = {
        "rob the bank": {"text": text.rob, "mode": "Markdown"},
        "delay": {"text": text.delay, "mode": "Markdown"},
        "patience": {"text": text.patience, "mode": "Markdown"},
        "https://twitter": {
            "text": random.choice(text.x_replies),
            "mode": None,
        },
        "https://x.com": {
            "text": random.choice(text.x_replies),
            "mode": None,
        },
        "gm": {"sticker": media.gm},
        "new on chain message": {"sticker": media.onchain},
        "lfg": {"sticker": media.lfg},
        "goat": {"sticker": media.goat},
        "smashed": {"sticker": media.smashed},
        "wagmi": {"sticker": media.wagmi},
        "slapped": {"sticker": media.slapped},
    }

    for keyword, response in keyword_to_response.items():
        target_message = message if "https://" in keyword else lower_message

        if keyword in target_message:
            if "text" in response:
                await update.message.reply_text(
                    text=response["text"], parse_mode=response["mode"]
                )
            elif "sticker" in response:
                await update.message.reply_sticker(sticker=response["sticker"])
