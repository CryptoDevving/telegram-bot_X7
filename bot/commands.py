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


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.ABOUT}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.XCHANGE}")],
                [InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}")],
            ]
        ),
    )


async def airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker=media.CHAINS)
    await update.message.reply_text(
        f"{text.AIRDROP}\n\n"
        f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="XChange Alerts", url=f"{url.TG_ALERTS}")],
            ]
        ),
    )


async def alumni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Alumni*\n\n{text.ALUMNI}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def announcements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption="\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Announcement Channel",
                        url="https://t.me/X7announcements",
                    )
                ],
            ]
        ),
    )


async def ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    def get_ath_info(coin):
        ath, ath_change, date = api.get_ath(coin)
        ath_change_str = f"{ath_change}"
        return ath, ath_change_str[:3], date
    
    try:
        x7r_ath, x7r_ath_change, x7r_date = get_ath_info("x7r")
        x7dao_ath, x7dao_ath_change, x7dao_date = get_ath_info("x7dao")
        
        x7dao_date_object = datetime.fromisoformat(x7dao_date.replace("Z", "+00:00"))
        x7dao_readable_date = x7dao_date_object.strftime("%Y-%m-%d %H:%M:%S")
        x7dao_mcap = x7dao_ath * ca.SUPPLY

        x7r_date_object = datetime.fromisoformat(x7r_date.replace("Z", "+00:00"))
        x7r_readable_date = x7r_date_object.strftime("%Y-%m-%d %H:%M:%S")
        x7r_mcap = x7r_ath * api.get_x7r_supply("eth")

        x7r_ath = (
            f'${x7r_ath} (${"{:0,.0f}".format(x7r_mcap)})\n'
            f'{x7r_ath_change}%\n'
            f'{x7r_readable_date}'
            )
        x7dao_ath = (
            f'${x7dao_ath} (${"{:0,.0f}".format(x7dao_mcap)})\n'
            f'{x7dao_ath_change}%\n'
            f'{x7dao_readable_date}'
            )
    except Exception:
        x7dao_ath = "Unavaliable"
        x7r_ath = "Unavaliable"

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption = 
            f"*X7 Finance ATH Info*\n\n"
            f'*X7R*\n'
            f'{x7r_ath}\n\n'
            f'*X7DAO*\n'
            f'{x7dao_ath}\n\n'
            f"{api.get_quote()}",
        parse_mode="Markdown"
    )


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = " ".join(context.args)
    if not input:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance DAO*\n\n"
                "Follow the /bio command with a few sentences about yourself to be uploaded to x7finance.org/community/meetthedao\n\n"
                "No more than 230 characters\n\nNew entries will be uploaded every 3/4 days\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown"
        )
    elif len(input) > 230:
        await update.message.reply_text(
            f"Your bio exceeds the maximum character limit of 230 characters, please resubmit")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    else:
        user = update.effective_user
        user_info = user.username or f"{user.first_name} {user.last_name}"
        await context.bot.send_message(
            chat_id=os.getenv("BIO_TELEGRAM_CHANNEL_ID"),
            text=f"{user.first_name}\nhttps://t.me/{user.username}\n\n{input}",
            disable_web_page_preview="true",
            )
        await update.message.reply_text(
            f"Thanks {user_info}, Your bio has been submitted")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


async def blocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    time = round(t.time())
    block_types = ["eth", "arb", "bsc", "poly", "opti", "base"]
    blocks = {block_type: api.get_block(block_type, time) for block_type in block_types}
    blocks_text = "\n".join([f"{block_type.upper()}: {block}" for block_type, block in blocks.items()])
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*Latest Blocks*\n\n"
            f"{blocks_text}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown"
    )


async def blog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Finance Blog", url=f"{url.WEBSITE}blog"
                    )
                ],
            ]
        ),
    )


async def bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{text.COMMANDS}")


async def burn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7R:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7R[chain]
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    burn = api.get_token_balance(ca.DEAD, ca.X7R, chain)
    percent = round(burn / ca.SUPPLY * 100, 2)
    burn_dollar = api.get_price(ca.X7R, chain) * float(burn)
    im2 = Image.open(media.X7R_LOGO)
    native = f"{str(burn_dollar / api.get_native_price(chain_native))[:5]} {chain_native.upper()}"
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7R {chain_name} Tokens Burned:\n\n"
            f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
            f"{percent}% of Supply\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 28),
        fill =(255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"\n\nX7R {chain_name} Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n"
            f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
            f"{percent}% of Supply\n\n"
            f"{api.get_quote()}",
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Burn Wallet",
                        url=f"{chain_url}{ca.X7R}?a={ca.DEAD}",
                    )
                ],
            ]
        ),
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].xchange
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Buy Links {chain_name}*\nUse `/buy [chain-name]` for other chains\n"
            f"Use `/constellations` for constellations\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R - Rewards Token", url=f"{chain_url}{ca.X7R}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO - Governance Token", url=f"{chain_url}{ca.X7DAO}"
                    )
                ],
            ]
        ),
    )


async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(
                text="Community Chat", url="https://t.me/X7m105portal"
            ),
            InlineKeyboardButton(
                text="Announcements", url="https://t.me/X7announcements"
            ),
        ],
        [
            InlineKeyboardButton(
                text="DAO Proposers Chat", url=f"{url.TG_DAO}",
            ),
            InlineKeyboardButton(
                text="Xchange Alerts", url="https://t.me/x7_alerts"
            ),
        ],
        [
            InlineKeyboardButton(
                text="LP Providers", url="https://t.me/x7financeLPs"
            ),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].dext
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Chart Links* {chain_name}\nUse `/chart [chain-name]` for other chains\n"
            f"Use `/constellations` for constellations\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R - Rewards Token", url=f"{chain_url}{ca.X7R}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO - Governance Token",
                        url=f"{chain_url}{ca.X7DAO}",
                    )
                ],
            ]
        ),
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first = context.args[0]
    second = context.args[1]
    if first == second:
        reply = "✅ Both inputs match"
    else:
        reply = "❌ Inputs do not match"
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Input Checker*\n\n"
            f"First:\n{first}\n\n"
            f"Second:\n{second}\n\n"
            f"{reply}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown")


async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        token_names = {
            "x7r": {"contract": ca.X7R, "image": media.X7R_LOGO},
            "x7dao": {"contract": ca.X7DAO, "image": media.X7DAO_LOGO},
            "x7101": {"contract": ca.X7101, "image": media.X7101_LOGO},
            "x7102": {"contract": ca.X7102, "image": media.X7102_LOGO},
            "x7103": {"symbol": ca.X7103, "image": media.X7103_LOGO},
            "x7104": {"contract": ca.X7104, "image": media.X7104_LOGO},
            "x7105": {"contract": ca.X7105, "image": media.X7105_LOGO},
        }

        x7token = context.args[0].lower()
        token2 = context.args[1].lower()
        search = api.get_cg_search(token2)
        token_id = search["coins"][0]["api_symbol"]
        thumb = search["coins"][0]["large"]

        if x7token in token_names:
            token_info = token_names[x7token]
            x7_price = api.get_price(token_info["contract"], "eth")
            image = token_info["image"]
            token_market_cap = api.get_mcap(token_id)
            if token_market_cap == 0:
                await update.message.reply_photo(
                    photo=api.get_random_pioneer(),
                    caption=
                        f"*X7 Finance Market Cap Comparison*\n\n"
                        f"No Market Cap data found for {token2.upper()}\n\n"
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                )
            if x7token == ca.X7R:
                x7_supply = api.get_x7r_supply("eth")
            else:
                x7_supply = ca.SUPPLY
            x7_market_cap = x7_price * x7_supply
            percent = ((token_market_cap - x7_market_cap) / x7_market_cap) * 100
            x = (token_market_cap - x7_market_cap) / x7_market_cap
            token_value = token_market_cap / x7_supply
            img = Image.open(requests.get(thumb, stream=True).raw)
            result = img.convert("RGBA")
            result.save(r"media/tokenlogo.png")
            im1 = Image.open((random.choice(media.BLACKHOLE)))
            im2 = Image.open(r"media/tokenlogo.png")
            im2_resized = im2.resize((200, 200))
            im3 = Image.open(image)
            im1.paste(im2_resized, (680, 20), im2_resized)
            im1.paste(im3, (680, 200), im3)
            i1 = ImageDraw.Draw(im1)
            i1.text(
                (28, 36),
                f"X7 Finance Market Cap Comparison\n\n"
                f"{context.args[1].upper()} Market Cap:\n"
                f'${"{:,.2f}".format(token_market_cap)}\n\n'
                f'Token value of {context.args[0].upper()} at {context.args[1].upper()} Market Cap:\n'
                f'${"{:,.2f}".format(token_value)}\n'
                f'{"{:,.0f}%".format(percent)}\n'
                f'{"{:,.0f}x".format(x)}\n\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font = ImageFont.truetype(media.FONT, 28),
                fill = (255, 255, 255),
            )
            im1.save(r"media/blackhole.png", quality=95)
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=
                    f"*X7 Finance Market Cap Comparison*\n\n"
                    f"{context.args[1].upper()} Market Cap:\n"
                    f'${"{:,.2f}".format(token_market_cap)}\n\n'
                    f'Token value of {context.args[0].upper()} at {context.args[1].upper()} Market Cap:\n'
                    f'${"{:,.2f}".format(token_value)}\n'
                    f'{"{:,.0f}%".format(percent)}\n'
                    f'{"{:,.0f}x".format(x)}\n\n'
                    f'{api.get_quote()}',
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{context.args[1].upper()} Chart",
                                url=f"https://www.coingecko.com/en/coins/{token_id}",
                            )
                        ],
                    ]
                ),
            )
        else:
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Market Cap Comparison*\n\n"
                    f"Please enter X7 token first followed by token to compare\n\n"
                    f"ie. `/compare x7r uni`\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )
    except IndexError:
        await update.message.reply_text("Comparison not avaliable, please try again.")


async def constellations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    price = api.get_cg_price("x7101, x7102, x7103, x7104, x7105")
    x7101mc = price["x7101"]["usd"] * ca.SUPPLY
    x7102mc = price["x7102"]["usd"] * ca.SUPPLY
    x7103mc = price["x7103"]["usd"] * ca.SUPPLY
    x7104mc = price["x7104"]["usd"] * ca.SUPPLY
    x7105mc = price["x7105"]["usd"] * ca.SUPPLY
    const_mc = x7101mc + x7102mc + x7103mc + x7104mc + x7105mc
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    if chain == "":
        img = Image.open((random.choice(media.BLACKHOLE)))
        i1 = ImageDraw.Draw(img)
        i1.text(
            (28, 36),
            f"X7 Finance Constellation Token Prices (ETH)\n\n"
            f'X7101:      ${price["x7101"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n\n'
            f'X7102:      ${price["x7102"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n\n'
            f'X7103:      ${price["x7103"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 20),
            fill =(255, 255, 255),
        )
        i1.text(
            (522, 90),
            f'X7104:      ${price["x7104"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n\n'
            f'X7105:      ${price["x7105"]["usd"]}\n'
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
            f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n\n'
            f'Combined Market Cap:\n${"{:0,.0f}".format(const_mc)}\n',
            font = ImageFont.truetype(media.FONT, 20),
            fill=(255, 255, 255),
        )
        img.save(r"media/blackhole.png")
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Constellation Token Prices (ETH)*\n\n"
                f"For more info use `/x7token-name`\n\n"
                f'X7101:      ${price["x7101"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n'
                f"CA: `{ca.X7101}\n\n`"
                f'X7102:      ${price["x7102"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n'
                f"CA: `{ca.X7102}\n\n`"
                f'X7103:      ${price["x7103"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n'
                f"CA: `{ca.X7103}\n\n`"
                f'X7104:      ${price["x7104"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n'
                f"CA: `{ca.X7104}\n\n`"
                f'X7105:      ${price["x7105"]["usd"]}\n'
                f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n'
                f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n'
                f"CA: `{ca.X7105}\n\n`"
                f'Combined Market Cap: ${"{:0,.0f}".format(const_mc)}\n\n'
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )


async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Contract Addresses for all chains*\n\n"
            f"*X7R - Rewards Token *\n`{ca.X7R}`\n\n"
            f"*X7DAO - Governance Token*\n`{ca.X7DAO}`\n\n"
            f"For advanced trading and arbitrage opportunities see `/constellations`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 2:
        amount = context.args[0]
        token = context.args[1]
        if token.lower() in ["eth", "bnb", "matic"]:
            price = api.get_native_price(token.lower()) / 1**18
        elif token.lower() in ["x7r", "x7dao", "x7101", "x7102", "x7103", "x7104", "x7105"]:
            cg = api.get_cg_price(token)
            price = cg[token.lower()]['usd']
        else:
            await update.message.reply_text("Please follow command with amount and token name: X7 Tokens or ETH, BNB, MATIC")
            return
    output = float(amount) * float(price)
    
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Price Conversion*\n\n"
            f"{amount} {token.upper()} is worth ${'{:0,.0f}'.format(output )}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown"
        )


async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        duration = times.COUNTDOWN_TIME - datetime.utcnow()
        days, hours, minutes = api.get_duration_days(duration)
        if duration < timedelta(0):
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Countdown*\n\nNo countdown set, Please check back for more details\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )
            return
        await update.message.reply_text(
            text=f"*X7 Finance Countdown:*\n\n"
            f'{times.COUNTDOWN_TITLE}\n\n{times.COUNTDOWN_TIME.strftime("%A %B %d %Y %I:%M %p")} UTC\n\n'
            f"{days} days, {hours} hours and {minutes} minutes\n\n"
            f"{times.COUNTDOWN_DESC}\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )


async def dao_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_contract = " ".join(context.args).lower()
    contract_names = list(dao.CONTRACT_MAPPINGS.keys())
    formatted_contract_names = '\n'.join(contract_names)
    if input_contract == "list":
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance DAO*\n\nUse `/dao contract-name` for a list of DAO callable functions\n\n"
                f"*Contract Names:*\n\n{formatted_contract_names}\n\n",
            parse_mode="Markdown",
            )
        return
    if not input_contract:
        snapshot = api.get_snapshot()
        end = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        start = datetime.utcfromtimestamp(
            snapshot["data"]["proposals"][0]["start"]
        ).strftime("%Y-%m-%d %H:%M:%S")
        then = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"])
        duration = then - datetime.utcnow()
        days, hours, minutes = api.get_duration_days(duration)
        if duration < timedelta(0):
            countdown = "Vote Closed"
            caption = "View"
        else:
            countdown = f"Vote Closing in: {days} days, {hours} hours and {minutes} minutes"
            caption = "Vote"
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance DAO*\n\n"
                f'use `/dao list` for a list of call callable contracts\n\n'
                f'*Latest Proposal:*\n\n'
                f'{snapshot["data"]["proposals"][0]["title"]} by - '
                f'{snapshot["data"]["proposals"][0]["author"][-5:]}\n\n'
                f"Voting Start: {start} UTC\n"
                f"Voting End:   {end} UTC\n\n"
                f'{snapshot["data"]["proposals"][0]["choices"][0]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][0])} DAO Votes\n'
                f'{snapshot["data"]["proposals"][0]["choices"][1]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][1])} DAO Votes\n\n'
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores_total"])} Total DAO Votes\n\n'
                f"{countdown}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"{caption} Here",
                            url=f"{url.SNAPSHOT}/proposal/"
                            f'{snapshot["data"]["proposals"][0]["id"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text=f"DAO Proposers Chat",
                            url=f"{url.TG_DAO}",
                        )
                    ],
                ]
            ),
        )
        
        return
    matching_contract = None
    for contract in dao.CONTRACT_MAPPINGS:
        if contract.lower() == input_contract:
            matching_contract = contract
            break
    if matching_contract:
        contract_text, contract_ca = dao.CONTRACT_MAPPINGS[contract]
        await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance DAO Functions*\n"
            f"{contract}\n\n"
            f"The following functions can be called on the {contract} contract:\n\n"
            f"{contract_text}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Contract", url=f"{url.ETHER_ADDRESS}{contract_ca}")],
            ]
        ),
    )
    else:
        contract_names = list(dao.CONTRACT_MAPPINGS.keys())
        formatted_contract_names = '\n'.join(contract_names)
        await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance DAO Functions*\n\n"
            f"'{input_contract}' not found\nPlease choose from the following\n\n"
            f"*Contract Names:*\n\n{formatted_contract_names}",
        parse_mode="Markdown")


async def deployer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    tx = api.get_tx(ca.DEPLOYER, "eth")
    time = datetime.utcfromtimestamp(int(tx["result"][0]["timeStamp"]))
    duration = datetime.utcnow() - time
    days, hours, minutes = api.get_duration_days(duration)
    if (
        f'{tx["result"][0]["to"]}'.lower()
        == "0x000000000000000000000000000000000000dead"
    ):
        message = bytes.fromhex(tx["result"][0]["input"][2:]).decode("utf-8")
        await update.message.reply_text(
            f"*Last On Chain Message:*\n\n{time} UTC\n"
            f"{days} days, {hours} hours and {minutes} minutes ago:\n\n"
            f"`{message}`\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{url.ETHER_TX}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains",
                            url=f"{url.WEBSITE}docs/onchains",
                        )
                    ],
                ]
            ),
        )
    else:
        name = tx["result"][0]["functionName"]
        if name == "":
            name = f'Transfer to:\n{tx["result"][0]["to"]}'
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*Deployer Wallet last TX*\n\n{time} UTC\n"
                f"{days} days, {hours} hours and {minutes} minutes ago:\n\n"
                f"`{name}`\n\n"
                f"This command will pull last TX on the X7 Finance deployer wallet."
                f" To view last on chain use `/on_chain`\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{url.ETHER_TX}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains",
                            url=f"{url.WEBSITE}docs/onchains",
                        )
                    ],
                ]
            ),
        )


async def discount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"*X7 Finance Discount*\n\n{text.DISCOUNT}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Lending Discount Contract",
                        url=f"{url.ETHER_ADDRESS}{ca.LENDING_DISCOUNT}#code",
                    )
                ],
            ]
        ),
    )


async def docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="Get Started", url=f"{url.WEBSITE}getstarted/"),
            InlineKeyboardButton(text="Trader", url=f"{url.WEBSITE}docs/guides/trade/"),
        ],
        [
            InlineKeyboardButton(text="Liquidity Provider", url=f"{url.WEBSITE}docs/guides/liquidity-provider/"),
            InlineKeyboardButton(text="Capital Allocator", url=f"{url.WEBSITE}docs/guides/lending/"),
        ],
        [
            InlineKeyboardButton(text="Project Engineer", url=f"{url.WEBSITE}docs/guides/integrate-ui/"),
            InlineKeyboardButton(text="Project Launcher", url=f"{url.WEBSITE}docs/guides/launch/"),

        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def ebb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        chain_native = mappings.CHAINS[chain].token
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    now = datetime.utcnow()
    def get_liquidity_data(hub_address):
        hub = api.get_internal_tx(hub_address, chain)
        hub_filter = [d for d in hub["result"] if d["from"] in f"{hub_address}".lower()]
        value_raw = int(hub_filter[0]["value"]) / 10**18
        value = round(value_raw, 3) 
        dollar = float(value) * float(api.get_native_price(chain_native)) / 1**18
        time = datetime.utcfromtimestamp(int(hub_filter[0]["timeStamp"]))
        duration = now - time
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = (remainder % 3600) // 60
        return value, dollar, time, days, hours, minutes

    (
        x7r_value,
        x7r_dollar,
        x7r_time,
        x7r_days,
        x7r_hours,
        x7r_minutes,
    ) = get_liquidity_data(ca.X7R_LIQ_HUB)
    (
        x7dao_value,
        x7dao_dollar,
        x7dao_time,
        x7dao_days,
        x7dao_hours,
        x7dao_minutes,
    ) = get_liquidity_data(ca.X7DAO_LIQ_HUB)
    (
        x7100_value,
        x7100_dollar,
        x7100_time,
        x7100_days,
        x7100_hours,
        x7100_minutes,
    ) = get_liquidity_data(ca.X7100_LIQ_HUB)
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Liquidity Hubs {chain_name}*\nUse `/ebb [chain-name]` for other chains\n\n"
            f'Last X7R Buy Back: {x7r_time} UTC\n{x7r_value} {chain_native.upper()} (${"{:0,.0f}".format(x7r_dollar)})\n'
            f"{x7r_days} days, {x7r_hours} hours and {x7r_minutes} minutes ago\n\n"
            f'Last X7DAO Buy Back: {x7dao_time} UTC\n{x7dao_value} {chain_native.upper()} (${"{:0,.0f}".format(x7dao_dollar)})\n'
            f"{x7dao_days} days, {x7dao_hours} hours and {x7dao_minutes} minutes ago\n\n"
            f'Last X7100 Buy Back: {x7100_time} UTC\n{x7100_value} {chain_native.upper()} (${"{:0,.0f}".format(x7100_dollar)})\n'
            f"{x7100_days} days, {x7100_hours} hours and {x7100_minutes} minutes ago\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7R Liquidity Hub", url=f"{chain_url}{ca.X7R_LIQ_HUB}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO Liquidity Hub",
                        url=f"{chain_url}{ca.X7DAO_LIQ_HUB}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7100 Liquidity Hub",
                        url=f"{chain_url}{ca.X7100_LIQ_HUB}",
                    )
                ],
            ]
        ),
    )


async def ecosystem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.ECOSYSTEM}" f"\n\n{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{url.XCHANGE}")],
                [InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}")],
            ]
        ),
    )


async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*Fact!*\n\n"
            f"{api.get_fact()}",
        parse_mode="Markdown",
    )


async def factory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="ETH", url=f"{url.ETHER_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="BSC", url=f"{url.BSC_ADDRESS}{ca.FACTORY}"),
        ],
        [
            InlineKeyboardButton(text="Polygon", url=f"{url.POLY_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="Arbitrum", url=f"{url.ARB_ADDRESS}{ca.FACTORY}"),
        ],
        [
            InlineKeyboardButton(text="Optimism", url=f"{url.OPTI_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="Base", url=f"{url.BASE_ADDRESS}{ca.FACTORY}"),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(
                text="Airdrop Questions",
                url="https://www.x7finance.org/docs/faq/airdrop",
            ),
            InlineKeyboardButton(
                text="Constellation Tokens",
                url="https://www.x7finance.org/docs/faq/constellations",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Developer Questions",
                url="https://www.x7finance.org/docs/faq/devs",
            ),
            InlineKeyboardButton(
                text="General Questions",
                url="https://www.x7finance.org/docs/faq/general",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Governance Questions",
                url="https://www.x7finance.org/docs/faq/governance",
            ),
            InlineKeyboardButton(
                text="Investor Questions",
                url="https://www.x7finance.org/faq/investors",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Liquidity Lending Questions",
                url="https://www.x7finance.org/docs/faq/liquiditylending",
            ),
            InlineKeyboardButton(
                text="NFT Questions", url="https://www.x7finance.org/faq/nfts"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Snapshot.org Questions",
                url="https://www.x7finance.org/docs/faq/daosnapshot",
            ),
            InlineKeyboardButton(
                text="Xchange Questions",
                url="https://www.x7finance.org/faq/xchange",
            ),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def fees(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        chain_native = mappings.CHAINS[chain].token
        chain_tx = mappings.CHAINS[chain].scan_tx
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    now = datetime.utcnow()
    tx = api.get_tx(ca.FEE_TO, chain)
    filter = [d for d in tx["result"] if d["to"] in f"{ca.ECO_SPLITTER}".lower() and d.get("functionName", "") != "pushAll()"]
    value_raw = int(filter[0]["value"]) / 10**18
    hash = filter[0]["hash"]
    value = round(value_raw, 3) 
    dollar = float(value) * float(api.get_native_price(chain_native)) / 1**18
    time = datetime.utcfromtimestamp(int(filter[0]["timeStamp"]))
    duration = now - time
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes = (remainder % 3600) // 60
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Xchange Fee Liquidation {chain_name}*\nUse `/fees [chain-name]` for other chains\n\n"
            f'Last Liquidation: {time} UTC\n{value} {chain_native.upper()} (${"{:0,.0f}".format(dollar)})\n\n'
            f"{days} days, {hours} hours and {minutes} minutes ago\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Last Liquidation TX",
                        url=f"{chain_tx}{hash}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Liquidation Management Wallet",
                        url=f"{chain_url}0x7000e84af80f817010cf1a9c0d5f8df2a5da60dd",
                    )
                ],
            ]
        ),
    )


async def fg(update, context):
    fear_response = requests.get("https://api.alternative.me/fng/?limit=0")
    fear_data = fear_response.json()
    fear_values = []
    for i in range(7):
        timestamp = float(fear_data["data"][i]["timestamp"])
        localtime = datetime.fromtimestamp(timestamp)
        fear_values.append(
            (
                fear_data["data"][i]["value"],
                fear_data["data"][i]["value_classification"],
                localtime,
            )
        )
    duration_in_s = float(fear_data["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    caption = "*Market Fear and Greed Index*\n\n"
    caption += f'{fear_values[0][0]} - {fear_values[0][1]} - {fear_values[0][2].strftime("%A %B %d")}\n\n'
    caption += "Change:\n"
    for i in range(1, 7):
        caption += f'{fear_values[i][0]} - {fear_values[i][1]} - {fear_values[i][2].strftime("%A %B %d")}\n'
    caption += "\nNext Update:\n"
    caption += (
        f"{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}"
    )
    await update.message.reply_photo(
        photo="https://alternative.me/crypto/fear-and-greed-index.png",
        caption=caption,
        parse_mode="Markdown",
    )
   

async def gas(update, context):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].gas
        chain_logo = mappings.CHAINS[chain].logo
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    gas_data = api.get_gas(chain)
    im2 = Image.open(chain_logo)
    im1 = Image.open(random.choice(media.BLACKHOLE))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
            f"{chain_name} Gas Prices:\n\n"
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n\n\n\n\n\n\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 26),
        fill = (255, 255, 255),
    )
    im1.save("media/blackhole.png")
    await update.message.reply_photo(
        photo=open("media/blackhole.png", "rb"),
        caption=
            f"*{chain_name} Gas Prices:*\n"
            f"For other chains use `/gas [chain-name]`\n\n"
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n'
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n'
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n'
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f"{chain_name} Gas Tracker", url=chain_url)]]
        ),
    )


async def giveaway_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ext = " ".join(context.args)
    duration = giveaway.TIME - datetime.utcnow()
    days, hours, minutes = api.get_duration_days(duration)
    if duration < timedelta(0):
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7 Finance Giveaway is now closed\n\nPlease check back for more details"
                f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    else:
        if ext == "":
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*{giveaway.NAME}*\n\n{giveaway.TEXT}\n\n"
                    f"Ends:\n\n{giveaway.TIME.strftime('%A %B %d %Y %I:%M %p')} UTC\n\n"
                    f"{days} days, {hours} hours and {minutes} minutes\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )

        if ext == "entries":
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*{giveaway.NAME}*\n\n"
                    f"Entries for the {giveaway.NAME} are: (last 5 digits only):\n\n{api.get_giveaway_entries()}\n\n"
                    f"Last updated at:\n"
                    f"{giveaway.UPDATE.strftime('%A %B %d %Y %I:%M %p')} UTC\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )
        if ext == "run":
            chat_admins = await context.bot.get_chat_administrators(os.getenv("MAIN_TELEGRAM_CHANNEL_ID"))
            if update.effective_user in (admin.user for admin in chat_admins):
                winner_entries = list(api.get_giveaway_entries())
                winner = random.choice(winner_entries)
                await update.message.reply_photo(
                    photo=api.get_random_pioneer(),
                    caption=
                        f"*{giveaway.NAME}*\n\n"
                        f"The winner of the {giveaway.NAME} is: (last 5 digits only)\n\n"
                        f"{winner}\n\n"
                        f"Trust no one, trust code. Long live Defi!\n\n"
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                )
            else:
                await update.message.reply_text(f"{text.MODS_ONLY}")


async def holders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_logo = mappings.CHAINS[chain].logo
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    x7dao_holders = api.get_holders(ca.X7DAO, chain)
    x7r_holders = api.get_holders(ca.X7R, chain)
    x7d_holders = api.get_holders(ca.X7D, chain)
    
    im1 = Image.open(random.choice(media.BLACKHOLE))
    im2 = Image.open(chain_logo)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7 Finance Token Holders {chain_name}\n\n"
            f"X7R:   {x7r_holders}\n"
            f"X7DAO: {x7dao_holders}\n"
            f"X7D:   {x7d_holders}\n\n\n\n\n\n\n\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 26),
        fill = (255, 255, 255),
    )
    im1.save(r"media/blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*X7 Finance Token Holders {chain_name}*\n"
            f"For other chains use `/holders [chain-name]`\n\n"
            f"X7R:        {x7r_holders}\n"
            f"X7DAO:  {x7dao_holders}\n"
            f"X7D:        {x7d_holders}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "upload_photo")
    text = " ".join(context.args)
    img = Image.open((random.choice(media.BLACKHOLE)))
    i1 = ImageDraw.Draw(img)
    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=text)
    caption_new = ""
    for ii in word_list:
        caption_new = caption_new + ii + "\n"
    i1.text((50, img.size[1] / 8), caption_new, font=ImageFont.truetype(media.FONT, 28), fill=(255, 255, 255))
    img.save(r"media/blackhole.png")
    i1.text(
        (50, 460),
        f"{update.message.from_user.username}\n"
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 28),
        fill = (255, 255, 255),
    )
    img.save(r"media/blackhole.png")
    await update.message.reply_photo(photo=open(r"media/blackhole.png", "rb"))


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_response = requests.get("https://v2.jokeapi.dev/joke/Any?safe-mode")
    joke = joke_response.json()
    if joke["type"] == "single":
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=f'`{joke["joke"]}`',
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=f'`{joke["setup"]}\n\n{joke["delivery"]}`',
            parse_mode="Markdown",
        )


async def launch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    x7m105_duration = datetime.utcnow() - times.X7M105
    x7m105_years, x7m105_months, x7m105_weeks, x7m105_days = api.get_duration_years(x7m105_duration)
    migration_duration = datetime.utcnow() - times.MIGRATION
    migration_years, migration_months, migration_weeks, migration_days = api.get_duration_years(migration_duration)
    reply_message = f'*X7 Finance Launch Info*\n\nX7M105 Stealth Launch\n{times.X7M105.strftime("%A %B %d %Y %I:%M %p")} UTC\n'
    reply_message += f"{x7m105_years} years, {x7m105_months} months, {x7m105_weeks} weeks, and {x7m105_days} days ago\n\n"
    reply_message += f'V2 Migration\n{times.MIGRATION.strftime("%A %B %d %Y %I:%M %p")} UTC\n'
    reply_message += f"{migration_years} years, {migration_months} months, {migration_weeks} weeks, and {migration_days} days ago\n\n"
    reply_message += api.get_quote()
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=reply_message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7M105 Launch TX",
                        url=f"{url.ETHER_TX}0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Migration Go Live TX",
                        url=f"{url.ETHER_TX}0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41",
                    )
                ],
            ]
        ),
    )


async def leaderboard(update: Update, context: CallbackContext):
    board = db.clicks_get_leaderboard()
    click_counts_total = db.clicks_get_total()
    fastest = db.clicks_fastest_time()
    fastest_user = fastest[0]
    fastest_time = fastest[1]
    slowest = db.clicks_slowest_time()
    slowest_user = slowest[0]
    slowest_time = slowest[1]
    clicks_needed = times.BURN_INCREMENT - (click_counts_total % times.BURN_INCREMENT)
    streak = db.clicks_check_highest_streak()
    streak_user, streak_value = streak
    await update.message.reply_text(
        text=
            f"*X7 Finance Fastest Pioneer 2024 Leaderboard\n(Top 10)\n\n*"
            f"{api.escape_markdown(board)}\n"
            f"Total clicks: *{click_counts_total}*\n"
            f"Clicks till next X7R Burn: *{clicks_needed}*\n\n"
            f"Fastest Click:\n{fastest_time} seconds\nby {api.escape_markdown(fastest_user)}\n\n"
            f"Slowest Click:\n{slowest_time} seconds\nby {api.escape_markdown(slowest_user)}\n\n"
            f"{streak_user} clicked the button last and is on a *{streak_value}* click streak!",
        parse_mode="Markdown"
    )
    

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="Xchange App", url=f"{url.XCHANGE}"),
            InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}"),
        ],
        [
            InlineKeyboardButton(text="Snapshot", url=f"{url.SNAPSHOT}"),
            InlineKeyboardButton(text="Twitter", url=f"{url.TWITTER}"),
        ],
        [
            InlineKeyboardButton(text="Reddit", url=f"{url.REDDIT}"),
            InlineKeyboardButton(text="Youtube", url=f"{url.YOUTUBE}"),
        ],
        [
            InlineKeyboardButton(text="Github", url=f"{url.GITHUB}"),
            InlineKeyboardButton(text="Dune", url=f"{url.DUNE}"),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def liquidity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        chain_native = mappings.CHAINS[chain].token
        chain_logo = mappings.CHAINS[chain].logo
        pair_addresses = mappings.CHAINS[chain].pairs
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    im2 = Image.open(chain_logo)
    if chain == "eth":  ### REMOVE LINE AFTER MIGRATION
        token_liquidity = []
        weth_liquidity = []
        token_dollars = []
        weth_dollars = []

        for contract_address, pair in zip(ca.TOKENS, pair_addresses):
            token_price = api.get_price(contract_address, chain)
            liquidity_data = api.get_liquidity(pair, chain)
            token_liq = float(liquidity_data["reserve0"])
            weth_liq = float(liquidity_data["reserve1"]) / 10**18
            weth_dollar = weth_liq * float(api.get_native_price(chain_native))
            token_dollar = token_price * (token_liq / 10**18)

            token_liquidity.append(token_liq)
            weth_liquidity.append(weth_liq)
            token_dollars.append(token_dollar)
            weth_dollars.append(weth_dollar)

        constellations_tokens_liq = sum(token_liquidity[2:])
        constellations_weth_liq = sum(weth_liquidity[2:])
        constellations_weth_dollar = sum(weth_dollars[2:])
        constellations_token_dollar = sum(token_dollars[2:])

        x7r_token_liq = token_liquidity[0]
        x7r_weth_liq = weth_liquidity[0]
        x7r_token_dollar = token_dollars[0]
        x7r_weth_dollar = weth_dollars[0]

        x7dao_token_liq = token_liquidity[1]
        x7dao_weth_liq = weth_liquidity[1]
        x7dao_token_dollar = token_dollars[1]
        x7dao_weth_dollar = weth_dollars[1]

        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
                f"X7 Finance Token Liquidity {chain_name}\n\n"
                f"X7R\n"
                f'{"{:0,.0f}".format(x7r_token_liq)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7r_weth_liq)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                f"X7DAO\n"
                f'{"{:0,.0f}".format(x7dao_token_liq)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7dao_weth_liq)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
                f"Constellations\n"
                f'{"{:0,.0f}".format(constellations_tokens_liq)[:4]}M X7100 '
                f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
                f'{"{:0,.0f}".format(constellations_weth_liq)} WETH '
                f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar + constellations_token_dollar)}\n'
                f'\nUTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 20),
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Token Liquidity (ETH)*\n"
                f"To show initial liquidity for other chains, Use `/liquidity "
                f"[chain-name]`\n\n"
                f"*X7R*\n"
                f'{"{:0,.0f}".format(x7r_token_liq)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7r_weth_liq)} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)}\n\n'
                f"*X7DAO*\n"
                f'{"{:0,.0f}".format(x7dao_token_liq)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
                f'{"{:0,.0f}".format(x7dao_weth_liq)} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)}\n\n'
                f"*Constellations*\n"
                f'{"{:0,.0f}".format(constellations_tokens_liq)[:4]}M X7100 '
                f'(${"{:0,.0f}".format(constellations_token_dollar)})\n'
                f'{"{:0,.0f}".format(constellations_weth_liq)} WETH '
                f'(${"{:0,.0f}".format(constellations_weth_dollar)})\n'
                f'Total Liquidity ${"{:0,.0f}".format(constellations_weth_dollar + constellations_token_dollar)}\n\n'
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    ### REMOVE AFTER MIGRATION
    else:
        x7r_amount = api.get_native_balance(ca.X7R_LIQ_LOCK, chain)
        x7dao_amount = api.get_native_balance(ca.X7DAO_LIQ_LOCK, chain)
        cons_amount = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        native_price = api.get_native_price(chain_native)
        x7dao_dollar = (
            float(x7dao_amount) * float(native_price) / 1**18
        )
        x7r_dollar = (
            float(x7r_amount) * float(native_price) / 1**18
        )
        cons_dollar = (
            float(cons_amount) * float(native_price) / 1**18
        )
        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
                f"X7 Finance Initial Liquidity {chain_name}\n\n"
                f'X7R:\n{x7r_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} {chain_native.upper()} (${"{:0,.0f}".format(cons_dollar)})\n\n\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 26),
            fill=(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Initial Liquidity {chain_name}*\nUse `/liquidity [chain-name]` for other chains\n\n"
                f'X7R:\n{x7r_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} {chain_native.upper()} (${"{:0,.0f}".format(cons_dollar)})\n\n'
                f'{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7R Initial Liquidity",
                            url=f"{chain_url}{ca.X7R_LIQ_LOCK}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="X7DAO Initial Liquidity",
                            url=f"{chain_url}{ca.X7DAO_LIQ_LOCK}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="X7100 Initial Liquidity",
                            url=f"{chain_url}{ca.CONS_LIQ_LOCK}",
                        )
                    ],
                ]
            ),
        )


async def liquidate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        chain_web3 = mappings.CHAINS[chain].w3
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    contract = chain_web3.eth.contract(
        address=Web3.to_checksum_address(ca.LPOOL), abi=api.get_abi(ca.LPOOL, chain)
    )
    num_loans = contract.functions.nextLoanID().call()
    liquidatable_loans = 0
    results = []
    for loan_id in range(num_loans + 1):
        try:
            result = contract.functions.canLiquidate(int(loan_id)).call()
            if result == 1:
                liquidatable_loans += 1
                results.append(f"Loan ID {loan_id}")
        except Exception:
            continue

    liquidatable_loans_text = f"Total liquidatable loans: {liquidatable_loans}"
    output = "\n".join([liquidatable_loans_text] + results)
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Loan Liquidations {chain_name}*\nfor other chains use `/liquidate [chain-name]`\n\n"
            f"{output}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Lending Pool Contract",
                        url=f"{chain_url}{ca.LPOOL}#writeContract",
                    )
                ],
            ]
        ),
    )


async def loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        loan_id = context.args[0]
        chain = context.args[1].lower()
    else:
        await update.message.reply_text(
            f"Please use `/loan # chain` to see details",
            parse_mode="Markdown",
        )
        return
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_address_url = mappings.CHAINS[chain].scan_address
        chain_scan_url = mappings.CHAINS[chain].scan_token
        chain_native = mappings.CHAINS[chain].token
        chain_web3 = mappings.CHAINS[chain].w3
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    price = api.get_native_price(chain_native)
    address = to_checksum_address(ca.LPOOL)
    contract = chain_web3.eth.contract(address=address, abi=api.get_abi(ca.LPOOL, chain))
    liquidation_status = ""
    try:
        liquidation = contract.functions.canLiquidate(int(loan_id)).call()
        if liquidation != 0:
            reward = contract.functions.liquidationReward().call() / 10**18
            liquidation_status = (
                f"\n\n*Eligible For Liquidation*\n"
                f"Cost: {liquidation / 10 ** 18} {chain_native.upper()} "
                f'(${"{:0,.0f}".format(price * liquidation / 10 ** 18)})\n'
                f'Reward: {reward} {chain_native} (${"{:0,.0f}".format(price * reward)})'
            )
    except (Exception, TimeoutError, ValueError, StopAsyncIteration):
        pass
    liability = contract.functions.getRemainingLiability(int(loan_id)).call() / 10**18
    remaining = f'Remaining Liability:\n{liability} {chain_native.upper()} (${"{:0,.0f}".format(price * liability)})'
    schedule1 = contract.functions.getPremiumPaymentSchedule(int(loan_id)).call()
    schedule2 = contract.functions.getPrincipalPaymentSchedule(int(loan_id)).call()
    schedule_str = api.format_schedule(schedule1, schedule2, chain_native.upper())

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Initial Liquidity Loan - {loan_id} {chain_name}*\n\n"
            f"Payment Schedule UTC:\n{schedule_str}\n\n"
            f"{remaining}"
            f"{liquidation_status}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Token Contract",
                        url=f"{chain_scan_url}{contract.functions.loanToken(int(loan_id)).call()}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Borrower",
                        url=f"{chain_address_url}{contract.functions.loanBorrower(int(loan_id)).call()}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"X7 Lending Pool Contract",
                        url=f"{chain_address_url}{ca.LPOOL}#code",
                    )
                ],
            ]
        ),
    )


async def loans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loan_type = " ".join(context.args).lower()
    if loan_type == "":
        await update.message.reply_text(
            f"{loans.OVERVIEW}\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Finance Whitepaper", url=f"{url.WP_LINK}"
                        )
                    ],
                ]
            ),
        )
        return
    else:
        loan_types = {
            "ill001": (loans.ILL001_NAME, loans.ILL001_TERMS, ca.ILL001),
            "ill002": (loans.ILL002_NAME, loans.ILL002_TERMS, ca.ILL002),
            "ill003": (loans.ILL003_NAME, loans.ILL003_TERMS, ca.ILL003),
        }
        if loan_type in loan_types:
            loan_name, loan_terms, loan_ca = loan_types[loan_type]
            buttons = [
                [
                    InlineKeyboardButton(text="Ethereum", url=f"{url.ETHER_ADDRESS}{loan_ca}"),
                    InlineKeyboardButton(text="BSC", url=f"{url.BSC_ADDRESS}{loan_ca}"),
                ],
                [
                    InlineKeyboardButton(text="Polygon", url=f"{url.POLY_ADDRESS}{loan_ca}"),
                    InlineKeyboardButton(text="Arbitrum", url=f"{url.ARB_ADDRESS}{loan_ca}"),
                ],
                [
                    InlineKeyboardButton(text="Optimism", url=f"{url.OPTI_ADDRESS}{loan_ca}"),
                    InlineKeyboardButton(text="Base", url=f"{url.BASE_ADDRESS}{loan_ca}"),
                ],
            ]

            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=f"{loan_name}\n{loan_terms.generate_terms()}\n\n",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )

    if loan_type == "count":
        networks = {
            "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}",
            "ARB": f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}",
            "BSC": "https://bsc-dataseed.binance.org/",
            "POLY": f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}",
            "OPTI": f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}",
            "BASE": "https://mainnet.base.org"
        }
        contract_networks = {
            "ETH": "eth",
            "ARB": "arb",
            "BSC": "bsc",
            "POLY": "poly",
            "OPTI": "opti",
            "BASE": "base",
        }
        contract_instances = {}
        for network, web3_url in networks.items():
            web3 = Web3(Web3.HTTPProvider(web3_url))
            contract = web3.eth.contract(
                address=to_checksum_address(ca.LPOOL),
                abi=api.get_abi(ca.LPOOL, contract_networks[network]),
            )
            amount = contract.functions.nextLoanID().call() - 1
            contract_instances[network] = amount
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Loan Count*\n\n"
                f'`ETH:`       {contract_instances["ETH"]}\n'
                f'`BSC:`       {contract_instances["BSC"]}\n'
                f'`ARB:`       {contract_instances["ARB"]}\n'
                f'`POLY:`     {contract_instances["POLY"]}\n'
                f'`OPTI:`     {contract_instances["OPTI"]}\n'
                f'`BASE:`     {contract_instances["BASE"]}\n\n'
                f"`TOTAL:`   {sum(contract_instances.values())}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )


async def locks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"

    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        web3 = mappings.CHAINS[chain].w3
        x7r_pair = mappings.CHAINS[chain].pairs[0]
        x7dao_pair = mappings.CHAINS[chain].pairs[1]
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    def calculate_remaining_time(web3, contract, token_pair, now):
        timestamp = contract.functions.getTokenUnlockTimestamp(to_checksum_address(token_pair)).call()
        unlock_datetime = datetime.utcfromtimestamp(timestamp)
        time_remaining = unlock_datetime - now

        if unlock_datetime > now:
            time_remaining = unlock_datetime - now
            prefix = "in"
        else:
            time_remaining = now - unlock_datetime
            prefix = "ago"

        years = time_remaining.days // 365
        months = (time_remaining.days % 365) // 30
        days = (time_remaining.days % 365) % 30
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        weeks = days // 7
        days = days % 7

        remaining_time_str = f"{years} years, {months} months, {weeks} weeks, {days} days, {hours} hours, {minutes} minutes {prefix}"
        unlock_datetime_str = unlock_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

        return remaining_time_str, unlock_datetime_str
        
    address = to_checksum_address(ca.TIME_LOCK)
    contract = web3.eth.contract(address=address, abi=api.get_abi(ca.TIME_LOCK, chain))
    now = datetime.utcnow()

    x7r_remaining_time_str, x7r_unlock_datetime_str = calculate_remaining_time(web3, contract, x7r_pair, now)
    x7dao_remaining_time_str, x7dao_unlock_datetime_str = calculate_remaining_time(web3, contract, x7dao_pair, now)

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Liquidity Locks* {chain_name}\nfor other chains use `/locks [chain-name]`\n\n"
            f"*X7R Unlock Date:*\n{x7r_unlock_datetime_str}\n"
            f"{x7r_remaining_time_str}\n\n"
            f"*X7DAO Unlock Date*:\n{x7dao_unlock_datetime_str}\n"
            f"{x7dao_remaining_time_str}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Token Time Lock Contract",
                        url=f"{chain_url}{ca.TIME_LOCK}#readContract",
                    )
                ],
            ]
        ),
    )


async def magisters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_token
        chain_holders = mappings.CHAINS[chain].nft_holders
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return

    holders = api.get_nft_holder_count(ca.MAGISTER, chain_holders)
    response = api.get_nft_holder_list(ca.MAGISTER, chain)
    magisters = [holder["owner_of"] for holder in response["result"]]
    address = "\n\n".join(map(lambda x: f"`{x}`", magisters))
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Magister Holders {chain_name}*\n"
            f"Use `/magisters [chain-name]` or other chains\n\n"
            f"Holders - {holders}\n\n"
            f"{address}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Magister Holder List",
                        url=f"{chain_url}{ca.MAGISTER}#balances",
                    )
                ],
            ]
        ),
    )


async def mcap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    price = {}
    token_names = {
        ca.X7R: "X7R",
        ca.X7DAO: "X7DAO",
        ca.X7101: "X7101",
        ca.X7102: "X7102",
        ca.X7103: "X7103",
        ca.X7104: "X7104",
        ca.X7105: "X7105",
    }
    for token in ca.TOKENS:
        token_name = token_names.get(token, "Unknown Token")
        price[token] = api.get_price(token, chain)

    x7r_supply = api.get_x7r_supply(chain)

    caps = {}
    for token in ca.TOKENS:
        if token == ca.X7R:
            caps[token] = price[token] * x7r_supply
        else:
            caps[token] = price[token] * ca.SUPPLY
    cons_cap = sum(caps.values()) - caps[ca.X7R] - caps[ca.X7DAO]
    total_cap = sum(caps.values())
    im1 = Image.open(random.choice(media.BLACKHOLE))
    im2 = Image.open(media.ETH_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    market_cap_info = f"X7 Finance Market Cap Info {chain_name}\n\n"
    market_cap_info += f'X7R:     ${"{:0,.0f}".format(caps[ca.X7R])}\n'
    for token in ca.TOKENS:
        if token == ca.X7R:
            continue
        market_cap_info += f'{token_name}:   ${"{:0,.0f}".format(caps[token])}\n'
    market_cap_info += f'\nConstellations Combined:\n${"{:0,.0f}".format(cons_cap)}\n\n'
    market_cap_info += f'Total Token Market Cap:\n${"{:0,.0f}".format(total_cap)}\n\n'
    market_cap_info += (
        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}'
    )
    i1.text((28, 36), market_cap_info, font = ImageFont.truetype(media.FONT, 22), fill = (255, 255, 255))
    im1.save(r"media/blackhole.png")
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*X7 Finance Market Cap Info {chain_name}*\n\n"
            f'`X7R: `            ${"{:0,.0f}".format(caps[ca.X7R])}\n'
            f'`X7DAO:`         ${"{:0,.0f}".format(caps[ca.X7DAO])}\n'
            f'`X7101:`         ${"{:0,.0f}".format(caps[ca.X7101])}\n'
            f'`X7102:`         ${"{:0,.0f}".format(caps[ca.X7102])}\n'
            f'`X7103:`         ${"{:0,.0f}".format(caps[ca.X7103])}\n'
            f'`X7104:`         ${"{:0,.0f}".format(caps[ca.X7104])}\n'
            f'`X7105:`         ${"{:0,.0f}".format(caps[ca.X7105])}\n\n'
            f"`Constellations Combined:`\n"
            f'${"{:0,.0f}".format(cons_cap)}\n\n'
            f"`Total Token Market Cap:`\n"
            f'${"{:0,.0f}".format(total_cap)}\n\n'
            f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def me(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_data = db.clicks_get_by_name(user_info)
    clicks = user_data[0]
    fastest_time = user_data[1]
    streak = user_data[2]

    if streak != 0:
        streak_message = f"and currently on a *{streak}* click streak!"
    else:
        streak_message = ""    

    if fastest_time is None:
        message = f"*X7 Finance Fastest Pioneer Leaderboard*\n\n" \
                  f"{api.escape_markdown(user_info)}, You have been the Fastest Pioneer *{clicks}* times {streak_message}\n\n" \
                  f"Your fastest time has not been logged yet\n\n"
    else:
        message = f"*X7 Finance Fastest Pioneer Leaderboard*\n\n" \
                  f"{api.escape_markdown(user_info)}, You have been the Fastest Pioneer *{clicks}* times {streak_message}\n\n" \
                  f"Your fastest time is {fastest_time} seconds\n\n"

    await update.message.reply_text(
        text=message,
        parse_mode="Markdown"
    )


async def media_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(
                text="X7 Official Images", url="https://imgur.com/a/WEszZTa"
            ),
            InlineKeyboardButton(
                text="X7 Official Token Logos Pack 1",
                url="https://t.me/X7announcements/58",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Official Token Logos Pack 2",
                url="https://t.me/X7announcements/141",
            ),
            InlineKeyboardButton(
                text="X7 TG Sticker Pack 1",
                url="https://t.me/addstickers/x7financestickers",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 TG Sticker Pack 2",
                url="https://t.me/addstickers/X7finance",
            ),
            InlineKeyboardButton(
                text="X7 TG Sticker Pack 3",
                url="https://t.me/addstickers/x7financ",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 TG Sticker Pack 4",
                url="https://t.me/addstickers/GavalarsX7",
            ),
            InlineKeyboardButton(
                text="X7 Emojis Pack",
                url="https://t.me/addemoji/x7FinanceEmojis",
            ),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_os = mappings.CHAINS[chain].opensea
        chain_native = mappings.CHAINS[chain].token
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain_prices = nfts.NFT_PRICES()
    chain_counts = nfts.NFT_COUNTS()
    chain_floors = nfts.NFT_FLOORS()
    chain_discount = nfts.NFT_DISCOUNTS()

    eco_price = chain_prices.get(chain, {}).get("eco")
    liq_price = chain_prices.get(chain, {}).get("liq")
    dex_price = chain_prices.get(chain, {}).get("dex")
    borrow_price = chain_prices.get(chain, {}).get("borrow")
    magister_price = chain_prices.get(chain, {}).get("magister")

    eco_floor = chain_floors.get(chain, {}).get("eco")
    liq_floor = chain_floors.get(chain, {}).get("liq")
    dex_floor = chain_floors.get(chain, {}).get("dex")
    borrow_floor = chain_floors.get(chain, {}).get("borrow")
    magister_floor = chain_floors.get(chain, {}).get("magister")

    eco_count = chain_counts.get(chain, {}).get("eco")
    liq_count = chain_counts.get(chain, {}).get("liq")
    dex_count = chain_counts.get(chain, {}).get("dex")
    borrow_count = chain_counts.get(chain, {}).get("borrow")
    magister_count = chain_counts.get(chain, {}).get("magister")

    eco_discount = chain_discount.get("eco", {})
    liq_discount = chain_discount.get("liq", {})
    dex_discount = chain_discount.get("dex", {})
    borrow_discount = chain_discount.get("borrow", {})
    magister_discount = chain_discount.get("magister", {})

    eco_discount_text = "\n".join(
        [
            f"> {discount}% discount on {token}"
            for token, discount in eco_discount.items()
        ]
    )
    liq_discount_text = "\n".join(
        [
            f"> {discount}% discount on {token}"
            for token, discount in liq_discount.items()
        ]
    )
    dex_discount_text = "\n".join([f"> {discount}" for discount in dex_discount])
    borrow_discount_text = "\n".join([f"> {discount}" for discount in borrow_discount])
    magister_discount_text = "\n".join(
        [
            f"> {discount}% discount on {token}"
            for token, discount in magister_discount.items()
        ]
    )

    buttons = [
        [
            InlineKeyboardButton(text="Mint Here", url="https://x7.finance/x/nft/mint"),
            InlineKeyboardButton(text="OS - Ecosystem Maxi", url=f"{url.OS_ECO}{chain_os}"),
        ],
        [
            InlineKeyboardButton(text="OS - Liquidity Maxi", url=f"{url.OS_LIQ}{chain_os}"),
            InlineKeyboardButton(text="OS - DEX Maxi", url=f"{url.OS_DEX}{chain_os}"),
        ],
        [
            InlineKeyboardButton(text="OS - Borrowing Maxi", url=f"{url.OS_BORROW}{chain_os}"),
            InlineKeyboardButton(text="OS - Magister", url=f"{url.OS_MAGISTER}{chain_os}"),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*NFT Info {chain_name}*\nUse `/nft [chain-name]` for other chains\n\n"
            f"*Ecosystem Maxi*\n{eco_price}\n"
            f"Available - {500 - eco_count}\nFloor price - {eco_floor} {chain_native}\n"
            f"{eco_discount_text}\n\n"
            f"*Liquidity Maxi*\n{liq_price}\n"
            f"Available - {250 - liq_count}\nFloor price - {liq_floor} {chain_native}\n"
            f"{liq_discount_text}\n\n"
            f"*Dex Maxi*\n{dex_price}\n"
            f"Available - {150 - dex_count}\nFloor price - {dex_floor} {chain_native}\n"
            f"{dex_discount_text}\n\n"
            f"*Borrow Maxi*\n{borrow_price}\n"
            f"Available - {100 - borrow_count}\nFloor price - {borrow_floor} {chain_native}\n"
            f"{borrow_discount_text}\n\n"
            f"*Magister*\n{magister_price}\n"
            f"Available - {49 - magister_count}\nFloor price - {magister_floor} {chain_native}\n"
            f"{magister_discount_text}\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def on_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    tx_deployer = api.get_tx(ca.DEPLOYER, "eth")
    tx_magister_6 = api.get_tx(ca.MAGISTER_6, "eth")

    tx_filter_deployer = [d for d in tx_deployer["result"] if d["to"] in f"{ca.DEAD}".lower()]
    tx_filter_magister_6 = [d for d in tx_magister_6["result"] if d["to"] in f"{ca.DEAD}".lower()]

    recent_tx_deployer = max(tx_filter_deployer, key=lambda tx: int(tx["timeStamp"]), default=None)
    recent_tx_magister_6 = max(tx_filter_magister_6, key=lambda tx: int(tx["timeStamp"]), default=None)

    if recent_tx_deployer and (not recent_tx_magister_6 or int(recent_tx_deployer["timeStamp"]) > int(recent_tx_magister_6["timeStamp"])):
        recent_tx = recent_tx_deployer
        address = ca.DEPLOYER
    elif recent_tx_magister_6:
        recent_tx = recent_tx_magister_6
        address = ca.MAGISTER_6
    message = bytes.fromhex(recent_tx["input"][2:]).decode("utf-8")
    time = datetime.utcfromtimestamp(int(recent_tx["timeStamp"]))
    duration = datetime.utcnow() - time
    days, hours, minutes = api.get_duration_days(duration)
    try:
        await update.message.reply_text(
            f"*Last On Chain Message from* `{address}`\n\n{time} UTC\n"
            f"{days} days, {hours} hours, and {minutes} minutes ago\n\n"
            f"`{message}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{url.ETHER_TX}{recent_tx["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains", url=f"{url.WEBSITE}docs/onchains"
                        )
                    ],
                ]
            ),
        )
    except Exception as e:
        error_message = str(e)
        if "Message is too long" in error_message:
            middle_index = len(message) // 2

            part1 = message[:middle_index]
            part2 = message[middle_index:]

            await update.message.reply_text(
                f"*Last On Chain Message from* `{address}`\n\n{time} UTC\n"
                f"{days} days, {hours} hours, and {minutes} minutes ago\n\n"
                f"`{part1}...`",
                parse_mode="Markdown",
            )
            await update.message.reply_text(
                f"`...{part2}`",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View on chain",
                                url=f'{url.ETHER_TX}{recent_tx["hash"]}',
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="View all on chains", url=f"{url.WEBSITE}docs/onchains"
                            )
                        ],
                    ]
                ),
            )


async def pair(update: Update, context: CallbackContext):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    networks = {
        "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}",
        "ARB": f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ARB')}",
        "BSC": "https://bsc-dataseed.binance.org/",
        "POLY": f"https://polygon-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_POLY')}",
        "OPTI": f"https://opt-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_OPTI')}",
        "BASE": "https://mainnet.base.org"
    }
    contract_networks = {
        "ETH": "eth",
        "ARB": "arb",
        "BSC": "bsc",
        "POLY": "poly",
        "OPTI": "opti",
        "BASE": "base",
    }
    contract_instances = {}
    for network, web3_url in networks.items():
        web3 = Web3(Web3.HTTPProvider(web3_url))
        contract = web3.eth.contract(
            address=to_checksum_address(ca.FACTORY),
            abi=api.get_abi(ca.FACTORY, contract_networks[network]),
        )
        amount = contract.functions.allPairsLength().call()
        contract_instances[network] = amount
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Pair Count*\n\n"
            f'`ETH:`       {contract_instances["ETH"]}\n'
            f'`BSC:`       {contract_instances["BSC"]}\n'
            f'`ARB:`       {contract_instances["ARB"]}\n'
            f'`POLY:`     {contract_instances["POLY"]}\n'
            f'`OPTI:`     {contract_instances["OPTI"]}\n'
            f'`BASE:`     {contract_instances["BASE"]}\n'
            f"`TOTAL:`   {sum(contract_instances.values())}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Xchange Pairs Dashboard",
                        url="https://www.x7finance.org/dashboard",
                    )
                ],
            ]
        ),
    )


async def pfp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "upload_photo")
    text = " ".join(context.args)
    if text == "":
        await update.message.reply_text("Please follow the command with desired name")
    else:
        img = Image.open(requests.get(api.get_random_pioneer(), stream=True).raw)
        i1 = ImageDraw.Draw(img)
        letter_spacing = 7
        position = (360, 987.7)
        for char in text:
            i1.text(position, char, font = ImageFont.truetype(r"media/Bartomes.otf", 34), fill = (255, 255, 255))
            letter_width, _ = i1.textsize(char, font = ImageFont.truetype(r"media/Bartomes.otf", 34))
            position = (position[0] + letter_width + letter_spacing, position[1])
        img.save(r"media/pfp.png")
        await update.message.reply_photo(
            photo=open(r"media/pfp.png", "rb"))


async def pioneer(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        pioneer_id = " ".join(context.args)
        data = api.get_os_nft_collection("/x7-pioneer")
        floor = api.get_nft_floor(ca.PIONEER, "eth")
        native_price = api.get_native_price("eth")
        if floor != "N/A":
            floor_round = round(floor, 2)
            floor_dollar = floor * float(native_price) / 1**18
        else:
            floor_round = "N/A"
            floor_dollar = 0 
        pioneer_pool = api.get_native_balance(ca.PIONEER, "eth")
        each = float(pioneer_pool) / 639
        each_dollar = float(each) * float(native_price) / 1**18
        total_dollar = float(pioneer_pool) * float(native_price) / 1**18
        if pioneer_id == "":
            img = Image.open(random.choice(media.BLACKHOLE))
            i1 = ImageDraw.Draw(img)
            i1.text(
                (28, 36),
                    f"X7 Pioneer NFT Info\n\n"
                    f"Floor Price: {floor_round} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
                    f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n"
                    f"Per Pioneer: {each:.3f} ETH (${each_dollar:,.2f})\n\n"
                    f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
                font = ImageFont.truetype(media.FONT, 28),
                fill = (255, 255, 255),
            )
            img.save(r"media/blackhole.png")
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=
                    f"*X7 Pioneer NFT Info*\n\n"
                    f"Floor Price: {floor_round} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
                    f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n"
                    f"Per Pioneer: {each:.3f} ETH (${each_dollar:,.2f})\n\n"
                    f"{api.get_quote()}",
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="X7 Pioneer Dashboard",
                                url="https://x7.finance/x/nft/pioneer",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Opensea",
                                url=f"{url.OS_PIONEER}",
                            )
                        ],
                    ]
                ),
            )
        else:
            data = api.get_os_nft_id(ca.PIONEER, pioneer_id)
            status = data["nft"]["traits"][0]["value"]
            image_url = data["nft"]["image_url"]
            await update.message.reply_photo(
            photo=image_url,
            caption=
                f"*X7 Pioneer {pioneer_id} NFT Info*\n\n"
                f"Transfer Lock Status: {status}\n\n"
                f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Pioneer Dashboard",
                            url="https://x7.finance/x/nft/pioneer",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Opensea",
                            url=f"https://pro.opensea.io/nft/ethereum/{ca.PIONEER}/{pioneer_id}",
                        )
                    ],
                ]
            ),
        )
    except Exception:
        await update.message.reply_text(f"Pioneer {pioneer_id} not found")


async def pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        eth_price = api.get_native_price("eth")
        eth_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "eth")
        eth_lpool_reserve_dollar = (float(eth_lpool_reserve) * float(eth_price) / 1**18)
        eth_lpool = api.get_native_balance(ca.LPOOL, "eth")
        eth_lpool_dollar = (float(eth_lpool) * float(eth_price) / 1**18)
        eth_pool = round(float(eth_lpool_reserve) + float(eth_lpool), 2)
        eth_dollar = eth_lpool_reserve_dollar + eth_lpool_dollar

        bnb_price = api.get_native_price("bnb")
        bsc_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "bsc")
        bsc_lpool_reserve_dollar = (float(bsc_lpool_reserve) * float(bnb_price) / 1**18)
        bsc_lpool = api.get_native_balance(ca.LPOOL, "bsc")
        bsc_lpool_dollar = (float(bsc_lpool) * float(bnb_price) / 1**18)
        bsc_pool = round(float(bsc_lpool_reserve) + float(bsc_lpool), 2)
        bsc_dollar = bsc_lpool_reserve_dollar + bsc_lpool_dollar

        poly_price = api.get_native_price("matic")
        poly_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "poly")
        poly_lpool_reserve_dollar = (float(poly_lpool_reserve) * float(poly_price) / 1**18)
        poly_lpool = api.get_native_balance(ca.LPOOL, "poly")
        poly_lpool_dollar = (float(poly_lpool) * float(poly_price) / 1**18)
        poly_pool = round(float(poly_lpool_reserve) + float(poly_lpool), 2)
        poly_dollar = poly_lpool_reserve_dollar + poly_lpool_dollar

        arb_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "arb")
        arb_lpool_reserve_dollar = (float(arb_lpool_reserve) * float(eth_price) / 1**18)
        arb_lpool = api.get_native_balance(ca.LPOOL, "arb")
        arb_lpool_dollar = (float(arb_lpool) * float(eth_price) / 1**18)
        arb_pool = round(float(arb_lpool_reserve) + float(arb_lpool), 2)
        arb_dollar = arb_lpool_reserve_dollar + arb_lpool_dollar

        opti_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "opti")
        opti_lpool_reserve_dollar = (float(opti_lpool_reserve) * float(eth_price) / 1**18)
        opti_lpool = api.get_native_balance(ca.LPOOL, "opti")
        opti_lpool_dollar = (float(opti_lpool) * float(eth_price) / 1**18)
        opti_pool = round(float(opti_lpool_reserve) + float(opti_lpool), 2)
        opti_dollar = opti_lpool_reserve_dollar + opti_lpool_dollar

        base_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "base")
        base_lpool_reserve_dollar = (float(base_lpool_reserve) * float(eth_price) / 1**18)
        base_lpool = api.get_native_balance(ca.LPOOL, "base")
        base_lpool_dollar = (float(base_lpool) * float(eth_price) / 1**18)
        base_pool = round(float(base_lpool_reserve) + float(base_lpool), 2)
        base_dollar = base_lpool_reserve_dollar + base_lpool_dollar

        total_lpool_reserve_dollar = (
            eth_lpool_reserve_dollar
            + arb_lpool_reserve_dollar
            + poly_lpool_reserve_dollar
            + bsc_lpool_reserve_dollar
            + opti_lpool_reserve_dollar
            + base_lpool_reserve_dollar
        )
        total_lpool_dollar = (
            eth_lpool_dollar
            + arb_lpool_dollar
            + poly_lpool_dollar
            + bsc_lpool_dollar
            + opti_lpool_dollar
            + base_lpool_dollar
        )

        total_dollar = poly_dollar + bsc_dollar + opti_dollar + arb_dollar + eth_dollar + base_dollar
        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im2 = Image.open(media.X7D_LOGO)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 28),
                f"X7 Finance Lending Pool Info\n\n"
                f'ETH:   {eth_pool} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
                f'ARB:   {arb_pool} ETH (${"{:0,.0f}".format(arb_dollar)})\n'
                f'OPTI:  {opti_pool} ETH (${"{:0,.0f}".format(opti_dollar)})\n'
                f'BSC:   {bsc_pool} BNB (${"{:0,.0f}".format(bsc_dollar)})\n'
                f'POLY:  {poly_pool} MATIC (${"{:0,.0f}".format(poly_dollar)})\n'
                f'BASE:  {base_pool} ETH (${"{:0,.0f}".format(base_dollar)})\n\n'
                f'System Owned: ${"{:0,.0f}".format(total_lpool_dollar)}\n'
                f'External Deposits: ${"{:0,.0f}".format(total_lpool_reserve_dollar)}\n'
                f'Total: ${"{:0,.0f}".format(total_dollar)}\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 28),
            fill = (255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Lending Pool Info *\nUse `/pool [chain-name]` for individual chains\n\n"
                f'`ETH:`   {eth_pool} ETH (${"{:0,.0f}".format(eth_dollar)})\n'
                f'`ARB:`   {arb_pool} ETH (${"{:0,.0f}".format(arb_dollar)})\n'
                f'`OPTI:` {opti_pool} ETH (${"{:0,.0f}".format(opti_dollar)})\n'
                f'`BSC:`   {bsc_pool} BNB (${"{:0,.0f}".format(bsc_dollar)})\n'
                f'`POLY:`  {poly_pool} MATIC (${"{:0,.0f}".format(poly_dollar)})\n'
                f'`BASE:`  {base_pool} ETH (${"{:0,.0f}".format(base_dollar)})\n\n'
                f'System Owned: ${"{:0,.0f}".format(total_lpool_dollar)}\n'
                f'External Deposits: ${"{:0,.0f}".format(total_lpool_reserve_dollar)}\n'
                f'Total: ${"{:0,.0f}".format(total_dollar)}\n\n'
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    else:
        if chain in mappings.CHAINS:
            chain_name = mappings.CHAINS[chain].name
            chain_url = mappings.CHAINS[chain].scan_address
            chain_native = mappings.CHAINS[chain].token
            chain_logo = mappings.CHAINS[chain].logo
            web3_url = mappings.CHAINS[chain].w3
        else:
            await update.message.reply_text(text.CHAIN_ERROR)
            return

        address = to_checksum_address(ca.LPOOL)
        contract = web3_url.eth.contract(address=address, abi=api.get_abi(ca.LPOOL, chain))
        available = (contract.functions.availableCapital().call() / 10**18)
        native_price = api.get_native_price(chain_native)
        lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, chain)
        lpool_reserve_dollar = (float(lpool_reserve) * float(native_price) / 1**18)
        lpool = float(api.get_native_balance(ca.LPOOL, chain))
        lpool_dollar = (float(lpool) * float(native_price) / 1**18)
        pool = round(float(lpool_reserve) + float(lpool), 2)
        dollar = lpool_reserve_dollar + lpool_dollar
        lpool_reserve = round(float(lpool_reserve), 2)
        lpool = round(float(lpool), 2)

        used = lpool - available
        percent = int((used / pool) * 100)
            

        im2 = Image.open(chain_logo)
        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
                f"X7 Finance Lending Pool Info {chain_name}\n\n"
                f"System Owned\n"
                f'{lpool} {chain_native.upper()} (${"{:0,.0f}".format(lpool_dollar)})\n\n'
                f"External Deposits\n"
                f'{lpool_reserve} {chain_native.upper()} (${"{:0,.0f}".format(lpool_reserve_dollar)})\n\n'
                f"Total\n"
                f'{pool} {chain_native.upper()} (${"{:0,.0f}".format(dollar)})\n\n'
                f'Currently Borrowed\n'
                f'{used:.2f} {chain_native.upper()} ({percent}%)\n\n'
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 24),
            fill = (255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await update.message.reply_photo(
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Lending Pool Info {chain_name}*\nUse `/pool [chain-name]` for other chains\n\n"
                f"System Owned\n"
                f'{lpool} {chain_native.upper()} (${"{:0,.0f}".format(lpool_dollar)})\n\n'
                f"External Deposits\n"
                f'{lpool_reserve} {chain_native.upper()} (${"{:0,.0f}".format(lpool_reserve_dollar)})\n\n'
                f"Total\n"
                f'{pool} {chain_native.upper()} (${"{:0,.0f}".format(dollar)})\n\n'
                f'Currently Borrowed\n'
                f'{used:.2f} {chain_native.upper()} ({percent}%)\n\n'
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Lending Pool Contract",
                            url=f"{chain_url}{ca.LPOOL}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Lending Pool Reserve Contract",
                            url=f"{chain_url}{ca.LPOOL_RESERVE}",
                        )
                    ],
                ]
            ),
        )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        if context.args:
            search = context.args[0].lower()
            chain = context.args[1].lower() if len(context.args) > 1 else "eth"
        else:
            search = ""
            chain = ""
        token_info = db.token_get(search, chain)
        for token_instance in token_info:
                holders = api.get_holders(token_instance['ca'], token_instance['chain'])
                dext = mappings.CHAINS[token_instance['chain']].dext
                w3 = mappings.CHAINS[token_instance['chain']].w3
                token = mappings.CHAINS[token_instance['chain']].token
                contract = w3.eth.contract(
                    address=Web3.to_checksum_address(token_instance['pair']), abi=ca.PAIRS_ABI)
                token0_address = contract.functions.token0().call()
                token1_address = contract.functions.token1().call()
                is_reserve_token0 = token_instance['ca'].lower() == token0_address.lower()
                is_reserve_token1 = token_instance['ca'].lower() == token1_address.lower()
                supply = int(api.get_supply(token_instance['ca'], token_instance['chain']))
                eth = ""
                if is_reserve_token0:
                    eth = contract.functions.getReserves().call()[1]
                elif is_reserve_token1:
                    eth = contract.functions.getReserves().call()[0]
                decimals = contract.functions.decimals().call()
                eth_in_wei = int(eth)
                liq = api.get_native_price(token) * eth_in_wei * 2
                formatted_liq = "${:,.2f}".format(liq / (10**decimals))
                token_price = api.get_price(token_instance['ca'], token_instance['chain'])
                mcap = token_price * supply
                if "e-" in str(token_price):
                    price = "{:.8f}".format(token_price)
                elif token_price < 1:
                    price = "{:.8f}".format(token_price) 
                else:
                    price = "{:.2f}".format(token_price)
                formatted_mcap = "${:,.0f}".format(mcap / (10**decimals))
                volume = api.get_volume(token_instance['pair'], token_instance['chain'])
                price_change = api.get_price_change(token_instance['ca'], token_instance['chain'])
                im1 = Image.open((random.choice(media.BLACKHOLE)))
                try:
                    image = token_instance['image_url']
                    img = Image.open(requests.get(image, stream=True).raw)
                    img = img.resize((200, 200), Image.ANTIALIAS)
                    result = img.convert("RGBA")
                    result.save(r"media/tokenlogo.png")
                    im2 = Image.open(r"media/tokenlogo.png")
                except Exception:
                    if token_instance['chain'] == "eth":
                        im2 = Image.open(media.ETH_LOGO)
                    if token_instance['chain'] == "bsc":
                        im2 = Image.open(media.BSC_LOGO)
                    if token_instance['chain'] == "poly":
                        im2 = Image.open(media.POLY_LOGO)
                    if token_instance['chain'] == "arb":
                        im2 = Image.open(media.ARB_LOGO)
                    if token_instance['chain'] == "opti":
                        im2 = Image.open(media.OPTI_LOGO)

                im1.paste(im2, (720, 20), im2)
                i1 = ImageDraw.Draw(im1)
                i1.text(
                    (26, 30),
                        f"Xchange Pair Info\n\n💰 {search.upper()}\n\n"
                        f"💰 Price: {price}\n"
                        f"💎 Market Cap: {formatted_mcap}\n"
                        f"📊 24 Hour Volume: {volume}\n"
                        f"💦 Liquidity: {formatted_liq}\n"
                        f"👪 Holders: {holders}\n\n"
                        f"{price_change}\n\n"
                        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                    font = ImageFont.truetype(media.FONT, 26),
                    fill=(255, 255, 255),
                )
                img_path = os.path.join("media", "blackhole.png")
                im1.save(img_path)
                await update.message.reply_photo(
                    photo=open(r"media/blackhole.png", "rb"),
                    caption=
                        f"*Xchange Pair Info\n\n{search.upper()}*\n\n"
                        f"`{token_instance['ca']}`\n\n"
                        f"💰 Price: {price}\n"
                        f"💎 Market Cap: {formatted_mcap}\n"
                        f"📊 24 Hour Volume: {volume}\n"
                        f"💦 Liquidity: {formatted_liq}\n"
                        f"👪 Holders: {holders}\n\n"
                        f"{price_change}\n\n"
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Chart", url=f"{dext}{token_instance['pair']}"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="Buy",
                                    url=f"{url.XCHANGE}/#/swap?outputCurrency={token_instance['ca']}",
                                )
                            ],
                        ]
                    ),
                )
                return
        if not token_info:
            if search == "":
                price = api.get_cg_price("x7r, x7dao")
                x7r_change = price["x7r"]["usd_24h_change"]
                if x7r_change is None:
                    x7r_change = 0
                else:
                    x7r_change = round(price["x7r"]["usd_24h_change"], 2)
                x7dao_change = price["x7dao"]["usd_24h_change"]
                if x7dao_change is None:
                    x7dao_change = 0
                else:
                    x7dao_change = round(price["x7dao"]["usd_24h_change"], 2)

                im1 = Image.open((random.choice(media.BLACKHOLE)))
                im2 = Image.open(r"media/logo.png")
                im1.paste(im2, (740, 20), im2)
                i1 = ImageDraw.Draw(im1)
                i1.text(
                    (28, 36),
                        f"X7 Finance Token Price Info (ETH)\n\n"
                        f'X7R:    ${price["x7r"]["usd"]}\n'
                        f'24 Hour Change: {x7r_change}%\n\n'
                        f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                        f'24 Hour Change: {x7dao_change}%\n\n\n\n\n\n'
                        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                        font = ImageFont.truetype(media.FONT, 28),
                    fill = (255, 255, 255),
                )
                img_path = os.path.join("media", "blackhole.png")
                im1.save(img_path)
                await update.message.reply_photo(
                    photo=open(r"media/blackhole.png", "rb"),
                    caption=
                        f"*X7 Finance Token Price Info (ETH)*\n"
                        f"Use `/x7r [chain]` or `/x7dao [chain]` for all other details\n"
                        f"Use `/constellations` for constellations\n\n"
                        f'X7R:    ${price["x7r"]["usd"]}\n'
                        f"24 Hour Change: {x7r_change}%\n\n"
                        f'X7DAO:  ${price["x7dao"]["usd"]}\n'
                        f"24 Hour Change: {x7dao_change}%\n\n"
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="X7R Chart - Rewards Token",
                                    url=f"{url.DEX_TOOLS_ETH}{ca.X7R_PAIR_ETH}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="X7DAO Chart - Governance Token",
                                    url=f"{url.DEX_TOOLS_ETH}{ca.X7DAO_PAIR_ETH}",
                                )
                            ],
                        ]
                    ),
                )
                return
                
            if search.startswith("0x") and len(search) == 42:
                if chain == "":
                    chain = "eth"
                
                if chain in mappings.CHAINS:
                    chain_logo = mappings.CHAINS[chain].logo
                    dex_tools = mappings.CHAINS[chain].dext
                else:
                    await update.message.reply_text(text.CHAIN_ERROR)
                    return  
                try:
                    scan = api.get_scan(search, chain)
                except Exception:
                    await update.message.reply_text(
                        f"{search} {chain.upper()} Not found",
                        parse_mode="Markdown",
                    )
                    return
                
                holders = api.get_holders(search, chain)
                if "dex" in scan[str(search)] and scan[str(search)]["dex"]:
                    pair = scan[str(search)]["dex"][0]["pair"]
                else:
                    scan_holders = scan[str(search)].get("holders", [])
                    for holder in scan_holders:
                        if holder.get("is_contract", 0) == 1:
                            pair = holder.get("address")
                            break
                dex = api.get_liquidity_dex(pair, chain)
                token_price = api.get_price(search, chain)
                volume = api.get_volume(pair, chain)
                if "e-" in str(token_price):
                    price = "{:.8f}".format(token_price)
                elif token_price < 1:
                    price = "{:.8f}".format(token_price) 
                else:
                    price = "{:.2f}".format(token_price)
                info = api.get_token_data(search, chain)
                if (
                    info[0]["decimals"] == ""
                    or info[0]["decimals"] == "0"
                    or not info[0]["decimals"]
                ):
                    supply = int(api.get_supply(search, chain))
                else:
                    supply = int(api.get_supply(search, chain)) / 10 ** int(
                        info[0]["decimals"]
                    )

                mcap = float(price) * float(supply)
                formatted_mcap = "${:,.0f}".format(mcap)
                price_change = api.get_price_change(search, chain)
                liquidity_data = api.get_liquidity_from_dextools(pair, chain)
                try:
                    liq = f"${'{:0,.0f}'.format(liquidity_data['liquidity'])}"
                except Exception:
                    liq = "N/A"
                im1 = Image.open((random.choice(media.BLACKHOLE)))
                logo = api.get_token_image(search, chain)
                if logo:
                    img = Image.open(requests.get(logo, stream=True).raw)
                    result = img.convert("RGBA")
                    result.save(r"media/tokenlogo.png")
                    im2 = Image.open(r"media/tokenlogo.png")
                else:
                    im2 = Image.open(chain_logo)
                im1 = Image.open((random.choice(media.BLACKHOLE)))
                im1.paste(im2, (700, 20), im2)
                i1 = ImageDraw.Draw(im1)
                i1.text(
                    (26, 30),
                        f"💰 {scan[str(search).lower()]['token_name']} ({chain.upper()})\n\n"
                        f'💰 Price: {price}\n'
                        f"💎 Market Cap: {formatted_mcap}\n"
                        f"📊 24 Hour Volume: {volume}\n"
                        f"💦 Liquidity: {liq} ({dex} pair)\n"
                        f"👪 Holders: {holders}\n\n"
                        f"{price_change}\n\n\n"
                        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                    font = ImageFont.truetype(media.FONT, 26),
                    fill = (255, 255, 255),
                )
                img_path = os.path.join("media", "blackhole.png")
                im1.save(img_path)
                await update.message.reply_photo(
                    photo=open(r"media/blackhole.png", "rb"),
                    caption=
                        f"*{scan[str(search).lower()]['token_name']} ({chain.upper()})*\n\n"
                        f'💰 Price: {price}\n'
                        f"💎 Market Cap: {formatted_mcap}\n"
                        f"📊 24 Hour Volume: {volume}\n"
                        f"💦 Liquidity: {liq} ({dex} pair)\n"
                        f"👪 Holders: {holders}\n\n"
                        f"{price_change}\n\n"
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Chart", url=f"{dex_tools}{pair}"
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="Buy",
                                    url=f"{url.XCHANGE}/#/swap?outputCurrency={search}",
                                )
                            ],
                        ]
                    ),
                )
                return
            else:
                token = api.get_cg_search(search)
                token_id = token["coins"][0]["api_symbol"]
                symbol = token["coins"][0]["symbol"]
                thumb = token["coins"][0]["large"]
                token_price = api.get_cg_price(token_id)
                try:
                    if "e-" in str(token_price[token_id]["usd"]):
                        price = "{:.8f}".format(token_price[token_id]["usd"])
                    elif token_price[token_id]["usd"] < 1:
                        price = "{:.8f}".format(token_price[token_id]["usd"]) 
                    else:
                        price = "{:.2f}".format(token_price[token_id]["usd"])
                except Exception:
                    await update.message.reply_text(
                        f"{search.upper()} Not found",
                        parse_mode="Markdown")
                    return
                price_change = token_price[token_id]["usd_24h_change"]
                if price_change is None:
                    price_change = 0
                else:
                    price_change = round(token_price[token_id]["usd_24h_change"], 2)
                market_cap = token_price[token_id]["usd_market_cap"]
                if market_cap is None or market_cap == 0:
                    market_cap_formatted = " N/A"
                else:
                    market_cap_formatted = "${:0,.0f}".format(float(market_cap))
                img = Image.open(requests.get(thumb, stream=True).raw)
                result = img.convert("RGBA")
                result.save(r"media/tokenlogo.png")
                im1 = Image.open((random.choice(media.BLACKHOLE)))
                im2 = Image.open(r"media/tokenlogo.png")
                im1.paste(im2, (680, 20), im2)
                i1 = ImageDraw.Draw(im1)
                i1.text(
                    (28, 36),
                        f"{symbol} price - CoinGecko\n\n"
                        f'Price: ${price}\n'
                        f"24 Hour Change: {price_change}%\n"
                        f'Market Cap: {market_cap_formatted}\n\n\n\n\n\n\n\n'
                        f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                    font = ImageFont.truetype(media.FONT, 28),
                    fill=(255, 255, 255),
                )
                im1.save(r"media/blackhole.png", quality=95)
                await update.message.reply_photo(
                    photo=open(r"media/blackhole.png", "rb"),
                    caption=
                        f"*{symbol} price* - CoinGecko\n\n"
                        f'Price: ${price}\n'
                        f'24 Hour Change: {price_change}%\n'
                        f'Market Cap: {market_cap_formatted}\n\n'
                        f"{api.get_quote()}",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Chart",
                                    url=f"https://www.coingecko.com/en/coins/{token_id}",
                                )
                            ],
                        ]
                    ),
                )
    except IndexError:
        await update.message.reply_text(
            f"{search.upper()} Not found",
            parse_mode="Markdown",
        )


async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="ETH", url=f"{url.ETHER_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="BSC", url=f"{url.BSC_ADDRESS}{ca.ROUTER}"),
        ],
        [
            InlineKeyboardButton(text="Polygon", url=f"{url.POLY_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="Arbitrum", url=f"{url.ARB_ADDRESS}{ca.ROUTER}"),
        ],
        [
            InlineKeyboardButton(text="Optimism", url=f"{url.OPTI_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="Base", url=f"{url.BASE_ADDRESS}{ca.ROUTER}"),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "upload_audio")
    if not context.args:
        await update.message.reply_text("Please provide some words to convert to speech.")
        return
    voice_note = gTTS(" ".join(context.args), lang='en', slow=False)
    voice_note.save("media/voicenote.mp3")
    await update.message.reply_audio(audio=open("media/voicenote.mp3", "rb"))


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            f"Please provide contract address and chain")
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    if len(context.args) == 1:
        token_address = context.args[0].lower()
        chain = "eth"

    if len(context.args) == 2:
        token_address = context.args[0].lower()
        chain = context.args[1].lower()

    if chain in mappings.CHAINS:
        web3_url = mappings.CHAINS[chain].w3
        scan_link = mappings.CHAINS[chain].scan_address
        dex_tools_link = mappings.CHAINS[chain].dext

    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    if token_address == "":
        await update.message.reply_text(
        f"Please provide Contract Address and chain",
    )
        return
    scan = api.get_scan(token_address, chain)
    if scan == {}:
        await update.message.reply_text(f"{token_address} ({chain.upper}) not found")
        return
    if api.get_verified(search, chain):
        verified = "✅ Contract Verified"
    else:
        "⚠️ Contract Unverified"
    if scan[f"{str(token_address).lower()}"]["is_in_dex"] == "1":
        try:
            if (
                scan[f"{str(token_address).lower()}"]["sell_tax"] == "1"
                or scan[f"{str(token_address).lower()}"]["buy_tax"] == "1"
            ):
                return
            buy_tax_raw = (
                float(scan[f"{str(token_address).lower()}"]["buy_tax"]) * 100
            )
            sell_tax_raw = (
                float(scan[f"{str(token_address).lower()}"]["sell_tax"]) * 100
            )
            buy_tax = int(buy_tax_raw)
            sell_tax = int(sell_tax_raw)
            if sell_tax > 10 or buy_tax > 10:
                tax = f"⚠️ Tax: {buy_tax}/{sell_tax}"
            else:
                tax = f"✅️ Tax: {buy_tax}/{sell_tax}"
        except Exception:
            tax = f"❓ Tax - Unknown"
    else:
        tax = f"❓ Tax - Unknown"
    token_address_str = str(token_address)
    if token_address_str in scan:
        if "owner_address" in scan[token_address_str]:
            if scan[token_address_str]["owner_address"] == "0x0000000000000000000000000000000000000000":
                renounced = "✅ Contract Renounced"
            else:
                renounced = "⚠️ Contract Not Renounced"
        if "is_mintable" in scan[token_address_str]:
            if scan[token_address_str]["is_mintable"] == "1":
                mint = "⚠️ Mintable"
            else:
                mint = "✅️ Not Mintable"
        else:
            mint = "❓ Mintable - Unknown"

        if "is_honeypot" in scan[token_address_str]:
            if scan[token_address_str]["is_honeypot"] == "1":
                honey_pot = "❌ Honey Pot"
            else:
                honey_pot = "✅️ Not Honey Pot"
        else:
            honey_pot = "❓ Honey Pot - Unknown"

        if "is_blacklisted" in scan[token_address_str]:
            if scan[token_address_str]["is_blacklisted"] == "1":
                blacklist = "⚠️ Has Blacklist Functions"
            else:
                blacklist = "✅️ No Blacklist Functions"
        else:
            blacklist = "❓ Blacklist Functions - Unknown"

        if "cannot_sell_all" in scan[token_address_str]:
            if scan[token_address_str]["cannot_sell_all"] == "1":
                sellable = "❌ Not Sellable"
            else:
                sellable = "✅️ Sellable"
        else:
            sellable = "❓ Sellable - Unknown"

        if "is_whitelisted" in scan[token_address_str]:
            if scan[token_address_str]["is_whitelisted"] == "1":
                whitelist = "⚠️ Has Whitelist Functions"
            else:
                whitelist = "✅️ No Whitelist Functions"
        else:
            whitelist = "❓ Whitelist Functions - Unknown"
            
        if "creator_percent" in scan[token_address_str]:
            creator_percent_str = float(scan[token_address_str]["creator_percent"])
            formatted_creator_percent = "{:.1f}".format(creator_percent_str * 100)

            if creator_percent_str >= 0.05:
                creator_percent = f'⚠️ Deployer Holds {formatted_creator_percent}% of Supply'
            else:
                creator_percent = f'✅ Deployer Holds {formatted_creator_percent}% of Supply'
        else:
            creator_percent = "❓ Tokens Held By Creator Unknown"
        if "owner_percent" in scan[token_address_str]:
            if renounced == "✅ Contract Renounced":
                owner_percent = f'✅️ Owner Holds 0.0% of Supply'
            else:
                owner_percent_str = float(scan[token_address_str]["owner_percent"])
                formatted_owner_percent = "{:.1f}".format(owner_percent_str * 100)
                if owner_percent_str >= 0.05:
                    owner_percent = f'⚠️ Owner Holds {formatted_owner_percent}% of Supply'
                else:
                    owner_percent = f'✅️ Owner Holds {formatted_owner_percent}% of Supply'
        else:
            owner_percent = "❓ Tokens Held By Owner Unknown"
        if "lp_holders" in scan[token_address_str]:
            locked_lp_list = [
                lp
                for lp in scan[token_address_str]["lp_holders"]
                if lp["is_locked"] == 1 and lp['balance'] > "0.1"
            ]
            if locked_lp_list:
                if locked_lp_list[0]["address"] == "0x000000000000000000000000000000000000dead":
                    lock_word = "🔥 Liquidity Burnt"
                else:
                    lock_word = "✅️ Liquidity Locked"
                lp_with_locked_detail = [
                    lp for lp in locked_lp_list if "locked_detail" in lp
                ]
                if lp_with_locked_detail:
                    percent = float(locked_lp_list[0]['percent'])
                    lock = (
                        f"{lock_word} - {locked_lp_list[0]['tag']} - {percent * 100:.2f}%\n"
                        f"⏰ Unlock - {locked_lp_list[0]['locked_detail'][0]['end_time'][:10]}"
                    )
                else:
                    percent = float(locked_lp_list[0]['percent'])
                    lock = (
                        f"{lock_word} - {percent * 100:.2f}%"
                    )
            else:
                lock = ""
        else:
            lock = ""
        if "dex" in scan[token_address_str]:
            liquidity = scan[f"{str(token_address).lower()}"]["dex"][0]["liquidity"]
            liq_eth = float(liquidity) * 2
            formatted_liq_eth = "{:,.2f}".format(liq_eth)
            if liq_eth  > 5000:

                liquidity = f'✅ Liquidity - ${formatted_liq_eth}'
            else:
                liquidity = f'⚠️ Liquidity - ${formatted_liq_eth}'
        else:
            liquidity = "❓ Liquidity Unknown"

    else:
        mint = "❓ Mintable - Unknown"
        honey_pot = "❓ Honey Pot - Unknown"
        blacklist = "❓ Blacklist Functions - Unknown"
        sellable = "❓ Sellable - Unknown"
        whitelist = "❓ Whitelist Functions Unknown"
        creator_percent = "❓ Tokens Held By Deployer Unknown"
        owner_percent = "❓ Tokens Held By Owner Unknown"
        lock  = "❓ Liquidity Lock Unknown"
        liquidity = "❓ Liquidity Unknown"

    status = f"{verified}\n{renounced}\n{tax}\n{sellable}\n{mint}\n{honey_pot}\n{whitelist}\n{blacklist}\n{creator_percent}\n{owner_percent}\n{liquidity}\n{lock}"
    token_name = scan[f"{str(token_address).lower()}"]["token_name"]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Token Scanner*\n\n{token_name} ({chain.upper()})\n`{token_address}`\n\n{status}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"{token_name} Contract",
                        url=f"{scan_link}{token_address}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Chart",
                        url=f'{dex_tools_link}{scan[str(token_address).lower()]["dex"][0]["pair"]}',
                    )
                ],
                


            ]
        ),
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    wiki = wikipediaapi.Wikipedia("en")
    keyword = " ".join(context.args)
    page_py = wiki.page(keyword)
    if keyword == "":
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption="Please follow the command with your search",
        )
    if page_py.exists():
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"Your search: {page_py.title}\n\n"
                f"{(page_py.summary[0:800])}"
                f"....[continue reading on wiki]({page_py.fullurl})\n\n"
                f"[Google](https://www.google.com/search?q={keyword})\n"
                f"[X](https://twitter.com/search?q={keyword}&src=typed_query)\n"
                f"[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n"
                f"{api.get_quote()}",
            parse_mode="markdown",
        )
    else:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"Your search: {keyword}\n\nNo description available\n\n"
                f"[Google](https://www.google.com/search?q={keyword})\n"
                f"[X](https://twitter.com/search?q={keyword}&src=typed_query)\n"
                f"[Etherscan](https://etherscan.io/search?f=0&q={keyword})\n\n"
                f"{api.get_quote()}",
            parse_mode="markdown",
        )


async def signers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        com_wallet = mappings.CHAINS[chain].com_multi
        dev_wallet = mappings.CHAINS[chain].dev_multi
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    dev_response = api.get_signers(dev_wallet)
    com_response = api.get_signers(com_wallet)
    dev_list = dev_response["owners"]
    dev_address = "\n\n".join(map(lambda x: f"`{x}`", dev_list))
    com_list = com_response["owners"]
    com_address = "\n\n".join(map(lambda x: f"`{x}`", com_list))
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Multi-Sig Signers {chain_name}*\n"
            f"Use `/signers [chain-name]` or other chains\n\n"
            f"*Developer Signers*\n{dev_address}\n\n*Community Signers*\n{com_address}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Developer Multi-Sig",
                        url=f"{chain_url}{dev_wallet}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7 Community Multi-Sig",
                        url=f"{chain_url}{com_wallet}",
                    )
                ],
            ]
        ),
    )


async def smart(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].scan_address
        buttons = [
        [
            InlineKeyboardButton(
                text="Contracts Directory",
                url=f"{url.CA_DIRECTORY}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7100 Liquidity Hub", url=f"{chain_url}{ca.X7100_LIQ_HUB}"
            ),
            InlineKeyboardButton(
                text="X7R Liquidity Hub", url=f"{chain_url}{ca.X7R_LIQ_HUB}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7DAO Liquidity Hub", url=f"{chain_url}{ca.X7DAO_LIQ_HUB}"
            ),
            InlineKeyboardButton(
                text="X7 Token Burner", url=f"{chain_url}{ca.BURNER}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7100 Discount Authority",
                url=f"{chain_url}{ca.X7100_DISCOUNT}",
            ),
            InlineKeyboardButton(
                text="X7R Discount Authority",
                url=f"{chain_url}{ca.X7R_DISCOUNT}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7DAO Discount Authority",
                url=f"{chain_url}{ca.X7DAO_DISCOUNT}",
            ),
            InlineKeyboardButton(
                text="X7 Token Time Lock", url=f"{chain_url}{ca.TIME_LOCK}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Ecosystem Splitter",
                url=f"{chain_url}{ca.ECO_SPLITTER}",
            ),
            InlineKeyboardButton(
                text="X7 Treasury Splitter",
                url=f"{chain_url}{ca.TREASURY_SPLITTER}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Profit Share Splitter",
                url=f"{chain_url}{ca.PROFIT_SHARING}",
            ),
            InlineKeyboardButton(
                text="X7 Lending Pool Reserve",
                url=f"{chain_url}{ca.LPOOL_RESERVE}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Xchange Discount Authority",
                url=f"{chain_url}{ca.XCHANGE_DISCOUNT}",
            ),
            InlineKeyboardButton(
                text="X7 Lending Discount Authority",
                url=f"{chain_url}{ca.LENDING_DISCOUNT}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Xchange Router", url=f"{chain_url}{ca.ROUTER}"
            ),
            InlineKeyboardButton(
                text="X7 Xchange Router with Discounts",
                url=f"{chain_url}{ca.DISCOUNT_ROUTER}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="X7 Lending Pool Contract", url=f"{chain_url}{ca.LPOOL}"
            ),
            InlineKeyboardButton(
                text="X7 Xchange Factory", url=f"{chain_url}{ca.FACTORY}"
            ),
        ],
    ]
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Smart Contracts {chain_name}*\nUse `/smart [chain-name]` or other chains\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def splitters(update: Update, context):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        if len(context.args) > 1:
            eth_value = float(context.args[1])
            chain = context.args[0].lower()
            if chain in mappings.CHAINS:
                chain_name = mappings.CHAINS[chain].name
                chain_url = mappings.CHAINS[chain].scan_address
                chain_native = mappings.CHAINS[chain].token
            else:
                await update.message.reply_text(text.CHAIN_ERROR)
                return
            distribution = api.get_split(eth_value)
            message = f"*X7 Finance Ecosystem Splitters {chain_name}* \n\n{eth_value} {chain_native.upper()}\n\n"
            for location, share in distribution.items():
                if location == "Treasury":
                    message += f"\n{location}: {share:.2f} {chain_native.upper()}:\n"
                else:
                    message += f"{location}: {share:.2f} {chain_native.upper()}\n"

            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"{message}\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Ecosystem Splitter",
                                url=f"{chain_url}{ca.ECO_SPLITTER}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Treasury Splitter",
                                url=f"{chain_url}{ca.TREASURY_SPLITTER}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Profit Share Splitter",
                                url=f"{chain_url}{ca.PROFIT_SHARING}",
                            )
                        ],
                    ]
                ),
            )
        elif len(context.args) == 1:
            chain = context.args[0].lower()
            if chain in mappings.CHAINS:
                chain_name = mappings.CHAINS[chain].name
                chain_url = mappings.CHAINS[chain].scan_address
                chain_native = mappings.CHAINS[chain].token
            else:
                await update.message.reply_text(text.CHAIN_ERROR)
                return
            
            treasury_eth_raw = api.get_native_balance(ca.TREASURY_SPLITTER, chain)
            eco_eth_raw = api.get_native_balance(ca.ECO_SPLITTER, chain)
            profit_eth_raw = api.get_native_balance(ca.PROFIT_SHARING, chain)
            treasury_eth = round(float(treasury_eth_raw), 2)
            eco_eth = round(float(eco_eth_raw), 2)
            profit_eth = round(float(profit_eth_raw), 2)
            native_price = api.get_native_price(chain_native)
            eco_dollar = float(eco_eth) * float(native_price)
            profit_dollar = float(profit_eth) * float(native_price)
            treasury_dollar = float(treasury_eth) * float(native_price)
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Ecosystem Splitters {chain_name}*\n\n"
                    f"Ecosystem Splitter: {eco_eth} {chain_native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
                    f"Profit Share Splitter: {profit_eth} {chain_native.upper()} (${'{:0,.0f}'.format(profit_dollar)})\n"
                    f"Treasury Splitter: {treasury_eth} {chain_native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                    f"For example of splitter allocation use\n`/splitter [chain-name] [amount]`\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Ecosystem Splitter",
                                url=f"{chain_url}{ca.ECO_SPLITTER}",
                            )
                        ],
                        [
                        InlineKeyboardButton(
                            text="Profit Share Splitter",
                            url=f"{chain_url}{ca.PROFIT_SHARING}",
                        )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Treasury Splitter",
                                url=f"{chain_url}{ca.TREASURY_SPLITTER}",
                            )
                        ],
                    ]
                ),
            )
        else:
            chain = "eth"
            if chain in mappings.CHAINS:
                chain_name = mappings.CHAINS[chain].name
                chain_url = mappings.CHAINS[chain].scan_address
                chain_native = mappings.CHAINS[chain].token
            else:
                await update.message.reply_text(text.CHAIN_ERROR)
                return
            
            treasury_eth_raw = api.get_native_balance(ca.TREASURY_SPLITTER, chain)
            eco_eth_raw = api.get_native_balance(ca.ECO_SPLITTER, chain)
            profit_eth_raw = api.get_native_balance(ca.PROFIT_SHARING, chain)
            treasury_eth = round(float(treasury_eth_raw), 2)
            eco_eth = round(float(eco_eth_raw), 2)
            profit_eth = round(float(profit_eth_raw), 2)
            native_price = api.get_native_price(chain_native)
            eco_dollar = float(eco_eth) * float(native_price)
            profit_dollar = float(profit_eth) * float(native_price)
            treasury_dollar = float(treasury_eth) * float(native_price)
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Ecosystem Splitters {chain_name}*\n\n"
                    f"Ecosystem Splitter: {eco_eth} {chain_native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
                    f"Profit Share Splitter: {profit_eth} {chain_native.upper()} (${'{:0,.0f}'.format(profit_dollar)})\n"
                    f"Treasury Splitter: {treasury_eth} {chain_native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                    f"For example of splitter allocation use\n`/splitter [chain-name] [amount]`\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Ecosystem Splitter",
                                url=f"{chain_url}{ca.ECO_SPLITTER}",
                            )
                        ],
                        [
                        InlineKeyboardButton(
                            text="Profit Share Splitter",
                            url=f"{chain_url}{ca.PROFIT_SHARING}",
                        )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Treasury Splitter",
                                url=f"{chain_url}{ca.TREASURY_SPLITTER}",
                            )
                        ],
                    ]
                ),
            )
    except Exception:
        await update.message.reply_text(
                            f"For example of splitter allocation use\n`/splitter [chain-name] [amount]`",
                            parse_mode="Markdown",
                        )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    github_url = f'https://api.github.com/repos/x7finance/telegram-bot'
    headers = {'Authorization': f'token {os.getenv("GITHUB_PAT")}'}
    response = requests.get(github_url, headers=headers)
    repo_info = response.json()
    update_time_raw = repo_info["pushed_at"]
    timestamp_datetime = datetime.fromisoformat(update_time_raw).astimezone(timezone.utc)
    current_datetime = datetime.now(timezone.utc)
    time_difference = (current_datetime - timestamp_datetime).total_seconds()
    days, seconds = divmod(int(time_difference), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    contriburots_url = f'https://api.github.com/repos/x7finance/telegram-bot/contributors'
    contributors_response = requests.get(contriburots_url, headers=headers)
    contributors = contributors_response.json()
    contributor_info = ''
    for contributor in contributors:
        contributor_info += f'{contributor["login"]}, Contributions: {contributor["contributions"]}\n'
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f'*X7 Finance Telegram Bot Stats*\n\n'
            f'Language: {repo_info["language"]}\n'
            f'Stars: {repo_info["stargazers_count"]}\n'
            f'Watchers: {repo_info["watchers_count"]}\n'
            f'Forks: {repo_info["forks_count"]}\n'
            f'Open Issues: {repo_info["open_issues_count"]}\n\n'
            f'Contributors:\n{contributor_info}\n'
            f"Last Updated {timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"{days} days, {hours} hours and {minutes} minutes ago\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="GitHub", url=f"https://github.com/x7finance/telegram-bot")],
            ]
        ),
    )


async def supply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    token_pairs = {
        "x7r": (ca.X7R_PAIR_ETH, ca.X7R),
        "x7dao": (ca.X7DAO_PAIR_ETH, ca.X7DAO),
        "x7101": (ca.X7101_PAIR_ETH, ca.X7101),
        "x7102": (ca.X7102_PAIR_ETH, ca.X7102),
        "x7103": (ca.X7103_PAIR_ETH, ca.X7103),
        "x7104": (ca.X7104_PAIR_ETH, ca.X7104),
        "x7105": (ca.X7105_PAIR_ETH, ca.X7105),
    }
    prices = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    supply_info = {}
    for token, (pair, contract) in token_pairs.items():
        balance = api.get_token_balance(pair, contract, "eth")
        dollar_value = balance * prices[token]["usd"]
        percent = round(balance / ca.SUPPLY * 100, 2)
        supply_info[token] = {
            "balance": balance,
            "dollar_value": dollar_value,
            "percent": percent,
        }
    caption_lines = []
    for token, info in supply_info.items():
        balance_str = "{:0,.0f}".format(info["balance"])
        dollar_value_str = "${:0,.0f}".format(info["dollar_value"])
        percent_str = f"{info['percent']}%"
        line = f"{token.upper()}\n{balance_str} {token.upper()} ({dollar_value_str}) {percent_str}"
        caption_lines.append(line)
    caption_text = "\n\n".join(caption_lines)
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Uniswap Supply*\n\n{caption_text}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
    )


async def swap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(
        sticker=media.SWAP,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange", url=f"{url.XCHANGE}")],
            ]
        ),
    )


async def tax_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    tax_info = tax.GENERATE_INFO(chain)
    if not chain:
        chain = "eth"
        tax_info = tax.GENERATE_INFO(chain)
    if tax_info:
        caption = f"{tax_info}"
    caption = f"{chain.upper()}:\n{caption}\n\n{api.get_quote()}"
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=caption,
        parse_mode="Markdown",
    )


async def timestamp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = " ".join(context.args)
        if text == "":
            await update.message.reply_text(
                "Please follow the command with the timestamp you wish to convert"
            )
        else:  
            stamp = int(" ".join(context.args).lower())
            time = api.timestamp_to_datetime(stamp)
            current_time = datetime.utcnow()
            timestamp_time = datetime.utcfromtimestamp(stamp)
            time_difference = current_time - timestamp_time
            if time_difference.total_seconds() > 0:
                time_message = "ago"
            else:
                time_message = "away"
                time_difference = abs(time_difference)
            years = time_difference.days // 365
            months = (time_difference.days % 365) // 30
            days = time_difference.days % 30
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Timestamp Conversion*\n\n"
                    f"{stamp}\n{time} UTC\n\n"
                    f"{years} years, {months} months, {days} days, "
                    f"{hours} hours, {minutes} minutes {time_message}\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )
    except Exception:
        await update.message.reply_text(
            "Timestamp not recognised"
        )


async def time(update: Update, context: CallbackContext):
    message = update.message.text.split(" ")
    timezones = [
        ("America/Los_Angeles", "PST"),
        ("America/New_York", "EST"),
        ("UTC", "UTC"),
        ("Europe/Dublin", "IST"),
        ("Europe/London", "GMT"),
        ("Europe/Berlin", "CET"),
        ("Asia/Dubai", "GST"),
        ("Asia/Tokyo", "JST"),
        ("Australia/Sydney", "AEST"),
    ]
    current_time = datetime.now(pytz.timezone("UTC"))
    local_time = current_time.astimezone(pytz.timezone("UTC"))
    try:
        if len(message) > 1:
            time_variable = message[1]
            time_format = "%I%p"
            if re.match(r"\d{1,2}:\d{2}([ap]m)?", time_variable):
                time_format = (
                    "%I:%M%p"
                    if re.match(r"\d{1,2}:\d{2}am", time_variable, re.IGNORECASE)
                    else "%I:%M%p"
                )
            input_time = datetime.strptime(time_variable, time_format).replace(
                year=local_time.year, month=local_time.month, day=local_time.day
            )
            if len(message) > 2:
                time_zone = message[2]
                for tz, tz_name in timezones:
                    if time_zone.lower() == tz_name.lower():
                        tz_time = pytz.timezone(tz).localize(input_time)
                        time_info = f"{input_time.strftime('%A %B %d %Y')}\n"
                        time_info += f"{input_time.strftime('%I:%M %p')} - {time_zone.upper()}\n\n"
                        for tz_inner, tz_name_inner in timezones:
                            converted_time = tz_time.astimezone(pytz.timezone(tz_inner))
                            time_info += f"{converted_time.strftime('%I:%M %p')} - {tz_name_inner}\n"
                        await update.message.reply_text(
                            time_info, parse_mode="Markdown"
                        )
                        return
            time_info = f"{input_time.strftime('%A %B %d %Y')}\n"
            time_info += (
                f"{input_time.strftime('%I:%M %p')} - {time_variable.upper()}\n\n"
            )
            for tz, tz_name in timezones:
                tz_time = input_time.astimezone(pytz.timezone(tz))
                time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
            await update.message.reply_text(time_info, parse_mode="Markdown")
            return
        time_info = f"{local_time.strftime('%A %B %d %Y')}\n"
        time_info += (
            f"{local_time.strftime('%I:%M %p')} - {local_time.strftime('%Z')}\n\n"
        )
        for tz, tz_name in timezones:
            tz_time = local_time.astimezone(pytz.timezone(tz))
            time_info += f"{tz_time.strftime('%I:%M %p')} - {tz_name}\n"
        await update.message.reply_text(time_info, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(
            "use `/time HH:MMPM or HHAM TZ`", parse_mode="Markdown"
        )


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = api.get_today()
    today = random.choice(data["data"]["Events"])
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f'On this day in {today["year"]}:\n\n{today["text"]}',
        parse_mode="Markdown",
    )


async def translate_german(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang="english", to_lang="german")
    phrase = " ".join(context.args).lower()
    if phrase == "":
        await update.message.reply_text("Please follow the command with the sentence you wish to translate")
    else:
        translation = translator.translate(phrase)
        await update.message.reply_text(translation)


async def translate_japanese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang="english", to_lang="japanese")
    phrase = " ".join(context.args).lower()
    if phrase == "":
        await update.message.reply_text("Please follow the command with the sentence you wish to translate")
    else:
        translation = translator.translate(phrase)
        await update.message.reply_text(translation)


async def translate_russian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translator = Translator(from_lang="english", to_lang="russian")
    phrase = " ".join(context.args).lower()
    if phrase == "":
        await update.message.reply_text("Please follow the command with the sentence you wish to translate")
    else:
        translation = translator.translate(phrase)
        await update.message.reply_text(translation)


async def treasury(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
                chain_name = mappings.CHAINS[chain].name
                chain_url = mappings.CHAINS[chain].scan_address
                chain_native = mappings.CHAINS[chain].token
                chain_com_multi = mappings.CHAINS[chain].com_multi
                chain_logo = mappings.CHAINS[chain].logo
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    native_price = api.get_native_price(chain_native)
    com_eth_raw = api.get_native_balance(chain_com_multi, chain)
    com_eth = round(float(com_eth_raw), 2)
    com_dollar = float(com_eth) * float(native_price)
    treasury_eth = api.get_native_balance(ca.TREASURY_SPLITTER, chain)
    eco_eth = api.get_native_balance(ca.ECO_SPLITTER, chain)
    eco_dollar = float(eco_eth) * float(native_price)
    treasury_dollar = float(treasury_eth) * float(native_price)
    com_usdt_balance = api.get_stables_balance(chain_com_multi, ca.USDT, chain)
    com_usdc_balance = api.get_stables_balance(chain_com_multi, ca.USDC, chain)
    stables = com_usdt_balance + com_usdc_balance
    com_x7r_balance = api.get_token_balance(chain_com_multi, ca.X7R, chain)
    com_x7r_price = com_x7r_balance * api.get_price(ca.X7R, chain)
    com_x7dao_balance = api.get_token_balance(chain_com_multi, ca.X7DAO, chain)
    com_x7dao_price = com_x7dao_balance * api.get_price(ca.X7DAO, chain)
    com_x7d_balance = api.get_token_balance(chain_com_multi, ca.X7D, chain)
    com_x7d_price = com_x7d_balance * native_price
    com_total = com_x7r_price + com_dollar + com_x7d_price + com_x7dao_price + stables
    im2 = Image.open(chain_logo)
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 10),
            f"X7 Finance Treasury {chain_name}\n\n"
            f"Community Wallet:\n{com_eth} {chain_native.upper()} (${'{:0,.0f}'.format(com_dollar)})\n"
            f"{com_x7d_balance} X7D (${'{:0,.0f}'.format(com_x7d_price)})\n"
            f"{com_x7r_balance} X7R (${'{:0,.0f}'.format(com_x7r_price)})\n"
            f"{com_x7dao_balance} X7DAO (${'{:0,.0f}'.format(com_x7dao_price)})\n"
            f"${'{:0,.0f}'.format(stables)} USDT/C\n"
            f"Total: (${'{:0,.0f}'.format(com_total)})\n\n"
            f"Ecosystem Splitter:\n{eco_eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n\n"
            f"Treasury Splitter:\n{treasury_eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
            f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        font = ImageFont.truetype(media.FONT, 24),
        fill = (255, 255, 255),
    )

    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*X7 Finance Treasury {chain_name}*\nUse `/treasury [chain-name]` for other chains\n\n"
            f'Community Wallet:\n{com_eth} {chain_native.upper()} (${"{:0,.0f}".format(com_dollar)})\n'
            f'{com_x7d_balance} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
            f'{"{:0,.0f}".format(com_x7r_balance)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
            f'{"{:0,.0f}".format(com_x7dao_balance)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
            f"${'{:0,.0f}'.format(stables)} USDT/C\n"
            f'Total: (${"{:0,.0f}".format(com_total)})\n\n'
            f"Ecosystem Splitter: {eco_eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
            f"Treasury Splitter: {treasury_eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Community Multi-sig Wallet",
                        url=f"{chain_url}{chain_com_multi}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Ecosystem Splitter Contract",
                        url=f"{chain_url}{ca.ECO_SPLITTER}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Treasury Splitter Contract",
                        url=f"{chain_url}{ca.TREASURY_SPLITTER}",
                    )
                ],
            ]
        ),
    )


async def volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        if dune.FLAG == False:
            execution_id = dune.execute_query("2972368", "medium")
            t.sleep(5)
            response = dune.get_query_results(execution_id)
            response_data = response.json()

            last_24hr_amt = response_data['result']['rows'][0]['last_24hr_amt']
            last_30d_amt = response_data['result']['rows'][0]['last_30d_amt']
            last_7d_amt = response_data['result']['rows'][0]['last_7d_amt']
            lifetime_amt = response_data['result']['rows'][0]['lifetime_amt']

            volume = (
                f'Total:       ${"{:0,.0f}".format(lifetime_amt)}\n'
                f'30 Day:    ${"{:0,.0f}".format(last_30d_amt)}\n'
                f'7 Day:      ${"{:0,.0f}".format(last_7d_amt)}\n'
                f'24 Hour:  ${"{:0,.0f}".format(last_24hr_amt)}'
                )

            await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*Xchange Trading Volume*\n\n{volume}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Dune Dashboard", url=f"{url.DUNE}"
                        )
                    ],
                ]
            ),
            )
            dune.TIMESTAMP = datetime.utcnow().timestamp()
            dune.FLAG = True
            dune.VOLUME = volume
        else:
            await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f'*Xchange Trading Volume*\n\n'
                f'{dune.VOLUME}\n\nLast Updated: {dune.LAST_DATE}\n\n'
                f'{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Dune Dashboard", url=f"{url.DUNE}"
                        )
                    ],
                ]
            ),
            )
    except Exception:
        await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f'*Xchange Volume*\n\n'
            f'Unable to refresh Dune data, please use the link below\n\n'
            f'{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Dune Dashboard", url=f"{url.DUNE}"
                    )
                ],
            ]
        ),
        )


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        chain = context.args[1].lower()
        wallet = context.args[0]
    else:
        await update.message.reply_text(
        f"Please use `/wallet [wallet_address] [chain-name]`",
        parse_mode="Markdown")
        return
    if not wallet.startswith("0x"):
        await update.message.reply_text(
        f"Please use `/wallet [wallet_address] [chain-name]`",
        parse_mode="Markdown")
        return
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
                chain_name = mappings.CHAINS[chain].name
                chain_url = mappings.CHAINS[chain].scan_address
                chain_native = mappings.CHAINS[chain].token
                chain_logo = mappings.CHAINS[chain].logo
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    native_price = api.get_native_price(chain_native)
    eth = api.get_native_balance(wallet, chain)
    dollar = float(eth) * float(native_price)
    x7r_balance = api.get_token_balance(wallet, ca.X7R, chain)
    x7r_price = x7r_balance * api.get_price(ca.X7R, chain)
    x7dao_balance = api.get_token_balance(wallet, ca.X7DAO, chain)
    x7dao_price = x7dao_balance * api.get_price(ca.X7DAO, chain)
    x7101_balance = api.get_token_balance(wallet, ca.X7101, chain)
    x7101_price = x7101_balance * api.get_price(ca.X7101, chain)
    x7102_balance = api.get_token_balance(wallet, ca.X7102, chain)
    x7102_price = x7102_balance * api.get_price(ca.X7102, chain)
    x7103_balance = api.get_token_balance(wallet, ca.X7103, chain)
    x7103_price = x7103_balance * api.get_price(ca.X7103, chain)
    x7104_balance = api.get_token_balance(wallet, ca.X7104, chain)
    x7104_price = x7104_balance * api.get_price(ca.X7104, chain)
    x7105_balance = api.get_token_balance(wallet, ca.X7105, chain)
    x7105_price = x7105_balance * api.get_price(ca.X7105, chain)
    x7d_balance = api.get_token_balance(wallet, ca.X7D, chain)
    x7d_price = x7d_balance * native_price
    total = (
        x7d_price
        + x7r_price
        + x7dao_price
        + x7101_price
        + x7102_price
        + x7103_price
        + x7104_price
        + x7105_price
    )
    percentages = [round(balance / ca.SUPPLY * 100, 2) for balance in [x7dao_balance, x7101_balance, x7102_balance, x7103_balance, x7104_balance, x7105_balance]]
    if x7r_balance == 0:
        x7r_percent = 0
    else:
        x7r_percent = round(x7r_balance / api.get_x7r_supply(chain) * 100, 2)
    pioneers = api.get_pioneer_holdings(wallet, chain)
    maxis = api.get_maxi_holdings(wallet, chain)
    txs = api.get_daily_tx_count(wallet, chain)
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(chain_logo)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 10),
            f"X7 Finance Wallet Info {chain_name}\n\n"
            f"{eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(dollar)})\n\n"
            f"{x7r_balance} X7R {x7r_percent}% (${'{:0,.0f}'.format(x7r_price)})\n"
            f"{x7dao_balance} X7DAO {percentages[0]}% (${'{:0,.0f}'.format(x7dao_price)})\n"
            f"{x7101_balance} X7101 {percentages[1]}% (${'{:0,.0f}'.format(x7101_price)})\n"
            f"{x7102_balance} X7102 {percentages[2]}% (${'{:0,.0f}'.format(x7102_price)})\n"
            f"{x7103_balance} X7103 {percentages[3]}% (${'{:0,.0f}'.format(x7103_price)})\n"
            f"{x7104_balance} X7104 {percentages[4]}% (${'{:0,.0f}'.format(x7104_price)})\n"
            f"{x7105_balance} X7105 {percentages[5]}% (${'{:0,.0f}'.format(x7105_price)})\n"
            f"{x7d_balance} X7D (${'{:0,.0f}'.format(x7d_price)})\n"
            f"{pioneers} Pioneer NFTs\n"
            f"{maxis} Maxi NFTs\n"
            f"{txs} tx's in the last 24 hours\n\n"
            f"Total X7 Finance token value ${'{:0,.0f}'.format(total)}\n\n\n"
            f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        font = ImageFont.truetype(media.FONT, 24),
        fill = (255, 255, 255),
    )

    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*X7 Finance Wallet Info {chain_name}*\nUse `/wallet [wallet_address] [chain-name]` for other chains\n\n"
            f"`{wallet}`\n\n"
            f"{eth[:6]} {chain_native.upper()} (${'{:0,.0f}'.format(dollar)})\n\n"
            f"{x7r_balance} X7R {x7r_percent}% (${'{:0,.0f}'.format(x7r_price)})\n"
            f"{x7dao_balance} X7DAO {percentages[0]}% (${'{:0,.0f}'.format(x7dao_price)})\n"
            f"{x7101_balance} X7101 {percentages[1]}% (${'{:0,.0f}'.format(x7101_price)})\n"
            f"{x7102_balance} X7102 {percentages[2]}% (${'{:0,.0f}'.format(x7102_price)})\n"
            f"{x7103_balance} X7103 {percentages[3]}% (${'{:0,.0f}'.format(x7103_price)})\n"
            f"{x7104_balance} X7104 {percentages[4]}% (${'{:0,.0f}'.format(x7104_price)})\n"
            f"{x7105_balance} X7105 {percentages[5]}% (${'{:0,.0f}'.format(x7105_price)})\n"
            f"{x7d_balance} X7D (${'{:0,.0f}'.format(x7d_price)})\n"
            f"{pioneers} Pioneer NFTs\n"
            f"{maxis} Maxi NFTs\n\n"
            f"{txs} tx's in the last 24 hours\n\n"
            f"Total X7 Finance token value ${'{:0,.0f}'.format(total)}\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Wallet Link",
                        url=f"{chain_url}{wallet}",
                    )
                ],
            ]
        ),
    )


async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange", url=f"{url.XCHANGE}")],
                [
                    InlineKeyboardButton(
                        text="X7.Finance",
                        url=f"{url.WEBSITE_DEV}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7Finance.org",
                        url=f"{url.WEBSITE}",
                    )
                ],
            ]
        ),
    )


async def wei(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eth = " ".join(context.args)
    if eth == "":
        await update.message.reply_text("Please follow the command with the amount of eth you wish to convert")
    else:
        wei = int(float(eth) * 10**18)
        await update.message.reply_text(
            f"{eth} ETH is equal to \n" f"`{wei}` wei", parse_mode="Markdown"
        )


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


async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        word = " ".join(context.args).lower()
        if word == "":
            await update.message.reply_text(
                f"Please use /word followed by the word you want to search")
            return
        
        definition, audio_url = api.get_word(word)
        caption = f"*X7 Finance Dictionary*\n\n{word}:\n\n{definition}\n\n{api.get_quote()}"
        keyboard_markup = None
        
        if audio_url:
            keyboard_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Pronunciation", url=f"{audio_url}")]]
            )
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
        )
    except Exception:
        await update.message.reply_text("Word not found")


async def wp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f"*X7 Finance Whitepaper Quote*\n\n{random.choice(text.QUOTES)}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}")],
                [InlineKeyboardButton(text="Full WP", url=f"{url.WP_LINK}")],
            ]
        ),
    )


async def x7d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7D:
        chain_name, chain_url, chain_native = mappings.X7D[chain]
        native_price = api.get_native_price(chain_native)
        lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, chain)
        lpool_reserve_dollar = (float(lpool_reserve) * float(native_price) / 1**18)
        lpool = api.get_native_balance(ca.LPOOL, chain)
        lpool_dollar = (float(lpool) * float(native_price) / 1**18)
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        lpool_rounded = round(float(lpool), 2)
        lpool_reserve_rounded = round(float(lpool_reserve), 2)
        holders = api.get_holders(ca.X7D, chain)
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7D_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 28),
            f"X7D {chain_name} Info\n\n"
            f"Holders: {holders}\n\n"
            f'System Owned:\n{lpool_rounded} X7D (${"{:0,.0f}".format(lpool_dollar)})\n\n'
            f'External Deposits:\n{lpool_reserve_rounded} X7D (${"{:0,.0f}".format(lpool_reserve_dollar)})\n\n'
            f'Total Supply:\n{supply} X7D (${"{:0,.0f}".format(dollar)})\n\n'
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 28),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*X7D {chain_name} Info*\n"
            f"For other chains use `/x7d [chain-name]`\n\n"
            f"Holders: {holders}\n\n"
            f'System Owned:\n{lpool_rounded} X7D (${"{:0,.0f}".format(lpool_dollar)})\n\n'
            f'External Deposits:\n{lpool_reserve_rounded} X7D (${"{:0,.0f}".format(lpool_reserve_dollar)})\n\n'
            f'Total Supply:\n{supply} X7D (${"{:0,.0f}".format(dollar)})\n\n'
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7D Funding Dashboard",
                        url=f"{url.XCHANGE_FUND}",
                    )
                ],
            ]
        ),
    )


async def x7dao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7DAO:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7DAO[chain]
        holders = api.get_holders(ca.X7DAO, chain)
        price = api.get_price(ca.X7DAO, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7dao")
        volume = cg["x7dao"]["usd_24h_vol"]
        change = cg["x7dao"]["usd_24h_change"]
        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7dao")[1]}'
            ath_value = api.get_ath("x7dao")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"     
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        market_cap = "N/A"

    try:
        x7dao = api.get_liquidity(chain_pair, chain)
        x7dao_token = float(x7dao["reserve0"]) / 10**18
        x7dao_weth = float(x7dao["reserve1"]) / 10**18
        x7dao_token_dollar = float(price) * float(x7dao_token)
        native_price = api.get_native_price(chain_native)
        x7dao_weth_dollar = float(x7dao_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n'
            f'{x7dao_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7dao_weth_dollar)})\n'
            f"Total Liquidity ${float(x7dao_weth_dollar + x7dao_token_dollar):,.0f}"
        )

        ### REMOVE AT MIGRATION ###
    except Exception:
        x7dao_weth = api.get_native_balance(ca.X7DAO_LIQ_LOCK, chain)
        x7dao_weth_dollar = float(x7dao_weth) * native_price
        x7dao_token = 0
        x7dao_token_dollar = 0
        liquidity = f'{x7dao_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7dao_weth_dollar)})'
        ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7DAO_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7DAO Info {chain_name}\n\n"
            f"X7DAO Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7DAO Info {chain_name}\n\n"
            f"X7DAO Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7DAO}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7DAO}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7DAO}")],
            ]
        ),
    )


async def x7r(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7R:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7R[chain]
        holders = api.get_holders(ca.X7R, chain)
        price = api.get_price(ca.X7R, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7r")
        volume = cg["x7r"]["usd_24h_vol"]
        change = cg["x7r"]["usd_24h_change"]
        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * api.get_x7r_supply(chain))}'
        try:
            ath_change = f'{api.get_ath("x7r")[1]}'
            ath_value = api.get_ath("x7r")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * api.get_x7r_supply(chain))}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"        
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7r = api.get_liquidity(chain_pair, chain)
        x7r_token = float(x7r["reserve0"]) / 10**18
        x7r_weth = float(x7r["reserve1"]) / 10**18
        x7r_token_dollar = float(price) * float(x7r_token)
        native_price = api.get_native_price(chain_native)
        x7r_weth_dollar = float(x7r_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n'
            f'{x7r_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7r_weth_dollar)})\n'
            f"Total Liquidity ${float(x7r_weth_dollar + x7r_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7r_weth = api.get_native_balance(ca.X7R_LIQ_LOCK, chain)
        x7r_weth_dollar = float(x7r_weth) * native_price
        x7r_token = 0
        x7r_token_dollar = 0
        liquidity = f'{x7r_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7r_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7R_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7R Info {chain_name}\n\n"
            f"X7R Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7R Info {chain_name}\n\n"
            f"X7R Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  {market_cap}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7R}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7R}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7R}")],
            ]
        ),
    )


async def x7101(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7101:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7101[chain]
        holders = api.get_holders(ca.X7101, chain)
        price = api.get_price(ca.X7101, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7101")
        volume = cg["x7101"]["usd_24h_vol"]
        change = cg["x7101"]["usd_24h_change"]

        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7101")[1]}'
            ath_value = api.get_ath("x7101")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"     
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7101 = api.get_liquidity(chain_pair, chain)
        x7101_token = float(x7101["reserve0"]) / 10**18
        x7101_weth = float(x7101["reserve1"]) / 10**18
        x7101_token_dollar = float(price) * float(x7101_token)
        native_price = api.get_native_price(chain_native)
        x7101_weth_dollar = float(x7101_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7101_token)[:4]}M X7101 (${"{:0,.0f}".format(x7101_token_dollar)})\n'
            f'{x7101_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7101_weth_dollar)})\n'
            f"Total Liquidity ${float(x7101_weth_dollar + x7101_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7101_weth = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        x7101_weth_dollar = float(x7101_weth) * native_price
        x7101_token = 0
        x7101_token_dollar = 0
        liquidity = f'{x7101_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7101_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7101_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7101 Info {chain_name}\n\n"
            f"X7101 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity (X7100):\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7101 Info {chain_name}\n\n"
            f"X7101 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7101}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7101}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7101}")],
            ]
        ),
    )


async def x7102(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7102:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7102[chain]
        holders = api.get_holders(ca.X7102, chain)
        price = api.get_price(ca.X7102, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7102")
        volume = cg["x7102"]["usd_24h_vol"]
        change = cg["x7102"]["usd_24h_change"]
        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7102")[1]}'
            ath_value = api.get_ath("x7102")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"  
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7102 = api.get_liquidity(chain_pair, chain)
        x7102_token = float(x7102["reserve0"]) / 10**18
        x7102_weth = float(x7102["reserve1"]) / 10**18
        x7102_token_dollar = float(price) * float(x7102_token)
        native_price = api.get_native_price(chain_native)
        x7102_weth_dollar = float(x7102_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7102_token)[:4]}M X7102 (${"{:0,.0f}".format(x7102_token_dollar)})\n'
            f'{x7102_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7102_weth_dollar)})\n'
            f"Total Liquidity ${float(x7102_weth_dollar + x7102_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7102_weth = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        x7102_weth_dollar = float(x7102_weth) * native_price
        x7102_token = 0
        x7102_token_dollar = 0
        liquidity = f'{x7102_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7102_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7102_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7102 Info {chain_name}\n\n"
            f"X7102 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity (X7100):\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7102 Info {chain_name}\n\n"
            f"X7102 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7102}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7102}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7102}")],
            ]
        ),
    )


async def x7103(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7103:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7103[chain]
        holders = api.get_holders(ca.X7103, chain)
        price = api.get_price(ca.X7103, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7103")
        volume = cg["x7103"]["usd_24h_vol"]
        change = cg["x7103"]["usd_24h_change"]

        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7103")[1]}'
            ath_value = api.get_ath("x7103")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7103 = api.get_liquidity(chain_pair, chain)
        x7103_token = float(x7103["reserve0"]) / 10**18
        x7103_weth = float(x7103["reserve1"]) / 10**18
        x7103_token_dollar = float(price) * float(x7103_token)
        native_price = api.get_native_price(chain_native)
        x7103_weth_dollar = float(x7103_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7103_token)[:4]}M X7103 (${"{:0,.0f}".format(x7103_token_dollar)})\n'
            f'{x7103_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7103_weth_dollar)})\n'
            f"Total Liquidity ${float(x7103_weth_dollar + x7103_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7103_weth = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        x7103_weth_dollar = float(x7103_weth) * native_price
        x7103_token = 0
        x7103_token_dollar = 0
        liquidity = f'{x7103_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7103_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7103_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7103 Info {chain_name}\n\n"
            f"X7103 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity (X7100):\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7103 Info {chain_name}\n\n"
            f"X7103 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7103}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7103}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7103}")],
            ]
        ),
    )


async def x7104(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7104:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7104[chain]
        holders = api.get_holders(ca.X7104, chain)
        price = api.get_price(ca.X7104, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7104")
        volume = cg["x7104"]["usd_24h_vol"]
        change = cg["x7104"]["usd_24h_change"]
        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7104")[1]}'
            ath_value = api.get_ath("x7104")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7104 = api.get_liquidity(chain_pair, chain)
        x7104_token = float(x7104["reserve0"]) / 10**18
        x7104_weth = float(x7104["reserve1"]) / 10**18
        x7104_token_dollar = float(price) * float(x7104_token)
        native_price = api.get_native_price(chain_native)
        x7104_weth_dollar = float(x7104_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7104_token)[:4]}M X7104 (${"{:0,.0f}".format(x7104_token_dollar)})\n'
            f'{x7104_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7104_weth_dollar)})\n'
            f"Total Liquidity ${float(x7104_weth_dollar + x7104_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7104_weth = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        x7104_weth_dollar = float(x7104_weth) * native_price
        x7104_token = 0
        x7104_token_dollar = 0
        liquidity = f'{x7104_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7104_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7104_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7104 Info {chain_name}\n\n"
            f"X7104 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity (X7100):\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7104 Info {chain_name}\n\n"
            f"X7104 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7104}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7104}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7104}")],
            ]
        ),
    )


async def x7105(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.X7105:
        (
            chain_name,
            chain_url,
            chain_dext,
            chain_pair,
            chain_xchange,
            chain_scan,
            chain_native,
        ) = mappings.X7105[chain]
        holders = api.get_holders(ca.X7105, chain)
        price = api.get_price(ca.X7105, chain)
    if chain == "eth":
        cg = api.get_cg_price("x7105")
        volume = cg["x7105"]["usd_24h_vol"]
        change = cg["x7105"]["usd_24h_change"]
        if change == None or 0:
            change = 0
        else:
            change = round(change, 1)
        if volume == None or 0:
            volume = 0
        else:
            volume = f'${"{:0,.0f}".format(volume)}'
        market_cap = f'${"{:0,.0f}".format(price * ca.SUPPLY)}'
        try:
            ath_change = f'{api.get_ath("x7105")[1]}'
            ath_value = api.get_ath("x7105")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        except Exception:
            ath = "Unavailable"
        
    else:
        volume = "N/A"
        change = "N/A"
        ath = "N/A"
        holders = "N/A"
        market_cap = "N/A"

    try:
        x7105 = api.get_liquidity(chain_pair, chain)
        x7105_token = float(x7105["reserve0"]) / 10**18
        x7105_weth = float(x7105["reserve1"]) / 10**18
        x7105_token_dollar = float(price) * float(x7105_token)
        native_price = api.get_native_price(chain_native)
        x7105_weth_dollar = float(x7105_weth) * float(native_price)

        liquidity = (
            f'{"{:0,.0f}".format(x7105_token)[:4]}M X7105 (${"{:0,.0f}".format(x7105_token_dollar)})\n'
            f'{x7105_weth:.0f} {chain_native.upper()} (${"{:0,.0f}".format(x7105_weth_dollar)})\n'
            f"Total Liquidity ${float(x7105_weth_dollar + x7105_token_dollar):,.0f}"
        )
    ### REMOVE AT MIGRATION ###
    except Exception:
        x7105_weth = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        x7105_weth_dollar = float(x7105_weth) * native_price
        x7105_token = 0
        x7105_token_dollar = 0
        liquidity = f'{x7105_weth} {chain_native.upper()}\n(${"{:0,.0f}".format(x7105_weth_dollar)})'
    ###
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.X7105_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (28, 36),
            f"X7105 Info {chain_name}\n\n"
            f"X7105 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f"Market Cap: {market_cap}\n"
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity (X7100):\n"
            f"{liquidity}\n\n"
            f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        font = ImageFont.truetype(media.FONT, 25),
        fill = (255, 255, 255),
    )
    img_path = os.path.join("media", "blackhole.png")
    im1.save(img_path)
    await update.message.reply_photo(
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"X7105 Info {chain_name}\n\n"
            f"X7105 Price: ${round(price, 8)}\n"
            f"24 Hour Change: {change}%\n"
            f'Market Cap:  ${"{:0,.0f}".format(price * ca.SUPPLY)}\n'
            f"24 Hour Volume: {volume}\n"
            f"ATH: {ath}\n"
            f"Holders: {holders}\n\n"
            f"Liquidity:\n"
            f"{liquidity}\n\n"
            f"Contract Address:\n`{ca.X7105}`\n\n"
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=chain_scan, url=f"{chain_url}{ca.X7105}")],
                [InlineKeyboardButton(text="Chart", url=f"{chain_dext}{chain_pair}")],
                [InlineKeyboardButton(text="Buy", url=f"{chain_xchange}{ca.X7105}")],
            ]
        ),
    )
