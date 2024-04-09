from telegram import *
from telegram.ext import *

import os, sys, sentry_sdk, subprocess, random, time as t
from datetime import datetime

from bot import admin, auto, commands, welcome
from hooks import api, db
from variables import times
from constants import chains


application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
job_queue = application.job_queue


CURRENT_BUTTON_DATA = None
CLICKED_BUTTONS = set()
FIRST_USER_CLICKED = False


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

sentry_sdk.init(
    dsn = os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)


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
            print({context.error})
            sentry_sdk.capture_exception(
                Exception(f"{message.text} caused error: {context.error}")
                )
        else:
            sentry_sdk.capture_exception(
                Exception(
                    f"Error occurred without a valid message: {context.error}"
                )
            )


def scanners():
    python_executable = sys.executable
    processes = []
    for chain_name, chain_info in chains.CHAINS.items():
        script_filename = chain_name + ".py"
        script_path = os.path.join(os.path.dirname(__file__), script_filename)
        if os.path.exists(script_path):
            command = [python_executable, script_path]
            process = subprocess.Popen(command)
            processes.append(process)



async def button_send(context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_BUTTON_DATA, FIRST_USER_CLICKED
    FIRST_USER_CLICKED = False
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

    CURRENT_BUTTON_DATA = str(random.randint(1, 100000000))
    context.bot_data["current_button_data"] = CURRENT_BUTTON_DATA

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Me!", callback_data=CURRENT_BUTTON_DATA)]]
    )
    click_me = await context.bot.send_photo(
                    photo=api.get_random_pioneer(),
                    chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
                    reply_markup=keyboard,
                )

    button_generation_timestamp = t.time()
    context.bot_data["button_generation_timestamp"] = button_generation_timestamp
    context.bot_data['click_me_id'] = click_me.message_id


async def button_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_BUTTON_DATA, FIRST_USER_CLICKED
    button_click_timestamp = t.time()

    if context.user_data is None:
        context.user_data = {}

    CURRENT_BUTTON_DATA = context.bot_data.get("current_button_data")
    button_generation_timestamp = context.bot_data.get("button_generation_timestamp")
    if not CURRENT_BUTTON_DATA:
        return

    button_data = update.callback_query.data
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}" or user.first_name

    if button_data in CLICKED_BUTTONS:
        return

    CLICKED_BUTTONS.add(button_data)

    if button_data == CURRENT_BUTTON_DATA:
        time_taken = button_click_timestamp - button_generation_timestamp

        await db.clicks_update(user_info, time_taken)

        if not FIRST_USER_CLICKED:
            FIRST_USER_CLICKED = True

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
            button_send,
            times.BUTTON_TIME,
            chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
            name="Click Me",
        )
            
            return times.BUTTON_TIME


async def click_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        await button_send(context)


if __name__ == "__main__":
    application.add_error_handler(error)
    application.add_handler(CommandHandler("test", test))

    ## WELCOME ##
    application.add_handler(ChatMemberHandler(welcome.message, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.StatusUpdate._NewChatMembers(Update) | filters.StatusUpdate._LeftChatMember(Update), welcome.delete))
    application.add_handler(CallbackQueryHandler(welcome.button_callback, pattern=r"unmute:.+"))
    
    ## COMANDS ##
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler("admins", commands.admins))
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(CommandHandler("alumni", commands.alumni))
    application.add_handler(CommandHandler("announcements", commands.announcements))
    application.add_handler(CommandHandler("ath", commands.ath))
    application.add_handler(CommandHandler("blocks", commands.blocks))
    application.add_handler(CommandHandler("blog", commands.blog))
    application.add_handler(CommandHandler("borrow", commands.borrow))
    application.add_handler(CommandHandler(["bot", "start", "filters"], commands.bot))
    application.add_handler(CommandHandler("burn", commands.burn))
    application.add_handler(CommandHandler("buy", commands.buy))
    application.add_handler(CommandHandler("channels", commands.channels))
    application.add_handler(CommandHandler(["chart", "charts"], commands.chart))
    application.add_handler(CommandHandler("check", commands.check))
    application.add_handler(CommandHandler("compare", commands.compare))
    application.add_handler(CommandHandler(["constellations", "constellation", "quints"], commands.constellations))
    application.add_handler(CommandHandler(["ca", "contract", "contracts"], commands.contracts))
    application.add_handler(CommandHandler("contribute", commands.contribute))
    application.add_handler(CommandHandler("convert", commands.convert))
    application.add_handler(CommandHandler("costs", commands.costs))
    application.add_handler(CommandHandler("countdown", commands.countdown))
    application.add_handler(CommandHandler(["dao", "vote", "snapshot", "propose"], commands.dao_command))
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
    application.add_handler(CommandHandler(["links", "socials", "dune", "github", "reddit", "warpcast"], commands.links))
    application.add_handler(CommandHandler("liquidate", commands.liquidate))
    application.add_handler(CommandHandler("liquidity", commands.liquidity))
    application.add_handler(CommandHandler("loan", commands.loan))
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
    application.add_handler(CommandHandler(["price", "prices"], commands.price))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("scan", commands.scan))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler(["split", "splitters", "splitter"], commands.splitters_command))
    application.add_handler(CommandHandler("stats", commands.stats))
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("timestamp", commands.timestamp_command))
    application.add_handler(CommandHandler(["time", "clock"], commands.time))
    application.add_handler(CommandHandler("today", commands.today))
    application.add_handler(CommandHandler("german", commands.translate_german))
    application.add_handler(CommandHandler("japanese", commands.translate_japanese))
    application.add_handler(CommandHandler("russian", commands.translate_russian))
    application.add_handler(CommandHandler("treasury", commands.treasury))
    application.add_handler(CommandHandler(["trending", "trend"], commands.trending))
    application.add_handler(CommandHandler("twitter", commands.twitter))
    application.add_handler(CommandHandler(["website", "site", "swap", "dex", "xchange"], commands.website))
    application.add_handler(CommandHandler("v1", commands.v1))
    application.add_handler(CommandHandler(["volume"], commands.volume))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler("wallet", commands.wallet))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(CommandHandler("word", commands.word))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))
    application.add_handler(CommandHandler("x7r", commands.x7r))
    application.add_handler(CommandHandler("x7d", commands.x7d))
    application.add_handler(CommandHandler("x7dao", commands.x7dao))
    application.add_handler(CommandHandler(["x7101", "101"], commands.x7101))
    application.add_handler(CommandHandler(["x7102", "102"], commands.x7102))
    application.add_handler(CommandHandler(["x7103", "103"], commands.x7103))
    application.add_handler(CommandHandler(["x7104", "104"], commands.x7104))
    application.add_handler(CommandHandler(["x7105", "105"], commands.x7105))
    application.add_handler(CommandHandler("x", commands.x))


    ## ADMIN ##
    application.add_handler(CommandHandler("clickme", click_me))
    application.add_handler(CommandHandler("add", admin.add))
    application.add_handler(CommandHandler("delete", admin.delete))
    application.add_handler(CommandHandler("reset", admin.reset))
    application.add_handler(CommandHandler("wen", admin.wen))

    ## AUTO ##
    application.add_handler(CallbackQueryHandler(button_function))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto.replies))

    job_queue.run_once(
        button_send,
        times.FIRST_BUTTON_TIME,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Click Me",
    )

    ## RUN ##
    scanners()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
