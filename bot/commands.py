from telegram import *
from telegram.ext import *

import os, pytz, random, re, requests, textwrap, time as t, wikipediaapi
from datetime import datetime, timedelta, timezone
from gtts import gTTS

from eth_utils import to_checksum_address
from translate import Translator
from PIL import Image, ImageDraw, ImageFont
from web3 import Web3

from constants import ca, dao, loans, mappings, nfts, splitters, tax, text, urls  
from hooks import api, db, dune 
import media
from variables import times, giveaway


dextools = api.Dextools()
coingecko = api.CoinGecko()
defined = api.Defined()
opensea = api.Opensea()


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{text.ABOUT}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Xchange App", url=f"{urls.XCHANGE}")],
                [InlineKeyboardButton(text="Website", url=f"{urls.WEBSITE}")],
            ]
        ),
    )


async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    administrators = await context.bot.get_chat_administrators(-1001780235511)
    community_team = [f"@{admin.user.username}" for admin in administrators if 'community team' in admin.custom_title.lower()]
    og = [f"@{admin.user.username}" for admin in administrators if 'og' in admin.custom_title.lower()]
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=(
            "*X7 Finance Telegram Admins*\n\n"
            "Community Team:\n" + "\n".join(community_team) +
            "\n\nOGs:\n" + "\n".join(og) +
            f"\n\n{api.get_quote()}"
        ),
        parse_mode="Markdown",
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
                [InlineKeyboardButton(text="XChange Alerts", url=f"{urls.TG_ALERTS}")],
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
        ath, ath_change, date = coingecko.get_ath(coin)
        ath_change_str = f"{ath_change}"
        return ath, ath_change_str[:3], date
    
    try:
        x7r_ath, x7r_ath_change, x7r_date = get_ath_info("x7r")
        x7r_date_object = datetime.fromisoformat(x7r_date.replace("Z", "+00:00"))
        x7r_readable_date = x7r_date_object.strftime("%Y-%m-%d %H:%M:%S")
        x7r_mcap = x7r_ath * api.get_x7r_supply("eth")
        x7r_ath = (
            f'${x7r_ath} (${"{:0,.0f}".format(x7r_mcap)})\n'
            f'{x7r_ath_change}%\n'
            f'{x7r_readable_date}'
            )
    except Exception:
        x7r_ath = "Unavaliable"

    try:
        x7dao_ath, x7dao_ath_change, x7dao_date = get_ath_info("x7dao")
        x7dao_date_object = datetime.fromisoformat(x7dao_date.replace("Z", "+00:00"))
        x7dao_readable_date = x7dao_date_object.strftime("%Y-%m-%d %H:%M:%S")
        x7dao_mcap = x7dao_ath * ca.SUPPLY
        x7dao_ath = (
            f'${x7dao_ath} (${"{:0,.0f}".format(x7dao_mcap)})\n'
            f'{x7dao_ath_change}%\n'
            f'{x7dao_readable_date}'
            )
    except Exception:
        x7dao_ath = "Unavaliable"
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
                        text="X7 Finance Blog", url=f"{urls.WEBSITE}blog"
                    )
                ],
            ]
        ),
    )


async def borrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) ==  2:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        amount= context.args[0]
        amount_in_wei = int(float(amount) * 10 ** 18)
        chain = context.args[1]
    else:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Loan Rates*\n\n"
                "Follow the /borrow command with an amount and chain\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown"
            )
        return
    if chain in mappings.CHAINS:
        chain_name = mappings.CHAINS[chain].name
        chain_web3 = mappings.CHAINS[chain].w3
        chain_native =  mappings.CHAINS[chain].token
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    message = await update.message.reply_text("Getting Loan Rates Info, Please wait...")

    loan_info = ""
    native_price = api.get_native_price(chain_native)
    borrow_usd = native_price * float(amount)
    for loan_key, loan_term in loans.LOANS.items():
        loan_contract = chain_web3.eth.contract(
            address=Web3.to_checksum_address(loan_term.ca), abi=api.get_abi(loan_term.ca, chain)
        )
        loan_data = loan_contract.functions.getQuote(int(amount_in_wei)).call()
        origination_fee, total_premium = [value / 10**18 for value in loan_data[1:]]
        origination_dollar, total_premium_dollar = [value * native_price for value in [origination_fee, total_premium]]
        
        loan_info += (
            f"*{loan_term.name}*\n"
            f"Origination Fee: {origination_fee} {chain_native.upper()} (${origination_dollar:,.0f})\n"
            f"Premium Fees: {total_premium} {chain_native.upper()} (${total_premium_dollar:,.0f})\n"
            f"Total Cost: {total_premium + origination_fee} {chain_native.upper()} (${origination_dollar + total_premium_dollar:,.0f})\n\n"
        )
    await message.delete()
    await update.message.reply_photo(
    photo=api.get_random_pioneer(),
    caption=
        f"*X7 Finance Loan Rates {chain_name}*\n\n"
        f"Borrowing {amount} {chain_native.upper()} (${borrow_usd:,.0f}) will cost:\n\n"
        f"{loan_info}"

        f"{api.get_quote()}",
    parse_mode="Markdown"
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
    price,_ = dextools.get_price(ca.X7R, "eth")
    burn_dollar = float(price) * float(burn)
    native = f"{str(burn_dollar / api.get_native_price(chain_native))[:5]} {chain_native.upper()}"
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
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
                text="DAO Proposers Chat", url=f"{urls.TG_DAO}",
            ),
            InlineKeyboardButton(
                text="Xchange Alerts", url="https://t.me/x7_alerts"
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
        dext = mappings.CHAINS[chain].dext
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
                        text="X7R - Rewards Token", url=f"https://www.dextools.io/app/{dext}/pair-explorer/{ca.X7R}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7DAO - Governance Token",
                        url=f"https://www.dextools.io/app/{dext}/pair-explorer/{ca.X7DAO}",
                    )
                ],
            ]
        ),
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first = context.args[0]
    second = context.args[1]
    differences = [(i, j) for i, j in zip(first, second) if i != j]

    if not differences:
        reply = "✅ Both inputs match"
    else:
        mismatch_details = "\n".join([f"'{char1}' vs '{char2}'" for i, (char1, char2) in enumerate(differences)])
        reply = f"❌ Inputs do not match\n\nDifferences:\n{mismatch_details}"
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
    if x7token not in token_names:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Market Cap Comparison*\n\n"
                f"Please enter X7 token first followed by token to compare\n\n"
                f"ie. `/compare x7r uni`\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )
        return
    
    token2 = context.args[1].lower()
    search = coingecko.search(token2)
    if "coins" in search and search["coins"]:
        token_id = search["coins"][0]["api_symbol"]
    else:
        await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Market Cap Comparison*\n\n"
                    f"No Market Cap data found for {token2.upper()}\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown",
            )
        return

    token_market_cap = coingecko.get_mcap(token_id)
    if token_market_cap == 0:
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Market Cap Comparison*\n\n"
                f"No Market Cap data found for {token2.upper()}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )
        return
    if x7token == ca.X7R:
        x7_supply = api.get_x7r_supply("eth")
    else:
        x7_supply = ca.SUPPLY
    token_info = token_names[x7token]
    x7_price,_ = dextools.get_price(token_info["contract"], "eth")
    x7_market_cap = float(x7_price) * float(x7_supply)
    percent = ((token_market_cap - x7_market_cap) / x7_market_cap) * 100
    x = (token_market_cap - x7_market_cap) / x7_market_cap
    token_value = token_market_cap / x7_supply
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Market Cap Comparison*\n\n"
            f"{context.args[1].upper()} Market Cap:\n"
            f'${"{:,.0f}".format(token_market_cap)}\n\n'
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


async def constellations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    price = coingecko.get_price("x7101, x7102, x7103, x7104, x7105")
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
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
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
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        amount = context.args[0]
        search = context.args[1]
        token = coingecko.search(search.lower())
        if token and "coins" in token and len(token["coins"]) > 0:
            token_id = token["coins"][0]["api_symbol"]
            thumb = token["coins"][0]["large"]
            cg = coingecko.get_price(token_id)
            price = cg[token_id]["usd"]
            output = float(amount) * float(price)
            caption_text = f"{amount} {token_id.upper()} is currently worth:\n${'{:0,.0f}'.format(output)}"
            if amount == "500000" and search == "x7dao":
                proposers = api.get_proposers("eth")
                caption_text +=f"\n\nDAO Proposers: {proposers}"
                
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance Price Conversion*\n\n"
                    f"{caption_text}\n\n"
                    f"{api.get_quote()}",
                parse_mode="Markdown")
        else:
            await update.message.reply_text(f"{search.upper()} Not Found")
    else:
        await update.message.reply_text("Please follow command with amount and token name you wish to convert")


async def costs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        web3 = mappings.CHAINS[chain].w3
        native = mappings.CHAINS[chain].token
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    gas_price = web3.eth.gas_price / 10**9
    eth_price = api.get_native_price("eth")

    try:
        pair_data = "0xc9c65396" + ca.WETH[2:].lower().rjust(64, '0') + ca.DEAD[2:].lower().rjust(64, '0')
        pair_gas_estimate = web3.eth.estimate_gas({
            'from': web3.to_checksum_address(ca.DEPLOYER),
            'to': web3.to_checksum_address(ca.FACTORY),
            'data': pair_data,})
        pair_cost_in_eth = gas_price * pair_gas_estimate
        pair_cost_in_dollars = (pair_cost_in_eth / 10**9)* eth_price
        pair_text = f"Create Pair: {pair_cost_in_eth / 10**9:.2f} {native.upper()} (${pair_cost_in_dollars:.2f})"
    except Exception:
        pair_text = "Create Pair: N/A"
    split_data = "0x11ec9d34"
    try:
        eco_split_gas = web3.eth.estimate_gas({
            'from': web3.to_checksum_address(ca.DEPLOYER),
            'to': web3.to_checksum_address(ca.ECO_SPLITTER),
            'data': split_data,})
        eco_split_eth = gas_price * eco_split_gas
        eco_split_dollars = (eco_split_eth / 10**9)* eth_price
        eco_split_text = f"Ecosystem Splitter Push: {eco_split_eth / 10**9:.3f} {native.upper()} (${eco_split_dollars:.2f})"
    except Exception:
        eco_split_text = "Ecosystem Splitter Push: N/A"
    try:
        treasury_split_gas = web3.eth.estimate_gas({
            'from': web3.to_checksum_address(ca.DEPLOYER),
            'to': web3.to_checksum_address(ca.TREASURY_SPLITTER),
            'data': split_data,})
        treasury_split_eth = gas_price * treasury_split_gas
        treasury_split_dollars = (treasury_split_eth / 10**9)* eth_price
        treasury_split_text = f"Treasury Splitter Push: {treasury_split_eth / 10**9:.3f} {native.upper()} (${treasury_split_dollars:.2f})"
    except Exception:
        treasury_split_text = "Treasury Splitter Push: N/A"

    try:
        deposit_data = "0xf6326fb3"
        deposit_gas = web3.eth.estimate_gas({
            'from': web3.to_checksum_address(ca.DEPLOYER),
            'to': web3.to_checksum_address(ca.LPOOL_RESERVE),
            'data': deposit_data,})
        deposit_eth = gas_price * deposit_gas
        deposit_dollars = (deposit_eth / 10**9)* eth_price
        deposit_text = f"Mint X7D: {deposit_eth / 10**9:.3f} {native.upper()} (${deposit_dollars:.2f})"
    except Exception:
        deposit_text = "Mint X7D: N/A"
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*Live Xchange Costs ({chain.upper()})*\nUse `/costs [chain-name]` for other chains\n\n"
            f"{pair_text}\n"
            f"{eco_split_text}\n"
            f"{treasury_split_text}\n"
            f"{deposit_text}\n\n"
            f"{api.get_quote()}",
        parse_mode = "markdown")


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
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    buttons = []
    input_contract = " ".join(context.args).lower()
    contract_names = list(dao.CONTRACT_MAPPINGS.keys())
    formatted_contract_names = '\n'.join(contract_names)
    keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Vote Here",url=urls.SNAPSHOT,)],
            [InlineKeyboardButton(text="DAO Proposers Chat",url=urls.TG_DAO,)],])
    if not input_contract:
        x7dao_proposers = api.get_proposers("eth")
        info = dextools.get_token_info(ca.X7DAO, "eth")
        holders = info["holders"]
        snapshot = api.get_snapshot()
        end = datetime.utcfromtimestamp(snapshot["data"]["proposals"][0]["end"])
        duration = end - datetime.utcnow()
        days, hours, minutes = api.get_duration_days(duration)
        if snapshot["data"]["proposals"][0]["state"] == "active":
            end_status = f'Vote Closing: {end.strftime("%Y-%m-%d %H:%M:%S")} UTC\n{days} days, {hours} hours and {minutes} minutes\n\n'
            header = 'Current Open Proposal'
            buttons.extend([
            [InlineKeyboardButton(
                text="Vote Here",
                url=f"{urls.SNAPSHOT}/proposal/{snapshot['data']['proposals'][0]['id']}")
            ],
            [InlineKeyboardButton(
                text="X7 Finance DAO",
                url=f"{urls.TG_DAO}")
            ],
            [InlineKeyboardButton(
                    text="DAO Proposers Chat",
                    url=f"{urls.TG_DAO}")
            ]
            ])
        else:
            end_status = f'Vote Closed: {end.strftime("%Y-%m-%d %H:%M:%S")}'
            header = 'No Current Open Proposal\n\nLast Proposal:'
            buttons.extend([
            [InlineKeyboardButton(
                text="X7 Finance DAO",
                url=f"{urls.SNAPSHOT}")
            ],
            [InlineKeyboardButton(
                text="DAO Proposers Chat",
                url=f"{urls.TG_DAO}")
            ]
            ])
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f'*X7 Finance DAO*\n'
                f'use `/dao functions` for a list of call callable contracts\n\n'
                f"X7DAO Holders: {holders}\n"
                f"X7DAO Proposers: {x7dao_proposers}\n\n"
                f'*{header}*\n\n'
                f'{snapshot["data"]["proposals"][0]["title"]} by - '
                f'{snapshot["data"]["proposals"][0]["author"][-5:]}\n\n'
                f'{snapshot["data"]["proposals"][0]["choices"][0]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][0])} Votes\n'
                f'{snapshot["data"]["proposals"][0]["choices"][1]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][1])} Votes\n'
                f'{snapshot["data"]["proposals"][0]["choices"][2]} - '
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores"][2])} Votes\n\n'
                f'{"{:0,.0f}".format(snapshot["data"]["proposals"][0]["scores_total"])} Total Votes\n\n'
                f'{end_status}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    else:
        if input_contract == "functions":
            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance DAO*\n\nUse `/dao [contract-name]` for a list of DAO callable functions\n\n"
                    f"*Contract Names:*\n\n{formatted_contract_names}\n\n",
                parse_mode="Markdown",
                reply_markup=keyboard
                )
        else:
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
                    f"*X7 Finance DAO Functions* - {contract}\n\n"
                    f"The following functions can be called on the {contract} contract:\n\n"
                    f"{contract_text}",
                parse_mode="Markdown",
                reply_markup=keyboard
                )
            else:
                await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=
                    f"*X7 Finance DAO Functions*\n\n"
                    f"'{input_contract}' not found - Use `/dao` followed by one of the contract names below:\n\n"
                    f"{formatted_contract_names}",
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
                            url=f'{urls.ETHER_TX}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains",
                            url=f"{urls.WEBSITE}docs/onchains",
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
                            url=f'{urls.ETHER_TX}{tx["result"][0]["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains",
                            url=f"{urls.WEBSITE}docs/onchains",
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
                        url=f"{urls.ETHER_ADDRESS}{ca.LENDING_DISCOUNT}#code",
                    )
                ],
            ]
        ),
    )


async def docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(text="Get Started", url=f"{urls.WEBSITE}getstarted/"),
            InlineKeyboardButton(text="Trader", url=f"{urls.WEBSITE}docs/guides/trade/"),
        ],
        [
            InlineKeyboardButton(text="Liquidity Provider", url=f"{urls.WEBSITE}docs/guides/liquidity-provider/"),
            InlineKeyboardButton(text="Capital Allocator", url=f"{urls.WEBSITE}docs/guides/lending/"),
        ],
        [
            InlineKeyboardButton(text="Project Engineer", url=f"{urls.WEBSITE}docs/guides/integrate-ui/"),
            InlineKeyboardButton(text="Project Launcher", url=f"{urls.WEBSITE}docs/guides/launch/"),

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
    message = await update.message.reply_text("Getting Buy Back Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    now = datetime.utcnow()
    def get_liquidity_data(hub_address):
        hub = api.get_internal_tx(hub_address, chain)
        hub_filter = [d for d in hub["result"] if d["from"] in f"{hub_address}".lower()]
        value_raw = int(hub_filter[0]["value"]) / 10**18
        value = round(value_raw, 3) 
        dollar = float(value) * float(api.get_native_price(chain_native))
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
    await message.delete()
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
                [InlineKeyboardButton(text="Xchange App", url=f"{urls.XCHANGE}")],
                [InlineKeyboardButton(text="Website", url=f"{urls.WEBSITE}")],
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
            InlineKeyboardButton(text="ETH", url=f"{urls.ETHER_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="BSC", url=f"{urls.BSC_ADDRESS}{ca.FACTORY}"),
        ],
        [
            InlineKeyboardButton(text="Polygon", url=f"{urls.POLY_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="Arbitrum", url=f"{urls.ARB_ADDRESS}{ca.FACTORY}"),
        ],
        [
            InlineKeyboardButton(text="Optimism", url=f"{urls.OPTI_ADDRESS}{ca.FACTORY}"),
            InlineKeyboardButton(text="Base", url=f"{urls.BASE_ADDRESS}{ca.FACTORY}"),
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
    dollar = float(value) * float(api.get_native_price(chain_native))
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


async def fg(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    caption += f'{fear_values[0][0]} - {fear_values[0][1]} - {fear_values[0][2].strftime("%B %d")}\n\n'
    caption += "Change:\n"
    for i in range(1, 7):
        caption += f'{fear_values[i][0]} - {fear_values[i][1]} - {fear_values[i][2].strftime("%B %d")}\n'
    caption += "\nNext Update:\n"
    caption += (
        f"{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}"
    )
    await update.message.reply_photo(
        photo=f"https://alternative.me/crypto/fear-and-greed-index.png?timestamp={int(t.time())}",
        caption=caption,
        parse_mode="Markdown",
    )
   

async def gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    if chain == "":
        chain = "eth"
    if chain in mappings.CHAINS:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        chain_name = mappings.CHAINS[chain].name
        chain_url = mappings.CHAINS[chain].gas
        chain_logo = mappings.CHAINS[chain].logo
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return

    gas_data = api.get_gas(chain)
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
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
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*{giveaway.NAME}*\n\n{giveaway.TEXT}\n\n"
                f"Ends:\n\n{giveaway.TIME.strftime('%A %B %d %Y %I:%M %p')} UTC\n\n"
                f"{days} days, {hours} hours and {minutes} minutes\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            )


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
    x7dao_proposers = api.get_proposers(chain)
    x7dao_info = dextools.get_token_info(ca.X7DAO, "eth")
    x7dao_holders = x7dao_info["holders"]
    x7r_info = dextools.get_token_info(ca.X7D, "eth")
    x7r_holders = x7r_info["holders"]
    x7d_info = dextools.get_token_info(ca.X7D, "eth")
    x7d_holders = x7d_info["holders"]
    
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Token Holders {chain_name}*\n"
            f"For other chains use `/holders [chain-name]`\n\n"
            f"X7R:        {x7r_holders}\n"
            f"X7DAO:  {x7dao_holders}\n"
            f"X7DAO ≥ 500K: {x7dao_proposers}\n"
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
    await context.bot.delete_message(update.effective_chat.id, update.message.id)
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
            caption=f'{joke["setup"]}\n\n{joke["delivery"]}',
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
                        url=f"{urls.ETHER_TX}0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Migration Go Live TX",
                        url=f"{urls.ETHER_TX}0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41",
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
            InlineKeyboardButton(text="Xchange App", url=f"{urls.XCHANGE}"),
            InlineKeyboardButton(text="Website", url=f"{urls.WEBSITE}"),
        ],
        [
            InlineKeyboardButton(text="Snapshot", url=f"{urls.SNAPSHOT}"),
            InlineKeyboardButton(text="Twitter", url=f"{urls.TWITTER}"),
        ],
        [
            InlineKeyboardButton(text="Reddit", url=f"{urls.REDDIT}"),
            InlineKeyboardButton(text="Youtube", url=f"{urls.YOUTUBE}"),
        ],
        [
            InlineKeyboardButton(text="Github", url=f"{urls.GITHUB}"),
            InlineKeyboardButton(text="Dune", url=f"{urls.DUNE}"),
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
        pair_addresses = mappings.CHAINS[chain].pairs
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    message = await update.message.reply_text("Getting Liquidity Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    if chain == "eth":
        all_liquidity = []

        for contract_address, pair in zip(ca.TOKENS, pair_addresses):
            liquidity = dextools.get_liquidity(pair, chain)
            all_liquidity.append(liquidity)

        def clean_liquidity(liquidity):
            if liquidity == 'N/A':
                return 0
            else:
                return float(liquidity.replace('$', '').replace(',', ''))

        cleaned_liquidity = [clean_liquidity(liquidity) for liquidity in all_liquidity]

        x7r_liq = cleaned_liquidity[0]
        x7dao_liq = cleaned_liquidity[1]
        constellations_liq = sum(cleaned_liquidity[2:7])
        total_liq = sum(cleaned_liquidity)

        await message.delete()
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Token Liquidity (ETH)*\n"
                f"For other chains, Use `/liquidity [chain-name]`\n\n"
                f"X7R:\n"
                f"${x7r_liq:,.0f}\n\n"
                f"X7DAO:\n"
                f"${x7dao_liq:,.0f}\n\n"
                f"X7100:\n"
                f"${constellations_liq:,.0f}\n\n"
                f"Total: ${total_liq:,.0f}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
        )
    ### REMOVE AFTER MIGRATION
    else:
        x7r_amount = api.get_native_balance(ca.X7R_LIQ_LOCK, chain)
        x7dao_amount = api.get_native_balance(ca.X7DAO_LIQ_LOCK, chain)
        cons_amount = api.get_native_balance(ca.CONS_LIQ_LOCK, chain)
        native_price = api.get_native_price(chain_native)
        x7dao_dollar = (float(x7dao_amount) * float(native_price))
        x7r_dollar = (float(x7r_amount) * float(native_price))
        cons_dollar = (float(cons_amount) * float(native_price))
        total = float(cons_dollar) + float(x7dao_dollar) + float(x7r_dollar)

        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Initial Liquidity {chain_name}*\nUse `/liquidity [chain-name]` for other chains\n\n"
                f'X7R:\n{x7r_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7r_dollar)})\n\n'
                f'X7DAO:\n{x7dao_amount} {chain_native.upper()} (${"{:0,.0f}".format(x7dao_dollar)})\n\n'
                f'X7100:\n{cons_amount} {chain_native.upper()} (${"{:0,.0f}".format(cons_dollar)})\n\n'
                f'Total:\n${"{:0,.0f}".format(total)}\n\n'
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
    message = await update.message.reply_text("Getting Liquidation Info, Please wait...")
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
    await message.delete()
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
            f"Please use `/loan [ID] [chain]` to see details",
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
        message = await update.message.reply_text("Getting Loan Info, Please wait...")
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        url = "https://lb.drpc.org/ogrpc?network="
        networks = {
            "ETH": (f"{url}ethereum&dkey={os.getenv('DRPC_API_KEY')}", ca.LPOOL),
            "ARB": (f"{url}arbitrum&dkey={os.getenv('DRPC_API_KEY')}", ca.LPOOL_V1),
            "BSC": ("https://bsc-dataseed.binance.org/", ca.LPOOL_V1),
            "POLY": (f"{url}polygon&dkey={os.getenv('DRPC_API_KEY')}", ca.LPOOL_V1),
            "OPTI": (f"{url}optimism&dkey={os.getenv('DRPC_API_KEY')}", ca.LPOOL_V1),
            "BASE": ("https://mainnet.base.org", ca.LPOOL_V1),
        }
        contract_instances = {}
        for network, (web3_url, pool_contract) in networks.items():
            web3 = Web3(Web3.HTTPProvider(web3_url))
            contract = web3.eth.contract(
                address=to_checksum_address(pool_contract),
                abi=api.get_abi(pool_contract, network.lower()),
            )
            amount = contract.functions.nextLoanID().call() - 1
            contract_instances[network] = amount
        await message.delete()
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Loan Count*\n"
                f"Use `/loans info` for ILL info\n"
                f"Use `/loan [ID] [chain]` for Individual loan details\n\n"
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
        return
    if loan_type == "info":
        await update.message.reply_text(
            f"{loans.OVERVIEW}\n\n{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Finance Whitepaper", url=f"{urls.WP_LINK}"
                        )
                    ],
                ]
            ),
        )
        return
    else:
        if loan_type in loans.LOANS:
            loan_terms = loans.LOANS[loan_type]
            buttons = [
                [
                    InlineKeyboardButton(text="Ethereum", url=f"{urls.ETHER_ADDRESS}{loan_terms.ca}"),
                    InlineKeyboardButton(text="BSC", url=f"{urls.BSC_ADDRESS}{loan_terms.ca}"),
                ],
                [
                    InlineKeyboardButton(text="Polygon", url=f"{urls.POLY_ADDRESS}{loan_terms.ca}"),
                    InlineKeyboardButton(text="Arbitrum", url=f"{urls.ARB_ADDRESS}{loan_terms.ca}"),
                ],
                [
                    InlineKeyboardButton(text="Optimism", url=f"{urls.OPTI_ADDRESS}{loan_terms.ca}"),
                    InlineKeyboardButton(text="Base", url=f"{urls.BASE_ADDRESS}{loan_terms.ca}"),
                ],
            ]

            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=f"{loan_terms.name}\n{loan_terms.generate_terms()}\n\n",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
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
            prefix = "away"
        else:
            time_remaining = now - unlock_datetime
            prefix = "ago"

        years = time_remaining.days // 365
        months = (time_remaining.days % 365) // 30
        days = (time_remaining.days % 365) % 30
        hours, remainder = divmod(time_remaining.seconds, 3600)
        weeks = days // 7
        days = days % 7

        remaining_time_str = f"{years} years, {months} months, {weeks} weeks, {days} days, and {hours} hours {prefix}"
        unlock_datetime_str = unlock_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

        return remaining_time_str, unlock_datetime_str
        
    address = to_checksum_address(ca.TIME_LOCK)
    contract = web3.eth.contract(address=address, abi=api.get_abi(ca.TIME_LOCK, chain))
    now = datetime.utcnow()

    x7r_remaining_time_str, x7r_unlock_datetime_str = calculate_remaining_time(web3, contract, x7r_pair, now)
    x7dao_remaining_time_str, x7dao_unlock_datetime_str = calculate_remaining_time(web3, contract, x7dao_pair, now)
    x7d_remaining_time_str, x7d_unlock_datetime_str = calculate_remaining_time(web3, contract, ca.X7D, now)

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Liquidity Locks* {chain_name}\nfor other chains use `/locks [chain-name]`\n\n"
            f"*X7R Unlock Date:*\n{x7r_unlock_datetime_str}\n"
            f"{x7r_remaining_time_str}\n\n"
            f"*X7DAO Unlock Date*:\n{x7dao_unlock_datetime_str}\n"
            f"{x7dao_remaining_time_str}\n\n"
            f"*X7D Unlock Date*:\n{x7d_unlock_datetime_str}\n"
            f"{x7d_remaining_time_str}\n\n"
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
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return

    data = api.get_nft_data(ca.MAGISTER, chain)
    holders = data["holder_count"]
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
    token_names = {
        ca.X7R: "X7R",
        ca.X7DAO: "X7DAO",
        ca.X7101: "X7101",
        ca.X7102: "X7102",
        ca.X7103: "X7103",
        ca.X7104: "X7104",
        ca.X7105: "X7105",
    }
    caps_info = {}
    caps = {}
    for token in ca.TOKENS:
        caps_info[token] = dextools.get_token_info(token, chain)
        caps[token] = caps_info[token]["mcap"]

    total_mcap = 0
    for token, mcap in caps.items():
        if mcap == 'N/A':
            continue
        mcap_value = float(''.join(filter(str.isdigit, mcap)))
        total_mcap += mcap_value

    total_cons = 0
    for token, mcap in caps.items():
        if token in (ca.X7DAO, ca.X7R):
            continue
        if mcap == 'N/A':
            continue
        cons_mcap_value = float(''.join(filter(str.isdigit, mcap)))
        total_cons += cons_mcap_value

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Market Cap Info {chain_name}*\n\n"
            f'`X7R: `            {caps[ca.X7R]}\n'
            f'`X7DAO:`         {caps[ca.X7DAO]}\n'
            f'`X7101:`         {caps[ca.X7101]}\n'
            f'`X7102:`         {caps[ca.X7102]}\n'
            f'`X7103:`         {caps[ca.X7103]}\n'
            f'`X7104:`         {caps[ca.X7104]}\n'
            f'`X7105:`         {caps[ca.X7105]}\n\n'
            f'`Constellations Combined:` ${total_cons:,.0f}\n'
            f'`Total Market Cap:` ${total_mcap:,.0f}\n\n'
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
    message = await update.message.reply_text("Getting NFT Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chain_prices = nfts.MINT_PRICES()
    chain_data = nfts.DATA()
    chain_discount = nfts.DISCOUNTS()

    eco_price = chain_prices.get(chain, {}).get("eco")
    liq_price = chain_prices.get(chain, {}).get("liq")
    dex_price = chain_prices.get(chain, {}).get("dex")
    borrow_price = chain_prices.get(chain, {}).get("borrow")
    magister_price = chain_prices.get(chain, {}).get("magister")

    eco_floor = chain_data.get(chain, {}).get("eco", {}).get("floor_price")
    liq_floor = chain_data.get(chain, {}).get("liq", {}).get("floor_price")
    dex_floor = chain_data.get(chain, {}).get("dex", {}).get("floor_price")
    borrow_floor = chain_data.get(chain, {}).get("borrow", {}).get("floor_price")
    magister_floor = chain_data.get(chain, {}).get("magister", {}).get("floor_price")

    eco_count = chain_data.get(chain, {}).get("eco", {}).get("holder_count")
    liq_count = chain_data.get(chain, {}).get("liq", {}).get("holder_count")
    dex_count = chain_data.get(chain, {}).get("dex", {}).get("holder_count")
    borrow_count = chain_data.get(chain, {}).get("borrow", {}).get("holder_count")
    magister_count = chain_data.get(chain, {}).get("magister", {}).get("holder_count")

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
            InlineKeyboardButton(text="OS - Ecosystem Maxi", url=f"{urls.OS_ECO}{chain_os}"),
        ],
        [
            InlineKeyboardButton(text="OS - Liquidity Maxi", url=f"{urls.OS_LIQ}{chain_os}"),
            InlineKeyboardButton(text="OS - DEX Maxi", url=f"{urls.OS_DEX}{chain_os}"),
        ],
        [
            InlineKeyboardButton(text="OS - Borrowing Maxi", url=f"{urls.OS_BORROW}{chain_os}"),
            InlineKeyboardButton(text="OS - Magister", url=f"{urls.OS_MAGISTER}{chain_os}"),
        ],
    ]

    await message.delete()
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*NFT Info {chain_name}*\nUse `/nft [chain-name]` for other chains\n\n"
            f"*Ecosystem Maxi*\n{eco_price}\n"
            f"Available - {500 - eco_count}\nFloor price - {eco_floor} {chain_native.upper()}\n"
            f"{eco_discount_text}\n\n"
            f"*Liquidity Maxi*\n{liq_price}\n"
            f"Available - {250 - liq_count}\nFloor price - {liq_floor} {chain_native.upper()}\n"
            f"{liq_discount_text}\n\n"
            f"*Dex Maxi*\n{dex_price}\n"
            f"Available - {150 - dex_count}\nFloor price - {dex_floor} {chain_native.upper()}\n"
            f"{dex_discount_text}\n\n"
            f"*Borrow Maxi*\n{borrow_price}\n"
            f"Available - {100 - borrow_count}\nFloor price - {borrow_floor} {chain_native.upper()}\n"
            f"{borrow_discount_text}\n\n"
            f"*Magister*\n{magister_price}\n"
            f"Available - {49 - magister_count}\nFloor price - {magister_floor} {chain_native.upper()}\n"
            f"{magister_discount_text}\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def on_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    tx= api.get_tx(ca.DEPLOYER, "eth")
    tx_filter = [d for d in tx["result"] if d["to"] in f"{ca.DEAD}".lower()]
    recent_tx = max(tx_filter, key=lambda tx: int(tx["timeStamp"]), default=None)
    message = bytes.fromhex(recent_tx["input"][2:]).decode("utf-8")
    time = datetime.utcfromtimestamp(int(recent_tx["timeStamp"]))
    duration = datetime.utcnow() - time
    days, hours, minutes = api.get_duration_days(duration)
    try:
        await update.message.reply_text(
            f"*Last On Chain Message*\n\n{time} UTC\n"
            f"{days} days, {hours} hours, and {minutes} minutes ago\n\n"
            f"`{message}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="View on chain",
                            url=f'{urls.ETHER_TX}{recent_tx["hash"]}',
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="View all on chains", url=f"{urls.WEBSITE}docs/onchains"
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
                f"*Last On Chain Message*\n\n{time} UTC\n"
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
                                url=f'{urls.ETHER_TX}{recent_tx["hash"]}',
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="View all on chains", url=f"{urls.WEBSITE}docs/onchains"
                            )
                        ],
                    ]
                ),
            )


async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("Getting Pair Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    url = "https://lb.drpc.org/ogrpc?network="
    networks = {
        "ETH": f"{url}ethereum&dkey={os.getenv('DRPC_API_KEY')}",
        "ARB": f"{url}arbitrum&dkey={os.getenv('DRPC_API_KEY')}",
        "BSC": "https://bsc-dataseed.binance.org/",
        "POLY": f"{url}polygon&dkey={os.getenv('DRPC_API_KEY')}",
        "OPTI": f"{url}optimism&dkey={os.getenv('DRPC_API_KEY')}",
        "BASE": "https://mainnet.base.org"
    }

    contract_instances = {}
    for network, web3_url in networks.items():
        web3 = Web3(Web3.HTTPProvider(web3_url))
        contract = web3.eth.contract(
            address=to_checksum_address(ca.FACTORY),
            abi=api.get_abi(ca.FACTORY, network.lower()),
        )
        amount = contract.functions.allPairsLength().call()
        contract_instances[network] = amount
    await message.delete()
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
    pioneer_id = " ".join(context.args)
    data = opensea.get_nft_collection("/x7-pioneer")
    floor_data = api.get_nft_data(ca.PIONEER, "eth")
    floor = floor_data["floor_price"]
    native_price = api.get_native_price("eth")
    if floor != "N/A":
        floor_round = round(floor, 2)
        floor_dollar = floor * float(native_price)
    else:
        floor_round = "N/A"
        floor_dollar = 0 
    pioneer_pool = api.get_native_balance(ca.PIONEER, "eth")
    each = float(pioneer_pool) / 639
    each_dollar = float(each) * float(native_price)
    total_dollar = float(pioneer_pool) * float(native_price)
    if pioneer_id == "":
    
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
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
                            url=f"{urls.OS_PIONEER}",
                        )
                    ],
                ]
            ),
        )
    else:
        data = opensea.get_nft_id(ca.PIONEER, pioneer_id)
        if "nft" in data and data["nft"]:
            status = data["nft"]["traits"][0]["value"]
            image_url = data["nft"]["image_url"]
        else:
            await update.message.reply_text(f"Pioneer {pioneer_id} not found")
            return
        
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


async def pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = " ".join(context.args).lower()
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    message = await update.message.reply_text("Getting Lending Pool Info, Please wait...")
    if chain == "":
        eth_price = api.get_native_price("eth")
        eth_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "eth")
        eth_lpool_reserve_dollar = (float(eth_lpool_reserve) * float(eth_price))
        eth_lpool = api.get_native_balance(ca.LPOOL, "eth")
        eth_lpool_dollar = (float(eth_lpool) * float(eth_price))
        eth_pool = round(float(eth_lpool_reserve) + float(eth_lpool), 2)
        eth_dollar = eth_lpool_reserve_dollar + eth_lpool_dollar

        bnb_price = api.get_native_price("bnb")
        bsc_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "bsc")
        bsc_lpool_reserve_dollar = (float(bsc_lpool_reserve) * float(bnb_price))
        bsc_lpool = api.get_native_balance(ca.LPOOL_V1, "bsc")
        bsc_lpool_dollar = (float(bsc_lpool) * float(bnb_price))
        bsc_pool = round(float(bsc_lpool_reserve) + float(bsc_lpool), 2)
        bsc_dollar = bsc_lpool_reserve_dollar + bsc_lpool_dollar

        poly_price = api.get_native_price("matic")
        poly_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "poly")
        poly_lpool_reserve_dollar = (float(poly_lpool_reserve) * float(poly_price))
        poly_lpool = api.get_native_balance(ca.LPOOL_V1, "poly")
        poly_lpool_dollar = (float(poly_lpool) * float(poly_price))
        poly_pool = round(float(poly_lpool_reserve) + float(poly_lpool), 2)
        poly_dollar = poly_lpool_reserve_dollar + poly_lpool_dollar

        arb_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "arb")
        arb_lpool_reserve_dollar = (float(arb_lpool_reserve) * float(eth_price))
        arb_lpool = api.get_native_balance(ca.LPOOL_V1, "arb")
        arb_lpool_dollar = (float(arb_lpool) * float(eth_price))
        arb_pool = round(float(arb_lpool_reserve) + float(arb_lpool), 2)
        arb_dollar = arb_lpool_reserve_dollar + arb_lpool_dollar

        opti_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "opti")
        opti_lpool_reserve_dollar = (float(opti_lpool_reserve) * float(eth_price))
        opti_lpool = api.get_native_balance(ca.LPOOL_V1, "opti")
        opti_lpool_dollar = (float(opti_lpool) * float(eth_price))
        opti_pool = round(float(opti_lpool_reserve) + float(opti_lpool), 2)
        opti_dollar = opti_lpool_reserve_dollar + opti_lpool_dollar

        base_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "base")
        base_lpool_reserve_dollar = (float(base_lpool_reserve) * float(eth_price))
        base_lpool = api.get_native_balance(ca.LPOOL_V1, "base")
        base_lpool_dollar = (float(base_lpool) * float(eth_price))
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

        await message.delete()
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
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
        if chain == "eth":
            pool_address = ca.LPOOL
        else:
            pool_address = ca.LPOOL_V1
        address = to_checksum_address(pool_address)
        contract = web3_url.eth.contract(address=address, abi=api.get_abi(pool_address, chain))
        available = (contract.functions.availableCapital().call() / 10**18)
        native_price = api.get_native_price(chain_native)
        lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, chain)
        lpool_reserve_dollar = (float(lpool_reserve) * float(native_price))
        lpool = float(api.get_native_balance(pool_address, chain))
        lpool_dollar = (float(lpool) * float(native_price))
        pool = round(float(lpool_reserve) + float(lpool), 2)
        dollar = lpool_reserve_dollar + lpool_dollar
        lpool_reserve = round(float(lpool_reserve), 2)
        lpool = round(float(lpool), 2)
        used = lpool - available
        percent = int((used / pool) * 100)
        
        await message.delete()
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
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
                            url=f"{chain_url}{pool_address}",
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
    try:
        if context.args:
            search = context.args[0].lower()
            chain = context.args[1].lower() if len(context.args) > 1 else "eth"
        else:
            search = ""
            chain = ""
        token_info = db.token_get(search, chain)
        for token_instance in token_info:
            message = await update.message.reply_text("Getting Xchange Pair Price Info, Please wait...")
            await context.bot.send_chat_action(update.effective_chat.id, "typing")
            info = dextools.get_token_data(token_instance['ca'], token_instance['chain'].lower())
            holders = info["holders"]
            dext = mappings.CHAINS[token_instance['chain'].lower()].dext
            w3 = mappings.CHAINS[token_instance['chain'].lower()].w3
            token = mappings.CHAINS[token_instance['chain'].lower()].token
            contract = w3.eth.contract(
                address=Web3.to_checksum_address(token_instance['pair']), abi=ca.PAIRS_ABI)
            token0_address = contract.functions.token0().call()
            token1_address = contract.functions.token1().call()
            is_reserve_token0 = token_instance['ca'].lower() == token0_address.lower()
            is_reserve_token1 = token_instance['ca'].lower() == token1_address.lower()
            eth = ""
            if is_reserve_token0:
                eth = contract.functions.getReserves().call()[1]
            elif is_reserve_token1:
                eth = contract.functions.getReserves().call()[0]
            decimals = contract.functions.decimals().call()
            eth_in_wei = int(eth)
            liq = api.get_native_price(token) * eth_in_wei * 2
            formatted_liq = "${:,.2f}".format(liq / (10**decimals))
            info = dextools.get_token_info(token_instance['ca'], token_instance['chain'].lower())
            holders = info["holders"]
            mcap = info["mcap"]
            price, price_change_raw = dextools.get_price(token_instance['ca'], token_instance['chain'].lower())
            price_change = (f"{price_change_raw['one_hour']}\n"
                        f"{price_change_raw['six_hour']}\n"
                        f"{price_change_raw['one_day']}")
            volume = dextools.get_volume(token_instance['pair'], token_instance['chain'].lower())
            im1 = Image.open((random.choice(media.BLACKHOLE)))
            try:
                image = token_instance['image_url']
                img = Image.open(requests.get(image, stream=True).raw)
                img = img.resize((200, 200), Image.ANTIALIAS)
                result = img.convert("RGBA")
                result.save(r"media/tokenlogo.png")
                im2 = Image.open(r"media/tokenlogo.png")
            except Exception:
                if token_instance['chain'].lower() == "eth":
                    im2 = Image.open(media.ETH_LOGO)
                if token_instance['chain'].lower() == "bsc":
                    im2 = Image.open(media.BSC_LOGO)
                if token_instance['chain'].lower() == "poly":
                    im2 = Image.open(media.POLY_LOGO)
                if token_instance['chain'].lower() == "arb":
                    im2 = Image.open(media.ARB_LOGO)
                if token_instance['chain'].lower() == "opti":
                    im2 = Image.open(media.OPTI_LOGO)

            im1.paste(im2, (720, 20), im2)
            i1 = ImageDraw.Draw(im1)
            i1.text(
                (0, 0),
                    f"  Xchange Pair Info\n\n💰 {search.upper()}\n\n"
                    f"💰 Chain: {token_instance['chain'].upper()}\n"
                    f"💰 Price: {price}\n"
                    f"💎 Market Cap: {mcap}\n"
                    f"📊 24 Hour Volume: {volume}\n"
                    f"💦 Liquidity: {formatted_liq}\n"
                    f"👪 Holders: {holders}\n\n"
                    f"{price_change}\n\n\n"
                    f'  UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
                font = ImageFont.truetype(media.FONT, 24),
                fill=(255, 255, 255),
            )
            img_path = os.path.join("media", "blackhole.png")
            im1.save(img_path)
            await message.delete()
            await update.message.reply_photo(
                photo=open(r"media/blackhole.png", "rb"),
                caption=
                    f"*Xchange Pair Info\n\n{search.upper()}*\n"
                    f"`{token_instance['ca']}`\n\n"
                    f"⛓️ Chain: {token_instance['chain'].upper()}\n"
                    f"💰 Price: {price}\n"
                    f"💎 Market Cap: {mcap}\n"
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
                                url=f"{urls.XCHANGE}/#/swap?outputCurrency={token_instance['ca']}",
                            )
                        ],
                    ]
                ),
            )
            return
        else:
            if search == "":
                price = coingecko.get_price("x7r, x7dao")
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

                await update.message.reply_photo(
                    photo=api.get_random_pioneer(),
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
                                    url=f"{urls.DEX_TOOLS_ETH}{ca.X7R_PAIR_ETH}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="X7DAO Chart - Governance Token",
                                    url=f"{urls.DEX_TOOLS_ETH}{ca.X7DAO_PAIR_ETH}",
                                )
                            ],
                        ]
                    ),
                )
                return
            else:
                token = coingecko.search(search)
                if token['coins'] == []:
                    await update.message.reply_text(
                        f"{search.upper()} Not found",
                        parse_mode="Markdown")
                    return
                id = token["coins"][0]["id"]
                symbol = token["coins"][0]["symbol"]
                thumb = token["coins"][0]["large"]
                token_price = coingecko.get_price(id)
                if "e-" in str(token_price[id]["usd"]):
                    price = "{:.8f}".format(token_price[id]["usd"])
                elif token_price[id]["usd"] < 1:
                    price = "{:.8f}".format(token_price[id]["usd"]) 
                else:
                    price = "{:.2f}".format(token_price[id]["usd"])
                    
                price_change = token_price[id]["usd_24h_change"]
                if price_change is None:
                    price_change = 0
                else:
                    price_change = round(token_price[id]["usd_24h_change"], 2)
                market_cap = token_price[id]["usd_market_cap"]
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
                        f"{id.capitalize()} ({symbol}) price\n\n"
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
                        f"*{id.capitalize()} ({symbol}) price*\n\n"
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
                                    url=f"https://www.coingecko.com/en/coins/{id}",
                                )
                            ],
                        ]
                    ),
                )
    except IndexError:
        await message.delete()
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
            InlineKeyboardButton(text="ETH", url=f"{urls.ETHER_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="BSC", url=f"{urls.BSC_ADDRESS}{ca.ROUTER}"),
        ],
        [
            InlineKeyboardButton(text="Polygon", url=f"{urls.POLY_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="Arbitrum", url=f"{urls.ARB_ADDRESS}{ca.ROUTER}"),
        ],
        [
            InlineKeyboardButton(text="Optimism", url=f"{urls.OPTI_ADDRESS}{ca.ROUTER}"),
            InlineKeyboardButton(text="Base", url=f"{urls.BASE_ADDRESS}{ca.ROUTER}"),
        ],
    ]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=f"\n",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide some words to convert to speech.")
        return
    voice_note = gTTS(" ".join(context.args), lang='en', slow=False)
    voice_note.save("media/voicenote.mp3")
    await context.bot.delete_message(update.effective_chat.id, update.message.id)
    await update.message.reply_audio(audio=open("media/voicenote.mp3", "rb"))


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            f"Please provide contract address and optional chain")
        return
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    if len(context.args) == 1:
        search = context.args[0].lower()
        chain = None

    if len(context.args) == 2:
        search = context.args[0].lower()
        chain = context.args[1].lower()
        
    if search == "":
        await update.message.reply_text(
        f"Please provide Contract Address and optional chain")
        return
    
    if chain is not None and chain not in mappings.CHAINS:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    
    message = await update.message.reply_text("Scanning, Please wait...")
    if chain == None:
        for chain in mappings.CHAINS:
            scan = api.get_scan(search, chain)
            if scan:
                break
        else:
            await update.message.reply_text(f"{search} not found")
            return
    
    else:
        if chain in mappings.CHAINS:
            scan = api.get_scan(search, chain)
        if scan == {}:
            await update.message.reply_text(f"{search} ({chain.upper()}) not found")
            return
    scan_link = mappings.CHAINS[chain].scan_address
    dext = mappings.CHAINS[chain].dext

    if api.get_verified(search, chain):
        verified = "✅ Contract Verified"
    else:
        verified = "⚠️ Contract Unverified"

    token_address = str(search.lower())
    if token_address in scan:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        token_name = scan[token_address]["token_name"]
        token_symbol = scan[token_address]["token_symbol"]
        if scan[token_address]["is_in_dex"] == "1":
            buy_tax_raw = (float(scan[token_address]["buy_tax"]) * 100)
            sell_tax_raw = (float(scan[token_address]["sell_tax"]) * 100)
            buy_tax = int(buy_tax_raw)
            sell_tax = int(sell_tax_raw)
            if sell_tax > 10 or buy_tax > 10:
                tax = f"⚠️ Tax: {buy_tax}/{sell_tax}"
            else:
                tax = f"✅️ Tax: {buy_tax}/{sell_tax}"
        else:
            tax = f"❓ Tax - Unknown"

        if "holders" in scan[token_address]:
            top_holders = scan[token_address].get("holders", [])
            for holder in top_holders:
                if holder.get("is_contract", 0) == 0:
                    top_holder = holder.get("percent")
                    break
                else:
                    top_percent = "❓ Top Holder Unknown"

            top_holder_str = float(top_holder)
            formatted_top_percent = "{:.1f}".format(float(top_holder_str) * 100)
            if top_holder_str >= 0.05:
                top_percent = f'⚠️ Top Holder Holds {formatted_top_percent}% of Supply'
            else:
                top_percent = f'✅️ Top Holder Holds {formatted_top_percent}% of Supply'
        else:
            top_percent = "❓ Top Holder Unknown"

        if "owner_address" in scan[token_address]:
            if scan[token_address]["owner_address"] == "0x0000000000000000000000000000000000000000":
                renounced = "✅ Contract Renounced"
            else:
                renounced = "⚠️ Contract Not Renounced"

        if "is_mintable" in scan[token_address]:
            if scan[token_address]["is_mintable"] == "1":
                mint = "⚠️ Mintable"
            else:
                mint = "✅️ Not Mintable"
        else:
            mint = "❓ Mintable - Unknown"

        if "is_honeypot" in scan[token_address]:
            if scan[token_address]["is_honeypot"] == "1":
                honey_pot = "❌ Honey Pot"
            else:
                honey_pot = "✅️ Not Honey Pot"
        else:
            honey_pot = "❓ Honey Pot - Unknown"

        if "is_blacklisted" in scan[token_address]:
            if scan[token_address]["is_blacklisted"] == "1":
                blacklist = "⚠️ Has Blacklist Functions"
            else:
                blacklist = "✅️ No Blacklist Functions"
        else:
            blacklist = "❓ Blacklist Functions - Unknown"

        if "cannot_sell_all" in scan[token_address]:
            if scan[token_address]["cannot_sell_all"] == "1":
                sellable = "❌ Not Sellable"
            else:
                sellable = "✅️ Sellable"
        else:
            sellable = "❓ Sellable - Unknown"

        if "owner_percent" in scan[token_address]:
            if renounced == "✅ Contract Renounced":
                owner_percent = f'✅️ Owner Holds 0.0% of Supply'
            else:
                owner_percent_str = float(scan[token_address]["owner_percent"])
                formatted_owner_percent = "{:.1f}".format(owner_percent_str * 100)
                if owner_percent_str >= 0.05:
                    owner_percent = f'⚠️ Owner Holds {formatted_owner_percent}% of Supply'
                else:
                    owner_percent = f'✅️ Owner Holds {formatted_owner_percent}% of Supply'
        else:
            owner_percent = "❓ Tokens Held By Owner Unknown"

        if "lp_holders" in scan[token_address]:
            locked_lp_list = [lp for lp in scan[token_address]["lp_holders"]if lp["is_locked"] == 1]
            if locked_lp_list:
                if locked_lp_list[0]["address"] == "0x000000000000000000000000000000000000dead":
                    lock_word = "🔥 Liquidity Burnt"
                else:
                    lock_word = "✅️ Liquidity Locked"
                lp_with_locked_detail = [lp for lp in locked_lp_list if "locked_detail" in lp]
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
                lock = "❓ Liquidity Lock Unknown"
        else:
            lock = "❓ Liquidity Lock Unknown"

        if "dex" in scan[token_address] and scan[token_address]["dex"]:
            pair = scan[token_address]["dex"][0]["pair"]
        else:
            pair = defined.get_pair(token_address, chain)

    else:
        renounced = "❓ Renounced - Unknown"
        tax = "❓ Tax - Unknown"
        mint = "❓ Mintable - Unknown"
        honey_pot = "❓ Honey Pot - Unknown"
        blacklist = "❓ Blacklist Functions - Unknown"
        sellable = "❓ Sellable - Unknown"
        owner_percent = "❓ Tokens Held By Owner Unknown"
        top_holder = "❓ Top Holder Unknown"
        lock  = "❓ Liquidity Lock Unknown"

    status = f"{verified}\n{renounced}\n{tax}\n{sellable}\n{mint}\n{honey_pot}\n{blacklist}\n{owner_percent}\n{top_percent}\n{lock}"

    await message.delete()
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Token Scanner*\n\n{token_name} ({token_symbol}) - {chain.upper()}\n`{token_address}`\n\n{status}\n\n"
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
                        url=f'https://www.dextools.io/app/{dext}/pair-explorer/{pair}',
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
                url=f"{urls.CA_DIRECTORY}",
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


async def splitters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    if len(context.args) > 1:
        eth_value = context.args[0]
        if eth_value.isdigit():
            eth_value = float(context.args[0])
        else:
            await update.message.reply_text(
                "Please Use `/splitter [amount] [chain-name]`",
            parse_mode = "markdown")
            return
        chain = context.args[1].lower()
        if chain in mappings.CHAINS:
            chain_name = mappings.CHAINS[chain].name
            chain_url = mappings.CHAINS[chain].scan_address
            chain_native = mappings.CHAINS[chain].token
        else:
            await update.message.reply_text(text.CHAIN_ERROR)
            return
        distribution = splitters.GENERATE_INFO(chain, eth_value)
        splitter_text = f"*X7 Finance Ecosystem Splitters {chain_name}* \n\n{eth_value} {chain_native.upper()}\n\n"
        for location, share in distribution.items():
            if location == "Treasury":
                splitter_text += f"\n{location}: {share:.2f} {chain_native.upper()}:\n"
            else:
                splitter_text += f"{location}: {share:.2f} {chain_native.upper()}\n"

        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"{splitter_text}\n"
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
    else:
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
                f"*X7 Finance Ecosystem Splitters {chain_name}*\n"
                f"For example of splitter allocation use\n`/splitter [amount] [chain-name]`\n\n"
                f"Ecosystem Splitter: {eco_eth} {chain_native.upper()} (${'{:0,.0f}'.format(eco_dollar)})\n"
                f"Profit Share Splitter: {profit_eth} {chain_native.upper()} (${'{:0,.0f}'.format(profit_dollar)})\n"
                f"Treasury Splitter: {treasury_eth} {chain_native.upper()} (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
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
    message = await update.message.reply_text("Getting Supply Info, Please wait...")
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
    prices = coingecko.get_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
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
    await message.delete()
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
                [InlineKeyboardButton(text="Xchange", url=f"{urls.XCHANGE}")],
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
    caption = f"{caption}\n\n{api.get_quote()}"
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
        ("Europe/London", "GMT"),
        ("Europe/Berlin", "CET"),
        ("Asia/Dubai", "GST"),
        ("Asia/Kolkata", "IST"),
        ("Asia/Tokyo", "JST"),
        ("Australia/Queensland", "AEST"),
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
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    message = await update.message.reply_text("Getting Treasury Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    native_price = api.get_native_price(chain_native)
    com_eth_raw = api.get_native_balance(chain_com_multi, chain)
    com_eth = round(float(com_eth_raw), 2)
    com_dollar = float(com_eth) * float(native_price)
    com_usdt_balance = api.get_stables_balance(chain_com_multi, ca.USDT, chain)
    com_usdc_balance = api.get_stables_balance(chain_com_multi, ca.USDC, chain)
    stables = com_usdt_balance + com_usdc_balance
    com_x7r_balance = api.get_token_balance(chain_com_multi, ca.X7R, chain)
    x7r_price,_ = dextools.get_price(ca.X7R, chain)
    com_x7r_price = float(com_x7r_balance) * float(x7r_price)
    com_x7dao_balance = api.get_token_balance(chain_com_multi, ca.X7DAO, chain)
    x7dao_price,_ = dextools.get_price(ca.X7DAO, chain)
    com_x7dao_price = float(com_x7dao_balance) * float(x7dao_price)
    com_x7d_balance = api.get_token_balance(chain_com_multi, ca.X7D, chain)
    com_x7d_price = com_x7d_balance * native_price
    com_total = com_x7r_price + com_dollar + com_x7d_price + com_x7dao_price + stables
    
    await message.delete()
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance Treasury {chain_name}*\nUse `/treasury [chain-name]` for other chains\n\n"
            f'Community Wallet:\n{com_eth} {chain_native.upper()} (${"{:0,.0f}".format(com_dollar)})\n'
            f'{com_x7d_balance} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
            f'{"{:0,.0f}".format(com_x7r_balance)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
            f'{"{:0,.0f}".format(com_x7dao_balance)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
            f"${'{:0,.0f}'.format(stables)} USDT/C\n\n"
            f'Total: (${"{:0,.0f}".format(com_total)})\n\n'
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


async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if dune.TRENDING_FLAG == False:
            message = await update.message.reply_text("Getting Xchange Trending, Please wait...")
            await context.bot.send_chat_action(update.effective_chat.id, "typing")
            execution_id = dune.execute_query("2970801", "medium")
            t.sleep(10)

            response = dune.get_query_results(execution_id)
            response_data = response.json()

            rows = response_data["result"]["rows"]
            rows = [row for row in rows if row["pair"] != "TOTAL"]
            sorted_rows = sorted(rows, key=lambda x: x['last_24hr_amt'], reverse=True)
            top_3_last_24hr_amt = sorted_rows[:3]
            trending_text = "*Xchange Trending Pairs*\n\n"

            for idx, item in enumerate(top_3_last_24hr_amt, start=1):
                trending_text += f'{idx}. {item["pair"]}\n24 Hour Volume: ${"{:0,.0f}".format(item["last_24hr_amt"])}\n\n'

            await update.message.reply_photo(
                photo=api.get_random_pioneer(),
                caption=f'{trending_text}{api.get_quote()}',
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="X7 Dune Dashboard", url=f"{urls.DUNE}"
                            )
                        ],
                    ]
                ),
                )
            dune.TRENDING_TIMESTAMP = datetime.utcnow().timestamp()
            dune.TRENDING_FLAG = True
            dune.TRENDING_TEXT = trending_text

        else:
            await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f'{dune.TRENDING_TEXT}Last Updated: {dune.TRENDING_LAST_DATE}\n\n'
                f'{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Dune Dashboard", url=f"{urls.DUNE}"
                        )
                    ],
                ]
            ),
            )
    except Exception:
        await message.delete()
        await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f'*Xchange Trending*\n\n'
            f'Unable to refresh Dune data, please use the link below\n\n'
            f'{api.get_quote()}',
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="X7 Dune Dashboard", url=f"{urls.DUNE}"
                    )
                ],
            ]
        ),
        )


async def twitter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
    await update.message.reply_text(
        f"*X7 Finance Twitter/X*\n\n" f"{random.choice(text.X_REPLIES)}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"{urls.TWITTER}",
                        url=f"{urls.TWITTER}",
                    )
                ],
            ]
        ),
    )

async def v1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    native_price = api.get_native_price("eth")
    v1_1_eth_raw = api.get_native_balance(ca.V1_1, "eth")
    v1_1_eth = round(float(v1_1_eth_raw), 2)
    v1_1_dollar = float(v1_1_eth) * float(native_price)

    v1_2_eth_raw = api.get_native_balance(ca.V1_2, "eth")
    v1_2_eth = round(float(v1_2_eth_raw), 2)
    v1_2_dollar = float(v1_2_eth) * float(native_price)

    total_eth  = v1_1_eth + v1_2_eth
    total_dollar = v1_1_dollar + v1_2_dollar 
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"*X7 Finance V1 Wallets*\n\n"
            f'Wallet 1: {v1_1_eth} ETH (${"{:0,.0f}".format(v1_1_dollar)})\n'
            f'Wallet 2: {v1_2_eth} ETH (${"{:0,.0f}".format(v1_2_dollar)})\n\n'
            f'Total: {total_eth} ETH (${"{:0,.0f}".format(total_dollar)})\n\n'
            f"{api.get_quote()}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Wallet 1",
                        url=f"{urls.ETHER_ADDRESS}{ca.V1_1}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Wallet 2",
                        url=f"{urls.ETHER_ADDRESS}{ca.V1_2}",
                    )
                ],
            ]
        ),
    )


async def volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("Getting Volume Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        if dune.VOLUME_FLAG == False:
            execution_id = dune.execute_query("2972368", "medium")
            t.sleep(5)
            response = dune.get_query_results(execution_id)
            response_data = response.json()

            last_24hr_amt = response_data['result']['rows'][0]['last_24hr_amt']
            last_30d_amt = response_data['result']['rows'][0]['last_30d_amt']
            last_7d_amt = response_data['result']['rows'][0]['last_7d_amt']
            lifetime_amt = response_data['result']['rows'][0]['lifetime_amt']

            volume_text = (
                f'Total:       ${"{:0,.0f}".format(lifetime_amt)}\n'
                f'30 Day:    ${"{:0,.0f}".format(last_30d_amt)}\n'
                f'7 Day:      ${"{:0,.0f}".format(last_7d_amt)}\n'
                f'24 Hour:  ${"{:0,.0f}".format(last_24hr_amt)}'
                )
            await message.delete()
            await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"*Xchange Trading Volume*\n\n{volume_text}\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Dune Dashboard", url=f"{urls.DUNE}"
                        )
                    ],
                ]
            ),
            )
            dune.VOLUME_TIMESTAMP = datetime.utcnow().timestamp()
            dune.VOLUME_FLAG = True
            dune.VOLUME_TEXT = volume_text
        else:
            await message.delete()
            await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f'*Xchange Trading Volume*\n\n'
                f'{dune.VOLUME_TEXT}\n\nLast Updated: {dune.VOLUME_LAST_DATE}\n\n'
                f'{api.get_quote()}',
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="X7 Dune Dashboard", url=f"{urls.DUNE}"
                        )
                    ],
                ]
            ),
            )
    except Exception:
        await message.delete()
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
                        text="X7 Dune Dashboard", url=f"{urls.DUNE}"
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
    if not re.match(r'^0x[a-fA-F0-9]{40}$', wallet):
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
    else:
        await update.message.reply_text(text.CHAIN_ERROR)
        return
    message = await update.message.reply_text("Getting Wallet Info, Please wait...")
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    native_price = api.get_native_price(chain_native)
    eth = api.get_native_balance(wallet, chain)
    dollar = float(eth) * float(native_price)
    x7r,_ = dextools.get_price(ca.X7R, chain)
    x7dao,_ = dextools.get_price(ca.X7DAO, chain)
    x7101,_ = dextools.get_price(ca.X7101, chain)
    x7102,_ = dextools.get_price(ca.X7102, chain)
    x7103,_ = dextools.get_price(ca.X7103, chain)
    x7104,_ = dextools.get_price(ca.X7104, chain)
    x7105,_ = dextools.get_price(ca.X7105, chain)

    x7r_balance = api.get_token_balance(wallet, ca.X7R, chain)
    x7r_price = float(x7r_balance) * float(x7r)
    
    x7dao_balance = api.get_token_balance(wallet, ca.X7DAO, chain)
    x7dao_price = float(x7dao_balance) * float(x7dao)
    
    x7101_balance = api.get_token_balance(wallet, ca.X7101, chain)
    x7101_price = float(x7101_balance) * float(x7101)
    
    x7102_balance = api.get_token_balance(wallet, ca.X7102, chain)
    x7102_price = float(x7102_balance) * float(x7102)
    
    x7103_balance = api.get_token_balance(wallet, ca.X7103, chain)
    x7103_price = float(x7103_balance) * float(x7103)

    x7104_balance = api.get_token_balance(wallet, ca.X7104, chain)
    x7104_price = float(x7104_balance) * float(x7104)

    x7105_balance = api.get_token_balance(wallet, ca.X7105, chain)
    x7105_price = float(x7105_balance) * float(x7105)
    
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
    txs = api.get_daily_tx_count(wallet, chain)
    
    await message.delete()
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
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
            f"{x7d_balance} X7D (${'{:0,.0f}'.format(x7d_price)})\n\n"
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
                [InlineKeyboardButton(text="Xchange", url=f"{urls.XCHANGE}")],
                [
                    InlineKeyboardButton(
                        text="X7.Finance",
                        url=f"{urls.WEBSITE_DEV}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="X7Finance.org",
                        url=f"{urls.WEBSITE}",
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
                [InlineKeyboardButton(text="Website", url=f"{urls.WEBSITE}")],
                [InlineKeyboardButton(text="Full WP", url=f"{urls.WP_LINK}")],
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
        lpool_reserve_dollar = (float(lpool_reserve) * float(native_price))
        lpool = api.get_native_balance(ca.LPOOL, chain)
        lpool_dollar = (float(lpool) * float(native_price))
        dollar = lpool_reserve_dollar + lpool_dollar
        supply = round(float(lpool_reserve) + float(lpool), 2)
        lpool_rounded = round(float(lpool), 2)
        lpool_reserve_rounded = round(float(lpool_reserve), 2)
        info = dextools.get_token_info(ca.X7D, "eth")
        holders = info["holders"]

    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
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
                        url=f"{urls.XCHANGE_FUND}",
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
        info = dextools.get_token_info(ca.X7DAO, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7DAO, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7dao")[1]}'
            ath_value = coingecko.get_ath("x7dao")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7DAO Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7R, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7R, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7r")[1]}'
            ath_value = coingecko.get_ath("x7r")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * api.get_x7r_supply(chain))}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
    
    await update.message.reply_photo(
        photo=api.get_random_pioneer(),
        caption=
            f"X7R Info {chain_name}\n\n"
            f"💰 Price: {price}\n"
            f'💎 Market Cap:  {market_cap}\n'
            f"📊 24 Hour Volume: {volume}\n"
            f"💦 Liquidity: {liquidity}\n"
            f"👪 Holders: {holders}\n"
            f"🔝 ATH: {ath}\n"
            f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7101, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7101, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7101")[1]}'
            ath_value = coingecko.get_ath("x7101")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7101 Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7102, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7102, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7102")[1]}'
            ath_value = coingecko.get_ath("x7102")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7102 Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7103, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7103, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7103")[1]}'
            ath_value = coingecko.get_ath("x7103")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7103 Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7104, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7104, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7104")[1]}'
            ath_value = coingecko.get_ath("x7104")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7104 Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
        info = dextools.get_token_info(ca.X7105, chain)
        holders = info["holders"]
        market_cap = info["mcap"]
        price, price_change_raw = dextools.get_price(ca.X7105, chain)
        price_change = (f"{price_change_raw['one_hour']}\n"
                    f"{price_change_raw['six_hour']}\n"
                    f"{price_change_raw['one_day']}")
        volume = dextools.get_volume(chain_pair, chain)
        liquidity = dextools.get_liquidity(chain_pair, chain)
        if chain == "eth":
            ath_change = f'{coingecko.get_ath("x7105")[1]}'
            ath_value = coingecko.get_ath("x7105")[0]
            ath = f'${ath_value} (${"{:0,.0f}".format(ath_value * ca.SUPPLY)}) {ath_change[:3]}%'
        else:
            ath = "Unavailable"        
        
        await update.message.reply_photo(
            photo=api.get_random_pioneer(),
            caption=
                f"X7105 Info {chain_name}\n\n"
                f"💰 Price: {price}\n"
                f'💎 Market Cap:  {market_cap}\n'
                f"📊 24 Hour Volume: {volume}\n"
                f"💦 Liquidity: {liquidity}\n"
                f"👪 Holders: {holders}\n"
                f"🔝 ATH: {ath}\n\n"
                f"{price_change}\n\n"
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
