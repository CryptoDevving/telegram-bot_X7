import os
import sys
import time
import random
import asyncio
from datetime import datetime

import sentry_sdk
from web3 import Web3
from telegram import *
from telegram.ext import *
from eth_utils import to_checksum_address
from PIL import Image, ImageDraw, ImageFont

from constants import ca, url
from hooks import api, db
import media


alchemy_opti = os.getenv("ALCHEMY_OPTI")
alchemy_opti_url = f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_opti}"
web3 = Web3(Web3.HTTPProvider(alchemy_opti_url))

factory = web3.eth.contract(address=ca.FACTORY, abi=api.get_abi(ca.FACTORY, "opti"))
ill001 = web3.eth.contract(address=ca.ILL001, abi=api.get_abi(ca.ILL001, "opti"))
ill002 = web3.eth.contract(address=ca.ILL002, abi=api.get_abi(ca.ILL002, "opti"))
ill003 = web3.eth.contract(address=ca.ILL003, abi=api.get_abi(ca.ILL003, "opti"))

pair_filter = factory.events.PairCreated.create_filter(fromBlock="latest")
ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock="latest")
ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock="latest")
ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock="latest")

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)


class FilterNotFoundError(Exception):
    def __init__(self, message="filter not found"):
        self.message = message
        super().__init__(self.message)


async def restart_script():
    python = sys.executable
    script = os.path.abspath(__file__)
    os.execl(python, python, script)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("opti pong")


async def new_pair(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "opti")
    if event["args"]["token0"] == ca.OWETH:
        native = api.get_token_name(event["args"]["token0"], "opti")
        token_name = api.get_token_name(event["args"]["token1"], "opti")
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] == ca.OWETH:
        native = api.get_token_name(event["args"]["token1"], "opti")
        token_name = api.get_token_name(event["args"]["token0"], "opti")
        token_address = event["args"]["token0"]
    elif event["args"]["token0"] in ca.STABLES:
        native = api.get_token_name(event["args"]["token0"], "opti")
        token_name = api.get_token_name(event["args"]["token1"], "opti")
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] in ca.STABLES:
        native = api.get_token_name(event["args"]["token1"], "opti")
        token_name = api.get_token_name(event["args"]["token0"], "opti")
        token_address = event["args"]["token0"]
    else:
        native = api.get_token_name(event["args"]["token1"], "opti")
        token_name = api.get_token_name(event["args"]["token0"], "opti")
        token_address = event["args"]["token0"]
    info = api.get_token_data(token_address, "opti")
    if api.get_verified(token_address, "opti"):
        verified = "✅ Contract Verified"
    else:
        "⚠️ Contract Unverified"
    if (
        info[0]["decimals"] == ""
        or info[0]["decimals"] == "0"
        or not info[0]["decimals"]
    ):
        supply = int(api.get_supply(token_address, "opti"))
    else:
        supply = int(api.get_supply(token_address, "opti")) / 10 ** int(
            info[0]["decimals"]
        )
    status = ""
    renounced = ""
    tax = ""
    try:
        scan = api.get_scan(token_address, "opti")
        if "owner_address" in scan[f"{str(token_address).lower()}"]:
            if scan[f"{str(token_address).lower()}"]["owner_address"] == "0x0000000000000000000000000000000000000000":
                renounced = "✅ Contract Renounced"
            else:
                renounced = "⚠️ Contract Not Renounced"
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
                tax = f"⚠️ Tax: Unavailable"
        else:
            tax = f"⚠️ Tax: Unavailable"
        status = f"{verified}\n{tax}\n{renounced}"
    except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        status = "⚠️ Scan Unavailable"
    pool = int(tx["result"]["value"], 0) / 10**18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Liquidity: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("eth"))
        pool_text = (
            f'{pool} ETH (${"{:0,.0f}".format(pool_dollar)})\n'
            f'Total Liquidity: ${"{:0,.0f}".format(pool_dollar * 2)}'
        )
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.OPTI_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
            f"New Pair Created (OPTIMISM)\n\n"
            f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
            f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
            f"{pool_text}\n\n"
            f"{status}\n",
        font = ImageFont.truetype(media.FONT, 26),
        fill = (255, 255, 255),
    )
    im1.save(r"media/blackhole.png")
    channel_chat_ids = [
        os.getenv("ALERTS_TELEGRAM_CHANNEL_ID"),
        os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
    ]
    for chat_id in channel_chat_ids:
        await application.bot.send_photo(
            chat_id,
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*New Pair Created (OPTIMISM)*\n\n"
                f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
                f"Token Address:\n`{token_address}`\n\n"
                f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
                f"{pool_text}\n\n"
                f"{status}\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"Buy On Xchange",
                            url=f"{url.XCHANGE_BUY_OPTI}{token_address}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart",
                            url=f"{url.DEX_TOOLS_OPTI}{event['args']['pair']}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Token Contract",
                            url=f"{url.OPTI_ADDRESS}{token_address}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Deployer TX",
                            url=f"{url.OPTI_TX}{event['transactionHash'].hex()}",
                        )
                    ],
                ]
            ),
        )
        try:
            if event["args"]["token0"] == ca.OWETH or event["args"]["token1"] == ca.OWETH:
                image_url = api.get_token_image(token_address, "opti")
                if image_url is None:
                    image_url = "N/A"

                db.token_add(token_name[1], event["args"]["pair"], token_address, "opti", image_url)

        except Exception as e:
            sentry_sdk.capture_exception(e)


async def new_loan(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "eth")
    try:
        address = to_checksum_address(ca.LPOOL)
        contract = web3.eth.contract(address=address, abi=api.get_abi(ca.LPOOL, "opti"))
        amount = (
            contract.functions.getRemainingLiability(
                int(event["args"]["loanID"])
            ).call()
            / 10**18
        )
        schedule1 = contract.functions.getPremiumPaymentSchedule(
            int(event["args"]["loanID"])
        ).call()
        schedule2 = contract.functions.getPrincipalPaymentSchedule(
            int(event["args"]["loanID"])
        ).call()

        schedule_str = api.format_schedule(schedule1, schedule2, "ETH")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        schedule_str = ""
        amount = ""
    cost = int(tx["result"]["value"], 0) / 10**18
    native_price = api.get_native_price("eth")
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.OPTI_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
            f"*New Loan Originated (OPTIMISM)*\n\n"
            f"Loan ID: {event['args']['loanID']}\n"
            f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} ETH "
            f'(${"{:0,.0f}".format(native_price * cost)})\n\n'
            f"Payment Schedule (UTC):\n{schedule_str}\n\n"
            f'Total: {amount} ETH (${"{:0,.0f}".format(native_price * amount)}',
        font = ImageFont.truetype(media.FONT, 26),
        fill = (255, 255, 255),
    )
    im1.save(r"media/blackhole.png")
    await application.bot.send_photo(
        os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*New Loan Originated (OPTIMISM)*\n\n"
            f"Loan ID: {event['args']['loanID']}\n"
            f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} ETH "
            f'(${"{:0,.0f}".format(api.native_price * cost)})\n\n'
            f"Payment Schedule (UTC):\n{schedule_str}\n\n"
            f'Total: {amount} ETH (${"{:0,.0f}".format(native_price * amount)})',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Loan TX",
                        url=f"{url.OPTI_TX}{event['transactionHash'].hex()}",
                    )
                ],
            ]
        ),
    )


async def log_loop(
    pair_filter, ill001_filter, ill002_filter, ill003_filter, poll_interval
):
    while True:
        try:
            for PairCreated in pair_filter.get_new_entries():
                await new_pair(PairCreated)

            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill001_filter.get_new_entries():
                await new_loan(LoanOriginated)

            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill002_filter.get_new_entries():
                await new_loan(LoanOriginated)

            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill003_filter.get_new_entries():
                await new_loan(LoanOriginated)

            await asyncio.sleep(poll_interval)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            await restart_script()


async def main():
    while True:
        try:
            tasks = [
                log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, 2)
            ]
            await asyncio.gather(*tasks)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            await restart_script()


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(os.getenv("TELEGRAM_BOT_TOKEN_OPTI"))
        .connection_pool_size(512)
        .build()
    )
    application.add_handler(CommandHandler("ping", ping))
    asyncio.run(main())
    application.run_polling(allowed_updates=Update.ALL_TYPES)
