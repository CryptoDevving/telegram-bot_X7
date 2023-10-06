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


async def auto_message_info(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    messages = [text.about, text.airdrop, text.ecosystem, text.endorse,
                text.refer, text.volume, text.voting, random.choice(text.quotes)]
    random_message = random.choice(messages)
    if random_message in text.quotes:
        message = f"*X7 Finance Whitepaper Quote*\n\n{random_message}"
    else:
        message = random_message

    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
    )

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"{message}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.xchange}")],
                [InlineKeyboardButton(text="Website", url=f"{url.dashboard}")],
            ]
        ),
    )


async def clicks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_button_data, first_user_clicked, first_user_info
    if context.user_data is None:
        context.user_data = {}

    current_button_data = context.bot_data.get("current_button_data")
    button_generation_timestamp = context.bot_data.get("button_generation_timestamp")
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
        button_click_timestamp = t.time()
        time_taken = button_click_timestamp - button_generation_timestamp
        click_counts[user_info] = click_counts.get(user_info, 0) + 1
        clicks_save(click_counts.copy())
        users_clicked_current_button.add(user_info)
        user_clicks = clicks_get_user_total(user_info)
        if not first_user_clicked:
            first_user_info = user_info
            first_user_clicked = True
            total_click_count = clicks_get_total()
            if user_clicks == 1:
                click_message = "🎉🎉 This is their first button click! 🎉🎉"
            elif user_clicks % 10 == 0:
                click_message = f"🎉🎉 They been the fastest Pioneer {user_clicks} times! 🎉🎉"
            else:
                click_message = f"They have been the fastest Pioneer {user_clicks} times!"
            
            message_text = (
                f"{api.escape_markdown(user_info)} was the fastest Pioneer in\n{time_taken:.2f} seconds!\n\n"
                f"{click_message}\n\n"
                f"use `/leaderboard` to see the fastest Pioneers!\n\n"
            )
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message_text,
                parse_mode="Markdown",
            )

            if total_click_count % 50 == 0:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"🎉🎉 The button has been clicked a total of {total_click_count} times by all Pioneers! 🎉🎉",
                    parse_mode="Markdown",
                )
                
    context.user_data["current_button_data"] = None
    click_counts.clear()


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


def clicks_get_user_total(username):
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
        "https://twitter": {
            "text": random.choice(text.x_replies),
            "mode": None,
        },
        "https://x.com": {
            "text": random.choice(text.x_replies),
            "mode": None,
        },
        "gm": {"sticker": media.gm},
        "gm!": {"sticker": media.gm},
        "new on chain message": {"sticker": media.onchain},
        "lfg": {"sticker": media.lfg},
        "goat": {"sticker": media.goat},
        "smashed": {"sticker": media.smashed},
        "wagmi": {"sticker": media.wagmi},
        "slapped": {"sticker": media.slapped},
    }

    words = lower_message.split()

    for keyword, response in keyword_to_response.items():
        if keyword.startswith("https://"):
            if any(word.startswith(keyword) for word in words):
                if "text" in response:
                    await update.message.reply_text(
                        text=response["text"], parse_mode=response["mode"]
                    )
                elif "sticker" in response:
                    await update.message.reply_sticker(sticker=response["sticker"])
        else:
            if (
                f" {keyword} " in f" {lower_message} "
                or lower_message.startswith(keyword + " ")
                or lower_message.endswith(" " + keyword)
            ):
                if "text" in response:
                    await update.message.reply_text(
                        text=response["text"], parse_mode=response["mode"]
                    )
                elif "sticker" in response:
                    await update.message.reply_sticker(sticker=response["sticker"])
