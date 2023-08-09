import os
import csv
import main
import random
import base64
import requests

import sentry_sdk
from telegram import *
from telegram.ext import *

from api import index as api
from media import index as media
from data import url, text, times


sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)


current_button_data = None
users_clicked_current_button = set()
clicked_buttons = set()
first_user_clicked = False
first_user_info = ""
click_counts = {}


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
        "new on chain message": {"sticker": media.chain},
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


async def error(update: Update, context: CallbackContext):
    try:
        if update is None:
            return
        if update.edited_message is not None:
            return
        if isinstance(context.error, AttributeError):
            return
        if isinstance(context.error, ValueError) or isinstance(
            context.error, Exception
        ):
            await update.message.reply_text("Error while loading data please try again")
        else:
            message: Message = update.message
            if message is not None and message.text is not None:
                await update.message.reply_text(
                    "Error while loading data, please try again"
                )
                sentry_sdk.capture_exception(
                    Exception(f"{message.text} caused error: {context.error}")
                )
            else:
                sentry_sdk.capture_exception(
                    Exception(
                        f"Error occurred without a valid message: {context.error}"
                    )
                )

    except Exception as e:
        sentry_sdk.capture_exception(e)


async def clicks(update, context):
    global current_button_data, users_clicked_current_button, clicked_buttons, first_user_clicked, first_user_info, click_counts
    if context.user_data is None:
        context.user_data = {}

    current_button_data = context.bot_data.get("current_button_data")
    if not current_button_data:
        return

    button_data = update.callback_query.data
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"

    if button_data in clicked_buttons:
        return

    clicked_buttons.add(button_data)

    if user_info not in click_counts:
        click_counts[user_info] = 0

    if button_data == current_button_data:
        click_counts[user_info] = click_counts.get(user_info, 0) + 1
        if click_counts[user_info] % 10 == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=
                f"🎉🎉 *{user_info} has been the fastest Pioneer {click_counts[user_info]} times!* 🎉🎉",
                parse_mode="Markdown"
            )

        clicks_save(click_counts.copy())
        users_clicked_current_button.add(user_info)

        if not first_user_clicked:
            first_user_info = user_info
            first_user_clicked = True
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=
                f"{user_info} was the fastest Pioneer!\n\n"
                "use `/leaderboard` to see the fastest Pioneers!",
                parse_mode="Markdown",
            )

        context.user_data["current_button_data"] = None

        main.application.job_queue.run_once(
            send_click_message,
            times.button_time, 
            chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
            name="Click Message",
            data=times.button_time, 
        )


def clicks_get():
    click_counts = {}
    try:
        with open("data/clicks.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                user, clicks = row
                click_counts[user] = int(clicks)
    except FileNotFoundError:
        pass  
    return click_counts


def clicks_save(click_counts):
    existing_clicks = clicks_get()
    for user, clicks in click_counts.items():
        if user in existing_clicks:
            existing_clicks[user] += clicks
        else:
            existing_clicks[user] = clicks

    with open("data/clicks.csv", mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["User", "Clicks"])  # Writing header
        for user, clicks in existing_clicks.items():
            csv_writer.writerow([user, clicks])

    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_PAT")}'
    }
    response = requests.get(
        'https://api.github.com/repos/x7finance/telegram-bot/contents/data/clicks.csv',
        headers=headers
    )

    if response.status_code == 200:
        content = response.json()
        sha = content['sha']

        with open("data/clicks.csv", 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        try:
            response = requests.put(
                'https://api.github.com/repos/x7finance/telegram-bot/contents/data/clicks.csv',
                headers=headers,
                json={
                    'message': 'auto: update clicks log',
                    'content': encoded_content,
                    'sha': sha
                }
            )
        except Exception as e:
            sentry_sdk.capture_exception(f"GitHub Push error: {e}")
            

async def send_click_message(context: CallbackContext):
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


async def send_endorsement_message(context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def send_referral_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    photo_url = f"{url.pioneers}{api.get_random_pioneer_number()}.png"
    caption_text = f"*X7 Finance Referral Scheme*\n\n{text.referral}"
    keyboard_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Application", url=f"{url.referral}")]]
    )
    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=photo_url,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=keyboard_markup,
    )
