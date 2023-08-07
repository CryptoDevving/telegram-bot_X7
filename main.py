import os
import csv
import sys
import random
import subprocess

import sentry_sdk
from telegram import *
from telegram.ext import *
from dotenv import load_dotenv

import commands
from api import index as api
from media import index as media
from data import url, text, times

load_dotenv()

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)

current_button_data = None
users_clicked_current_button = set()
clicked_buttons = set()
first_user_clicked = False
first_user_info = ""
click_counts = {}
random_message_job = None


async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"{update.effective_message.text}"
    lower_message = message.lower()
    keyword_to_response = {
        "rob the bank": {"text": text.rob, "mode": "Markdown"},
        "delay": {"text": text.delay, "mode": "Markdown"},
        "patience": {"text": text.patience, "mode": "Markdown"},
        "https://twitter": {
            "text": random.choice(text.twitter_replies),
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

        application.job_queue.run_once(
            send_click_message,
            random.randint(1, 20),
            chat_id=os.getenv("TEST_TELEGRAM_CHANNEL_ID"),
            name="Click Message",
            data=random.randint(1, 20),
        )


def clicks_get():
    click_counts = {}
    with open("data/clicks.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 1:
                user_info, count = row[0].split(": ")
                click_counts[user_info] = int(count)
    return click_counts


def clicks_save(click_counts):
    with open("data/clicks.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        for user_info, count in click_counts.items():
            writer.writerow([f"{user_info}: {count}"])


async def clicks_leaderboard(update: Update, context: CallbackContext):
    click_counts = clicks_get()
    sorted_click_counts = sorted(click_counts.items(), key=lambda x: x[1], reverse=True)
    formatted_click_counts = "\n".join(
        f"{user}: {count}" for user, count in sorted_click_counts
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=formatted_click_counts
    )


def scanner_start():
    scripts = [
        "scanner-bsc.py",
        "scanner-eth.py",
        "scanner-arb.py",
        "scanner-poly.py",
        "scanner-opti.py",
    ]
    python_executable = sys.executable
    processes = []
    for script in scripts:
        command = [python_executable, script]
        process = subprocess.Popen(command)
        processes.append(process)


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
        chat_id=os.getenv("TEST_TELEGRAM_CHANNEL_ID"),
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


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CallbackQueryHandler(clicks))
    application.add_error_handler(error)
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies)
    )
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(
        CommandHandler(["admin_commands", "admin", "admincommands"], commands.admin)
    )
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(
        CommandHandler(["rollout", "multichain", "airdrop"], commands.airdrop)
    )
    application.add_handler(CommandHandler("alumni", commands.alumni))
    application.add_handler(CommandHandler("announcements", commands.announcements))
    application.add_handler(CommandHandler("ath", commands.ath))
    application.add_handler(CommandHandler("blog", commands.blog))
    application.add_handler(CommandHandler(["bot", "start", "filters"], commands.bot))
    application.add_handler(CommandHandler("burn", commands.burn))
    application.add_handler(CommandHandler("buy", commands.buy))
    application.add_handler(
        CommandHandler(["buybots", "bobby", "buybot"], commands.buy_bots)
    )
    application.add_handler(
        CommandHandler(["buyevenly", "quintsevenly"], commands.buy_evenly)
    )
    application.add_handler(CommandHandler("channels", commands.channels))
    application.add_handler(CommandHandler(["chart", "charts"], commands.chart))
    application.add_handler(
        CommandHandler(
            ["constellations", "constellation", "quints"], commands.constellations
        )
    )
    application.add_handler(
        CommandHandler(["ca", "contract", "contracts"], commands.contracts)
    )
    application.add_handler(CommandHandler("compare", commands.compare))
    application.add_handler(CommandHandler("count", commands.count))
    application.add_handler(
        CommandHandler([f"{times.countdown_command}"], commands.countdown)
    )
    application.add_handler(CommandHandler(["deployer", "devs"], commands.deployer))
    application.add_handler(
        CommandHandler(["discount", "dsc", "dac"], commands.discount)
    )
    application.add_handler(
        CommandHandler(
            [
                "docs",
                "documents",
            ],
            commands.docs,
        )
    )
    application.add_handler(CommandHandler("draw", commands.draw))
    application.add_handler(CommandHandler(["ebb", "buybacks"], commands.ebb))
    application.add_handler(CommandHandler(["ecosystem", "tokens"], commands.ecosystem))
    application.add_handler(CommandHandler("fact", commands.fact))
    application.add_handler(CommandHandler("factory", commands.factory))
    application.add_handler(CommandHandler("faq", commands.faq))
    application.add_handler(CommandHandler(["fg", "feargreed"], commands.fg))
    application.add_handler(CommandHandler("gas", commands.gas))
    application.add_handler(CommandHandler("german", commands.german))
    application.add_handler(CommandHandler("giveaway", commands.giveaway_command))
    application.add_handler(CommandHandler("holders", commands.holders))
    application.add_handler(CommandHandler("image", commands.image))
    application.add_handler(CommandHandler("joke", commands.joke))
    application.add_handler(CommandHandler("launch", commands.launch))
    application.add_handler(CommandHandler("leaderboard", clicks_leaderboard))
    application.add_handler(CommandHandler(["links", "socials"], commands.links))
    application.add_handler(CommandHandler("liquidate", commands.liquidate))
    application.add_handler(CommandHandler("liquidity", commands.liquidity))
    application.add_handler(CommandHandler("loan", commands.loan))
    application.add_handler(CommandHandler(["loans", "borrow"], commands.loans_command))
    application.add_handler(CommandHandler("magisters", commands.magisters))
    application.add_handler(CommandHandler(["mcap", "marketcap", "cap"], commands.mcap))
    application.add_handler(CommandHandler("media", commands.media_command))
    application.add_handler(CommandHandler("mods", commands.mods))
    application.add_handler(CommandHandler(["nft", "nfts"], commands.nft))
    application.add_handler(
        CommandHandler(["on_chain", "onchain", "message"], commands.on_chain)
    )
    application.add_handler(CommandHandler(["pair", "pairs"], commands.pair))
    application.add_handler(CommandHandler("pioneer", commands.pioneer))
    application.add_handler(CommandHandler("proposal", commands.proposal))
    application.add_handler(
        CommandHandler(["pool", "lpool", "lendingpool"], commands.pool)
    )
    application.add_handler(CommandHandler(["price", "prices"], commands.price))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler("raid", commands.raid))
    application.add_handler(CommandHandler(["referral", "refer"], commands.refer))
    application.add_handler(CommandHandler("roadmap", commands.roadmap))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler("snapshot", commands.snapshot))
    application.add_handler(CommandHandler(["spaces", "space"], commands.spaces))
    application.add_handler(
        CommandHandler(["split", "splitters", "splitter"], commands.splitters)
    )
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(
        CommandHandler(["beta", "swap", "xchange", "dex"], commands.swap)
    )
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("test", commands.test))
    application.add_handler(CommandHandler(["time", "clock"], commands.time))
    application.add_handler(CommandHandler("today", commands.today))
    application.add_handler(CommandHandler("treasury", commands.treasury))
    application.add_handler(CommandHandler("twitter", commands.twitter))
    application.add_handler(CommandHandler("website", commands.website))
    application.add_handler(CommandHandler("x7r", commands.x7r))
    application.add_handler(CommandHandler("x7d", commands.x7d))
    application.add_handler(CommandHandler(["x7dao", "dao"], commands.x7dao))
    application.add_handler(CommandHandler(["x7101", "101"], commands.x7101))
    application.add_handler(CommandHandler(["x7102", "102"], commands.x7102))
    application.add_handler(CommandHandler(["x7103", "103"], commands.x7103))
    application.add_handler(CommandHandler(["x7104", "104"], commands.x7104))
    application.add_handler(CommandHandler(["x7105", "105"], commands.x7105))
    application.add_handler(CommandHandler(["volume", "dune"], commands.volume))
    application.add_handler(CommandHandler("voting", commands.voting))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler("wallet", commands.wallet))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(
        CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp)
    )

    job_queue = application.job_queue
    application.job_queue.run_repeating(
        send_endorsement_message,
        times.endorse_time * 60 * 60,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Endorsement Message",
        data=times.endorse_time * 60 * 60,
    )
    application.job_queue.run_repeating(
        send_referral_message,
        times.referral_time * 60 * 60,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        first=10800,
        name="Referral Message",
        data=times.referral_time * 60 * 60,
    )

    application.job_queue.run_once(
        send_click_message,
        random.randint(1, 20),  #86400
        chat_id=os.getenv("TEST_TELEGRAM_CHANNEL_ID"),
        name="Random Message",
        data=random.randint(1, 20),  #86400
    )
    scanner_start()

    application.run_polling()
