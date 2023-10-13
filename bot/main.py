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

import commands
import games
import admin
import twitter

from data import times, url, ca, text
from api import index as api
from media import index as media

current_button_data = None
clicked_buttons = set()
first_user_clicked = False


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
        button_click_timestamp = t.time()
        time_taken = button_click_timestamp - button_generation_timestamp
        await api.clicks_update(user_info)
        user_clicks = api.db_clicks_get_user_total(user_info)
        if not first_user_clicked:
            first_user_clicked = True
            total_click_count = api.db_clicks_get_total()
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
            if total_click_count % text.burn_increment == 0:
                try:
                    alchemy_keys = os.getenv("ALCHEMY_ETH")
                    alchemy_eth_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_keys}"
                    w3 = Web3(Web3.HTTPProvider(alchemy_eth_url))
                    sender_address = os.getenv("BURN_WALLET")
                    recipient_address = ca.dead
                    token_contract_address = ca.x7r
                    sender_private_key = os.getenv("BURN_WALLET_PRIVATE_KEY")
                    amount_to_send_tokens = 100
                    decimals = 18  
                    amount_to_send_wei = amount_to_send_tokens * (10 ** decimals)

                    token_transfer_data = (
                        '0xa9059cbb'
                        + recipient_address[2:].rjust(64, '0')
                        + hex(amount_to_send_wei)[2:].rjust(64, '0')
                    )

                    transaction = {
                        'from': sender_address,
                        'to': token_contract_address,
                        'data': token_transfer_data,
                        'gasPrice': w3.to_wei('50', 'gwei'),
                    }
                    
                    gas_estimate = w3.eth.estimate_gas(transaction)
                    nonce = w3.eth.get_transaction_count(sender_address)
                    transaction['gas'] = gas_estimate
                    transaction['nonce'] = nonce
                    signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
                    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                    burn_message = f"{amount_to_send_tokens} X7R Burnt\n\n{url.ether_tx}{tx_hash.hex()}"
                except Exception as e:
                        burn_message = f'Error burning X7R: {e}'
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"🔥🔥🔥🔥🔥🔥🔥🔥\n\n"
                        f"The button has been clicked a total of {total_click_count} times by all Pioneers!\n\n"
                        f"{burn_message}"
                )
                
        times.restart_time = datetime.now().timestamp()        
        context.user_data["current_button_data"] = None
        random_time = times.random_button_time()
        job_queue.run_once(
        auto_message_click,
        random_time,
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


application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
job_queue = application.job_queue


if __name__ == "__main__":
    application.add_error_handler(error)

    ## COMANDS ##
    application.add_handler(CommandHandler("about", commands.about))
    application.add_handler(CommandHandler("alerts", commands.alerts))
    application.add_handler(CommandHandler(["rollout", "multichain", "airdrop"], commands.airdrop))
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
    application.add_handler(CommandHandler("loan_id", commands.loan))
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
    application.add_handler(CommandHandler("word", commands.word))
    application.add_handler(CommandHandler(["whitepaper", "wp", "wpquote"], commands.wp))

    ## TWITTER ##
    application.add_handler(CommandHandler(["twitter", "x"], twitter.tweet))
    application.add_handler(CommandHandler("count", twitter.count))
    application.add_handler(CommandHandler("draw", twitter.draw))
    application.add_handler(CommandHandler("raid", twitter.raid))
    application.add_handler(CommandHandler(["spaces", "space"], twitter.spaces))

    ## GAMES ##
    application.add_handler(CommandHandler("ascii", games.ascii))
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

    ## ADMIN ##
    application.add_handler(CommandHandler(["admin_commands", "admin", "admincommands"], admin.admin_command))
    application.add_handler(CommandHandler("lock_games", admin.games_lock))
    application.add_handler(CommandHandler("unlock_games", admin.games_unlock))
    application.add_handler(CommandHandler("wen", admin.wen))

    ## AUTO ##
    application.add_handler(CallbackQueryHandler(clicks_function))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_replies))

    job_queue.run_repeating(
        auto_message_info,
        times.auto_message_time,
        #chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        first=times.auto_message_time,
        name="Auto Message",
    )

    job_queue.run_once(
        auto_message_click,
        times.button_time,
        chat_id=os.getenv("MAIN_TELEGRAM_CHANNEL_#ID"),
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
    application.run_polling()
