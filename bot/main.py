import os
import sys
import time as t
import subprocess
import sentry_sdk
from telegram import *
from telegram.ext import *
import auto
import commands
import games
import admin
import twitter

from data import times
from api import index as api


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
        "scanner/bsc.py",
        "scanner/eth.py",
        "scanner/arb.py",
        "scanner/poly.py",
        "scanner/opti.py",
##        "scanner/base.py",
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
    application.add_handler(CallbackQueryHandler(auto.clicks))

    application.add_handler(CommandHandler("about", commands.about))
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
    application.add_handler(CommandHandler(["fee", "fees"], commands.fees))
    application.add_handler(CommandHandler(["fg", "feargreed"], commands.fg))
    application.add_handler(CommandHandler("gas", commands.gas))
    application.add_handler(CommandHandler("games", commands.games))
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
    application.add_handler(CommandHandler("locks", commands.locks))
    application.add_handler(CommandHandler("me", commands.me))
    application.add_handler(CommandHandler("magisters", commands.magisters))
    application.add_handler(CommandHandler(["mcap", "marketcap", "cap"], commands.mcap))
    application.add_handler(CommandHandler("media", commands.media_command))
    application.add_handler(CommandHandler("mods", commands.mods))
    application.add_handler(CommandHandler(["nft", "nfts"], commands.nft))
    application.add_handler(CommandHandler(["on_chain", "onchain", "message"], commands.on_chain))
    application.add_handler(CommandHandler(["pair", "pairs"], commands.pair))
    application.add_handler(CommandHandler("pfp", commands.pfp))
    application.add_handler(CommandHandler("ping", commands.ping))
    application.add_handler(CommandHandler("pioneer", commands.pioneer))
    application.add_handler(CommandHandler(["pool", "lpool", "lendingpool"], commands.pool))
    application.add_handler(CommandHandler(["price", "prices", "x"], commands.price))
    application.add_handler(CommandHandler("logo", commands.price_logo))
    application.add_handler(CommandHandler("proposal", commands.proposal))
    application.add_handler(CommandHandler("quote", commands.quote))
    application.add_handler(CommandHandler(["referral", "refer"], commands.refer))
    application.add_handler(CommandHandler("router", commands.router))
    application.add_handler(CommandHandler("say", commands.say))
    application.add_handler(CommandHandler("scan", commands.scan))
    application.add_handler(CommandHandler("search", commands.search))
    application.add_handler(CommandHandler("signers", commands.signers))
    application.add_handler(CommandHandler("smart", commands.smart))
    application.add_handler(CommandHandler("snapshot", commands.snapshot))
    application.add_handler(CommandHandler(["split", "splitters", "splitter"], commands.splitters))
    application.add_handler(CommandHandler("supply", commands.supply))
    application.add_handler(CommandHandler(["beta", "swap", "xchange", "dex"], commands.swap))
    application.add_handler(CommandHandler(["tax", "slippage"], commands.tax_command))
    application.add_handler(CommandHandler("test", commands.test))
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
    application.add_handler(CommandHandler("voting", commands.voting))
    application.add_handler(CommandHandler("wei", commands.wei))
    application.add_handler(CommandHandler("wallet", commands.wallet))
    application.add_handler(CommandHandler(["website", "site"], commands.website))
    application.add_handler(CommandHandler("word", commands.word))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))

    application.add_handler(CommandHandler(["twitter", "x"], twitter.tweet))
    application.add_handler(CommandHandler("count", twitter.count))
    application.add_handler(CommandHandler("draw", twitter.draw))
    application.add_handler(CommandHandler("raid", twitter.raid))
    application.add_handler(CommandHandler(["spaces", "space"], twitter.spaces))

    application.add_handler(CommandHandler("coinflip", games.coinflip))
    application.add_handler(CommandHandler("roll", games.start_roll))

    guess_conversation = ConversationHandler(entry_points=[CommandHandler('guess', games.guess)],
    states={games.PLAYING_GUESS: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.guess_game)],},
    fallbacks=[CommandHandler('cancel_guess', games.guess_cancel)])
    application.add_handler(guess_conversation)

    rps_conversation = ConversationHandler(entry_points=[CommandHandler('rps', games.rps)],
    states={games.PLAYING_RPS: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.rps_game)],},
    fallbacks=[CommandHandler('cancel_rps', games.rps_cancel)])
    application.add_handler(rps_conversation)

    hangman_conversation = ConversationHandler(entry_points=[CommandHandler('hangman', games.hangman)],
    states={games.PLAYING_HANGMAN: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.hangman_game)],},
    fallbacks=[CommandHandler('cancel_hangman', games.hangman_cancel)])
    application.add_handler(hangman_conversation)

    scramble_conversation = ConversationHandler(entry_points=[CommandHandler('scramble', games.scramble)],
    states={games.PLAYING_SCRAMBLE: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.scramble_game)],},
    fallbacks=[CommandHandler('cancel_scramble', games.scramble_cancel)])
    application.add_handler(scramble_conversation)

    puzzle_conversation = ConversationHandler(entry_points=[CommandHandler('puzzle', games.puzzle)],
    states={games.PLAYING_PUZZLE: [MessageHandler(filters.Regex(r'^(up|down|left|right)$'), games.puzzle_game)]},
    fallbacks=[CommandHandler('cancel_scramble', games.puzzle_cancel)])
    application.add_handler(puzzle_conversation)

    emoji_conversation = ConversationHandler(entry_points=[CommandHandler('emoji', games.emoji)],
    states={games.PLAYING_EMOJI: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.emoji_game)]},
    fallbacks=[CommandHandler('cancel_emoji', games.emoji_cancel)])
    application.add_handler(emoji_conversation)

    riddle_conversation = ConversationHandler(entry_points=[CommandHandler('riddle', games.riddle)],
    states={games.PLAYING_RIDDLE: [MessageHandler(filters.TEXT & (~filters.COMMAND), games.riddle_game)]},
    fallbacks=[])
    application.add_handler(riddle_conversation)

    application.add_handler(CommandHandler(["admin_commands", "admin", "admincommands"], admin.admin_command))
    application.add_handler(CommandHandler("lock_games", admin.games_lock))
    application.add_handler(CommandHandler("unlock_games", admin.games_unlock))

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto.replies))

    job_queue.run_repeating(
        auto.auto_message_info,
        times.auto_message_time,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        first=times.auto_message_time,
        name="Auto Message",
    )

    job_queue.run_once(
        auto.auto_message_click,
        times.button_time(),
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        name="Click Message",
    )

    scanner()
    application.run_polling()
