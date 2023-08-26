import os
import sys
import time as t
import subprocess
import sentry_sdk
from telegram import *
from telegram.ext import *

import auto
import commands
from data import times
from api import index as api


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    if button_data in auto.clicked_buttons:
        return

    auto.clicked_buttons.add(button_data)

    if user_info not in auto.click_counts:
        auto.click_counts[user_info] = 0

    if button_data == current_button_data:
        button_click_timestamp = t.time()
        time_taken = button_click_timestamp - button_generation_timestamp
        auto.click_counts[user_info] = auto.click_counts.get(user_info, 0) + 1
        auto.clicks_save(auto.click_counts.copy())
        auto.users_clicked_current_button.add(user_info)
        user_clicks = auto.get_user_click_total(user_info)
        if not auto.first_user_clicked:
            first_user_info = user_info
            first_user_clicked = True
            total_click_count = auto.clicks_get_total()
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
    auto.click_counts.clear()
    
    job_queue.run_once(
        auto.auto_message_click,
        times.button_time(),
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Click Message",
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
            sentry_sdk.capture_exception(
                Exception(f"{message.text} caused error: {context.error}")
            )
        else:
            sentry_sdk.capture_exception(
                Exception(
                    f"Error occurred without a valid message: {context.error}"
                )
            )


def scanner():
    scripts = [
        "scanner_bsc.py",
        "scanner_eth.py",
        "scanner_arb.py",
        "scanner_poly.py",
        "scanner_opti.py",
    ]
    python_executable = sys.executable
    processes = []
    for script in scripts:
        command = [python_executable, script]
        process = subprocess.Popen(command)
        processes.append(process)


application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
job_queue = application.job_queue


if __name__ == "__main__":
    application.add_error_handler(error)
    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler(["admin_commands", "admin", "admincommands"], commands.admin))
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(CommandHandler(["rollout", "multichain", "airdrop"], commands.airdrop))
    application.add_handler(CommandHandler("alumni", commands.alumni))
    application.add_handler(CommandHandler("announcements", commands.announcements))
    application.add_handler(CommandHandler("ath", commands.ath))
    application.add_handler(CommandHandler("blocks", commands.blocks))
    application.add_handler(CommandHandler("blog", commands.blog))
    application.add_handler(CommandHandler(["bot", "start", "filters"], commands.bot))
    application.add_handler(CommandHandler("burn", commands.burn))
    application.add_handler(CommandHandler("buy", commands.buy))
    application.add_handler(CommandHandler(["buybots", "bobby", "buybot"], commands.buy_bots))
    application.add_handler(CommandHandler(["buyevenly", "quintsevenly"], commands.buy_evenly))
    application.add_handler(CommandHandler("channels", commands.channels))
    application.add_handler(CommandHandler(["chart", "charts"], commands.chart))
    application.add_handler(CommandHandler("check", commands.check))
    application.add_handler(CommandHandler(["constellations", "constellation", "quints"], commands.constellations))
    application.add_handler(CommandHandler(["ca", "contract", "contracts"], commands.contracts))
    application.add_handler(CommandHandler("compare", commands.compare))
    application.add_handler(CommandHandler("countdown", commands.countdown))
    application.add_handler(CommandHandler("dao", commands.dao_command))
    application.add_handler(CommandHandler(["deployer", "devs"], commands.deployer))
    application.add_handler(CommandHandler(["discount", "dsc", "dac"], commands.discount))
    application.add_handler(CommandHandler(["docs", "documents"], commands.docs,))
    application.add_handler(CommandHandler(["ebb", "buybacks"], commands.ebb))
    application.add_handler(CommandHandler(["ecosystem", "tokens"], commands.ecosystem))
    application.add_handler(CommandHandler("fact", commands.fact))
    application.add_handler(CommandHandler("factory", commands.factory))
    application.add_handler(CommandHandler("faq", commands.faq))
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
    application.add_handler(CommandHandler("loan", commands.loan))
    application.add_handler(CommandHandler(["loans", "borrow"], commands.loans_command))
    application.add_handler(CommandHandler("me", commands.me))
    application.add_handler(CommandHandler("magisters", commands.magisters))
    application.add_handler(CommandHandler(["mcap", "marketcap", "cap"], commands.mcap))
    application.add_handler(CommandHandler("media", commands.media_command))
    application.add_handler(CommandHandler("mods", commands.mods))
    application.add_handler(CommandHandler(["nft", "nfts"], commands.nft))
    application.add_handler(CommandHandler(["on_chain", "onchain", "message"], commands.on_chain))
    application.add_handler(CommandHandler(["pair", "pairs"], commands.pair))
    application.add_handler(CommandHandler("pfp", commands.pfp))
    application.add_handler(CommandHandler("pioneer", commands.pioneer))
    application.add_handler(CommandHandler(["pool", "lpool", "lendingpool"], commands.pool))
    application.add_handler(CommandHandler(["price", "prices"], commands.price))
    application.add_handler(CommandHandler("logo", commands.price_logo))
    application.add_handler(CommandHandler("proposal", commands.proposal))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler(["referral", "refer"], commands.refer))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler("snapshot", commands.snapshot))
    application.add_handler(CommandHandler(["split", "splitters", "splitter"], commands.splitters))
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(CommandHandler(["beta", "swap", "xchange", "dex"], commands.swap))
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("test", commands.test))
    application.add_handler(CommandHandler(["time", "clock"], commands.time))
    application.add_handler(CommandHandler("today", commands.today))
    application.add_handler(CommandHandler("german", commands.translate_german))
    application.add_handler(CommandHandler("german", commands.translate_japanese))
    application.add_handler(CommandHandler("treasury", commands.treasury))
    application.add_handler(CommandHandler("trending", commands.trending))
    application.add_handler(CommandHandler(["twitter", "x"], commands.twitter))
    application.add_handler(CommandHandler("count", commands.twitter_count))
    application.add_handler(CommandHandler("draw", commands.twitter_draw))
    application.add_handler(CommandHandler("raid", commands.twitter_raid))
    application.add_handler(CommandHandler(["spaces", "space"], commands.twitter_spaces))
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
    application.add_handler(CommandHandler("voting", commands.voting))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler("wallet", commands.wallet))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(CommandHandler("word", commands.word))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto.replies))

    job_queue.run_repeating(
        auto.auto_message_endorsement,
        times.endorse_time,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Endorsement Message",
    )
    
    job_queue.run_repeating(
        auto.auto_message_volume,
        times.volume_time,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        first=10800,
        name="Volume Message",
    )

    job_queue.run_once(
        auto.auto_message_click,
        times.button_time(),
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Click Message",
    )

    scanner()
    application.run_polling()
