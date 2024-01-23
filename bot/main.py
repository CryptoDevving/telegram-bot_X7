import sentry_sdk
from telegram import *
from telegram.ext import *
from web3 import Web3

import os
import sys
import time as t
import subprocess
import random
from datetime import datetime
from typing import Optional, Tuple

import commands
import twitter

from data import times, url, ca, text
from api import index as api
from api import db
from media import index as media


current_button_data = None
clicked_buttons = set()
first_user_clicked = False

sentry_sdk.init(
    dsn = os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)


RESTRICTIONS = {
    'can_send_messages': False,
    'can_send_media_messages': False,
    'can_send_other_messages': False,
    'can_add_web_page_previews': False,
}


async def auto_message_click(context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_button_data, first_user_clicked
    first_user_clicked = False
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

    current_button_data = str(random.randint(1, 100000000))
    context.bot_data["current_button_data"] = current_button_data
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Me!", callback_data=current_button_data)]]
    )
    click_me = await context.bot.send_photo(
                    photo=f"{url.pioneers}{api.get_random_pioneer_number()}.png",
                    chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
                    reply_markup=keyboard,
                )
    
    button_generation_timestamp = t.time()
    context.bot_data["button_generation_timestamp"] = button_generation_timestamp
    context.bot_data['click_me_id'] = click_me.message_id
    
    
async def auto_message_info(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    messages = [text.about, text.airdrop, text.ecosystem,
                text.volume, text.voting, random.choice(text.quotes)]
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
                [InlineKeyboardButton(text="Website", url=f"{url.website}")],
            ]
        ),
    )


async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def clicks_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_button_data, first_user_clicked
    button_click_timestamp = t.time()
    
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

    if button_data == current_button_data:
        time_taken = button_click_timestamp - button_generation_timestamp

        await db.clicks_update(user_info, time_taken)
    
        if not first_user_clicked:
            first_user_clicked = True

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

            if db.clicks_check_is_fastest(time_taken):
                click_message +=  f"\n\n🎉🎉 {time_taken:.3f} seconds is the new fastest time! 🎉🎉"

            clicks_needed = times.burn_increment - (total_click_count % times.burn_increment)

            message_text = (
                f"{api.escape_markdown(user_info)} was the fastest Pioneer in\n{time_taken:.3f} seconds!\n\n"
                f"{click_message}\n\n"
                f"The button has been clicked a total of {total_click_count} times by all Pioneers!\n\n"
                f"Clicks till next X7R Burn: *{clicks_needed}*\n\n"
                f"use `/leaderboard` to see the fastest Pioneers!\n\n"
            )
            
            clicked = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message_text,
                parse_mode="Markdown",
            )

            if total_click_count % text.burn_increment == 0:
                burn_message = await api.burn_x7r(text.burn_amount)
                await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"🔥🔥🔥🔥🔥🔥🔥🔥\n\n"
                            f"The button has been clicked a total of {total_click_count} times by all Pioneers!\n\n"
                            f"{burn_message}"
                    )

            context.bot_data['clicked_id'] = clicked.message_id

            times.restart_time = datetime.now().timestamp()        
            context.user_data["current_button_data"] = None
            times.button_time = times.random_button_time()
            job_queue.run_once(
            auto_message_click,
            times.button_time,
            chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
            name="Click Message",
        )
            
            return times.button_time
    

async def welcome_button_callback(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    action, _ = update.callback_query.data.split(":", 1)

    if action == "unmute":
        user_restrictions = {key: True for key in RESTRICTIONS}

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=user_restrictions,
        )


def welcome_member(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:

    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_id = update.effective_chat.id
    if str(channel_id) == os.getenv("MAIN_TELEGRAM_CHANNEL_ID"):
        result = welcome_member(update.chat_member)
        if result is None:
            return

        was_member, is_member = result
        new_member = update.chat_member.new_chat_member
        new_member_id = new_member.user.id
        if new_member.user.username:
            new_member_username = f"@{new_member.user.username}"
        else:
            if new_member.user.last_name:
                new_member_username = f"{new_member.user.first_name} {new_member.user.last_name}"
            else:
                new_member_username = new_member.user.first_name

        if not was_member and is_member:
            previous_welcome_message_id = context.bot_data.get('welcome_message_id')
            if previous_welcome_message_id:
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=previous_welcome_message_id)
                except Exception:
                    pass

            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=new_member_id,
                permissions=RESTRICTIONS,
            )
            welcome_message = await update.effective_chat.send_video(
                video=open(media.welcomevideo, 'rb'),
                caption=(
                    f"Welcome {api.escape_markdown(new_member_username)} to X7 Finance\n\n"
                    f"Home of Xchange - A censorship resistant DEX offering initial loaned liquidity across;\n\n"
                    f"• Ethereum\n"
                    f"• Binance Smart Chain\n"
                    f"• Arbitrum\n"
                    f"• Optimism\n"
                    f"• Polygon\n"
                    f"• Base Chain\n\n"
                    f"Verify as human and check out the links to get started!"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="I am human!",
                                callback_data=f"unmute:{new_member_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Website",
                                url=url.website,
                            ),
                            InlineKeyboardButton(
                                text="Xchange",
                                url=url.xchange,
                            ),
                        ],
                    ]
                )
            )

            context.bot_data['welcome_message_id'] = welcome_message.message_id
   

async def error(update: Update, context: CallbackContext):
    if update is None:
        return
    if update.edited_message is not None:
        return
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
            

application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
job_queue = application.job_queue


if __name__ == "__main__":
    application.add_error_handler(error)
    application.add_handler(ChatMemberHandler(welcome_message, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(CallbackQueryHandler(welcome_button_callback, pattern=r"unmute:.+"))
    application.add_handler(CommandHandler("test", commands.test))

    ## COMANDS ##
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler(["admin_commands", "admin", "admincommands"], commands.admin_command))
    application.add_handler(CommandHandler(["rollout", "multichain", "airdrop"], commands.airdrop))
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(CommandHandler("alumni", commands.alumni))
    application.add_handler(CommandHandler("announcements", commands.announcements))
    application.add_handler(CommandHandler("ath", commands.ath))
    application.add_handler(CommandHandler("bio", commands.bio))
    application.add_handler(CommandHandler("blocks", commands.blocks))
    application.add_handler(CommandHandler("blog", commands.blog))
    application.add_handler(CommandHandler(["bot", "start", "filters"], commands.bot))
    application.add_handler(CommandHandler("burn", commands.burn))
    application.add_handler(CommandHandler("buy", commands.buy))
    application.add_handler(CommandHandler("channels", commands.channels))
    application.add_handler(CommandHandler(["chart", "charts"], commands.chart))
    application.add_handler(CommandHandler("check", commands.check))
    application.add_handler(CommandHandler(["constellations", "constellation", "quints"], commands.constellations))
    application.add_handler(CommandHandler(["ca", "contract", "contracts"], commands.contracts))
    application.add_handler(CommandHandler("compare", commands.compare))
    application.add_handler(CommandHandler("countdown", commands.countdown))
    application.add_handler(CommandHandler(["dao", "vote", "snaphot"], commands.dao_command))
    application.add_handler(CommandHandler(["deployer", "devs"], commands.deployer))
    application.add_handler(CommandHandler(["discount", "dsc", "dac"], commands.discount))
    application.add_handler(CommandHandler(["docs", "documents"], commands.docs,))
    application.add_handler(CommandHandler(["ebb", "buybacks"], commands.ebb))
    application.add_handler(CommandHandler(["ecosystem", "tokens"], commands.ecosystem))
    application.add_handler(CommandHandler("fact", commands.fact))
    application.add_handler(CommandHandler("factory", commands.factory))
    application.add_handler(CommandHandler("faq", commands.faq))
    application.add_handler(CommandHandler(["fee", "fees"], commands.fees))
    application.add_handler(CommandHandler(["fg", "feargreed"], commands.fg))
    application.add_handler(CommandHandler("gas", commands.gas))
    application.add_handler(CommandHandler("giveaway", commands.giveaway_command))
    application.add_handler(CommandHandler("holders", commands.holders))
    application.add_handler(CommandHandler("image", commands.image))
    application.add_handler(CommandHandler("joke", commands.joke))
    application.add_handler(CommandHandler("launch", commands.launch))
    application.add_handler(CommandHandler("leaderboard", commands.leaderboard))
    application.add_handler(CommandHandler(["links", "socials"], commands.links))
    application.add_handler(CommandHandler("liquidate", commands.liquidate))
    application.add_handler(CommandHandler("liquidity", commands.liquidity))
    application.add_handler(CommandHandler("loan_id", commands.loan))
    application.add_handler(CommandHandler(["loans", "borrow"], commands.loans_command))
    application.add_handler(CommandHandler("locks", commands.locks))
    application.add_handler(CommandHandler("me", commands.me))
    application.add_handler(CommandHandler("magisters", commands.magisters))
    application.add_handler(CommandHandler(["mcap", "marketcap", "cap"], commands.mcap))
    application.add_handler(CommandHandler("media", commands.media_command))
    application.add_handler(CommandHandler(["nft", "nfts"], commands.nft))
    application.add_handler(CommandHandler(["on_chain", "onchain", "message"], commands.on_chain))
    application.add_handler(CommandHandler(["pair", "pairs"], commands.pair))
    application.add_handler(CommandHandler("pfp", commands.pfp))
    application.add_handler(CommandHandler("pioneer", commands.pioneer))
    application.add_handler(CommandHandler(["pool", "lpool", "lendingpool"], commands.pool))
    application.add_handler(CommandHandler(["price", "prices", "x"], commands.price))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler("reset_leaderboard", commands.reset_leaderboard))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("scan", commands.scan))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler(["split", "splitters", "splitter"], commands.splitters))
    application.add_handler(CommandHandler("stats", commands.stats))
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(CommandHandler(["beta", "swap", "xchange", "dex"], commands.swap))
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("timestamp", commands.timestamp_command))
    application.add_handler(CommandHandler(["time", "clock"], commands.time))
    application.add_handler(CommandHandler("today", commands.today))
    application.add_handler(CommandHandler("german", commands.translate_german))
    application.add_handler(CommandHandler("japanese", commands.translate_japanese))
    application.add_handler(CommandHandler("russian", commands.translate_russian))
    application.add_handler(CommandHandler("treasury", commands.treasury))
    application.add_handler(CommandHandler("website", commands.website))
    application.add_handler(CommandHandler("x7r", commands.x7r))
    application.add_handler(CommandHandler("x7d", commands.x7d))
    application.add_handler(CommandHandler("x7dao", commands.x7dao))
    application.add_handler(CommandHandler(["x7101", "101"], commands.x7101))
    application.add_handler(CommandHandler(["x7102", "102"], commands.x7102))
    application.add_handler(CommandHandler(["x7103", "103"], commands.x7103))
    application.add_handler(CommandHandler(["x7104", "104"], commands.x7104))
    application.add_handler(CommandHandler(["x7105", "105"], commands.x7105))
    application.add_handler(CommandHandler(["volume", "dune"], commands.volume))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler("wallet", commands.wallet))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(CommandHandler("wen", commands.wen))
    application.add_handler(CommandHandler("word", commands.word))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))

    ## TWITTER ##
    application.add_handler(CommandHandler(["twitter", "x"], twitter.tweet))
    application.add_handler(CommandHandler("count", twitter.count))
    application.add_handler(CommandHandler("draw", twitter.draw))
    application.add_handler(CommandHandler("raid", twitter.raid))
    application.add_handler(CommandHandler(["spaces", "space"], twitter.spaces))

    ## AUTO ##
    application.add_handler(CallbackQueryHandler(clicks_function))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies))

#    job_queue.run_repeating(
#        auto_message_info,
#        times.auto_message_time,
#        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
#        first=times.auto_message_time,
#        name="Auto Message",
#    )

    job_queue.run_once(
        auto_message_click,
        times.first_button_time,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Click Message",
    )


    ## SCANNERS ##
    scanners = [
        "scanner/bsc.py",
        "scanner/eth.py",
        "scanner/arb.py",
        "scanner/poly.py",
        "scanner/opti.py",
##        "scanner/base.py",
    ]
    python_executable = sys.executable
    processes = []
    for scanner in scanners:
        command = [python_executable, scanner]
        process = subprocess.Popen(command)
        processes.append(process)

    ## RUN ##
    application.run_polling(allowed_updates=Update.ALL_TYPES)
