
from telegram import *
from telegram.ext import *
import time as t
from datetime import datetime
import os, random
from constants import url
import media
from variables import times, text
from hooks import db, api
from main import job_queue


class ClickMe:
    def __init__(self):
        self.current_button_data = None
        self.clicked_buttons = set()
        self.first_user_clicked = False

    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.first_user_clicked = False
        if context.bot_data is None:
            context.bot_data = {}

        previous_click_me_id = context.bot_data.get('click_me_id')
        previous_clicked_id = context.bot_data.get('clicked_id')

        if previous_click_me_id:
            try:
                await context.bot.delete_message(chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"), message_id=previous_click_me_id)
                await context.bot.delete_message(chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"), message_id=previous_clicked_id)
            except Exception:
                pass

        self.current_button_data = str(random.randint(1, 100000000))
        context.bot_data["current_button_data"] = self.current_button_data

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Click Me!", callback_data=self.current_button_data)]]
        )
        click_me = await context.bot.send_photo(
                        photo=api.get_random_pioneer(),
                        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
                        reply_markup=keyboard,
                    )

        button_generation_timestamp = t.time()
        context.bot_data["button_generation_timestamp"] = button_generation_timestamp
        context.bot_data['click_me_id'] = click_me.message_id

    async def function(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        button_click_timestamp = t.time()

        if context.user_data is None:
            context.user_data = {}

        current_button_data = context.bot_data.get("current_button_data")
        button_generation_timestamp = context.bot_data.get("button_generation_timestamp")
        if not current_button_data:
            return

        button_data = update.callback_query.data
        user = update.effective_user
        user_info = user.username or f"{user.first_name} {user.last_name}" or user.first_name

        if button_data in self.clicked_buttons:
            return

        self.clicked_buttons.add(button_data)

        if button_data == current_button_data:
            time_taken = button_click_timestamp - button_generation_timestamp

            await db.clicks_update(user_info, time_taken)

            if not self.first_user_clicked:
                self.first_user_clicked = True

                user_data = db.clicks_get_by_name(user_info)
                clicks = user_data[0]
                streak = user_data[2]
                total_click_count = db.clicks_get_total()
                if clicks == 1:
                    click_message = f"🎉🎉 This is their first button click! 🎉🎉"

                elif clicks % 10 == 0:
                    click_message = f"🎉🎉 They been the fastest Pioneer {clicks} times and on a *{streak}* click streak! 🎉🎉"

                else:
                    click_message = f"They have been the fastest Pioneer {clicks} times and on a *{streak}* click streak!"

                check_time = db.clicks_check_time(time_taken)
                if check_time == "fastest" or check_time == "slowest":
                    click_message += f"\n\n🎉🎉 {time_taken:.3f} seconds is the new {check_time} time! 🎉🎉"

                clicks_needed = times.BURN_INCREMENT - (total_click_count % times.BURN_INCREMENT)

                message_text = (
                    f"{api.escape_markdown(user_info)} was the fastest Pioneer in {time_taken:.3f} seconds!\n\n"
                    f"{click_message}\n\n"
                    f"The button has been clicked a total of {total_click_count} times by all Pioneers!\n\n"
                    f"Clicks till next X7R Burn: *{clicks_needed}*\n\n"
                    f"use `/leaderboard` to see the fastest Pioneers!\n\n"
                )

                photos = await context.bot.get_user_profile_photos(update.effective_user.id, limit=1)
                if photos and photos.photos and photos.photos[0]:
                    photo = photos.photos[0][0].file_id

                    clicked = await context.bot.send_photo(
                        photo=photo,
                        chat_id=update.effective_chat.id,
                        caption=message_text,
                        parse_mode="Markdown",
                    )
                else:
                    clicked = await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message_text,
                        parse_mode="Markdown",
                    )

                if total_click_count % times.BURN_INCREMENT == 0:
                    burn_message = await api.burn_x7r(times.BURN_AMOUNT)
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=
                            f"🔥🔥🔥🔥🔥🔥🔥🔥\n\n"
                            f"The button has been clicked a total of {total_click_count} times by all Pioneers!\n\n"
                            f"{burn_message}"
                    )

            context.bot_data['clicked_id'] = clicked.message_id

            times.RESTART_TIME = datetime.now().timestamp()
            context.user_data["current_button_data"] = None
            times.BUTTON_TIME = times.RANDOM_BUTTON_TIME()
            job_queue.run_once(
                self.send,
                times.BUTTON_TIME,
                chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
                name="Click Me",
            )

            return times.BUTTON_TIME


async def messages(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    messages = [text.ABOUT, text.AIRDROP, text.ECOSYSTEM,
                text.VOLUME, random.choice(text.QUOTES)]
    random_message = random.choice(messages)
    if random_message in text.QUOTES:
        message = f"*X7 Finance Whitepaper Quote*\n\n{random_message}"
    else:
        message = random_message

    await context.bot.send_photo(
        chat_id=job.chat_id,
        photo=api.get_random_pioneer(),
    )

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"{message}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.XCHANGE}")],
                [InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}")],
            ]
        ),
    )


async def replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"{update.effective_message.text}"
    lower_message = message.lower()
    keyword_to_response = {
        "https://twitter": {
            "text": random.choice(text.X_REPLIES),
            "mode": None,
        },
        "https://x.com": {
            "text": random.choice(text.X_REPLIES),
            "mode": None,
        },
        "gm": {"sticker": media.GM},
        "gm!": {"sticker": media.GM},
        "new on chain message": {"sticker": media.ONCHAIN},
        "lfg": {"sticker": media.LFG},
        "goat": {"sticker": media.GOAT},
        "smashed": {"sticker": media.SMASHED},
        "wagmi": {"sticker": media.WAGMI},
        "slapped": {"sticker": media.SLAPPED},
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

