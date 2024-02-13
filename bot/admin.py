import os
import re
import random
import time as t
from datetime import datetime, timedelta, timezone

import pytz
from gtts import gTTS
import requests
import textwrap
import wikipediaapi
from web3 import Web3
from telegram import *
from telegram.ext import *
from translate import Translator
from eth_utils import to_checksum_address
from PIL import Image, ImageDraw, ImageFont

from hooks import dune, db, api
import media
from constants import ca, loans, nfts, tax, url, dao, mappings
from variables import times, giveaway, text


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        if len(context.args) == 4:
            ticker = context.args[0]
            pair = context.args[1]
            ca = context.args[2]
            chain = context.args[3]
            image_url = api.get_token_image(ca, chain)
            if image_url:
                image_url = image_url
            else:
                image_url = "None"
            try:
                db.token_add(ticker, pair, ca, chain, image_url)
                await update.message.reply_text(f"{ticker.upper()} Sucessfully added to @X7Finance_bot")
            except Exception:
                await update.message.reply_text(f"Error adding {ticker.upper()} Please try again.")


        else:
            await update.message.reply_text(f"use /add [ticker] [pair] [ca] [chain]")

    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        if len(context.args) == 2:
            ticker = context.args[0]
            chain = context.args[1]
            try:
                db.token_delete(ticker, chain)
                await update.message.reply_text(f"{ticker.upper()} ({chain.upper()}) Sucessfully deleted from @X7Finance_bot")
            except Exception:
                await update.message.reply_text(f"Error deleteing {ticker.upper()} ({chain.upper()}) Please try again.")
        else:
            await update.message.reply_text(f"use /add [ticker] [chain]")
    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")


async def reset_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        db.clicks_reset()
    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")


async def wen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        if times.BUTTON_TIME is not None:
            time = times.BUTTON_TIME
        else:    
            time = times.FIRST_BUTTON_TIME
        target_timestamp = times.RESTART_TIME + time
        time_difference_seconds = target_timestamp - datetime.now().timestamp()
        time_difference = timedelta(seconds=time_difference_seconds)
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await update.message.reply_text(f"Next Click Me:\n\n{hours} hours, {minutes} minutes, {seconds} seconds\n\n"
        )
    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")