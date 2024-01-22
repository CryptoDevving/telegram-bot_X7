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

from data import ca, url
from api import index as api
from media import index as media


web3_url = random.choice(url.bsc)
web3 = Web3(Web3.HTTPProvider(web3_url))

factory = web3.eth.contract(address=ca.factory, abi=api.get_abi(ca.factory, "bsc"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "bsc"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "bsc"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "bsc"))

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


async def new_pair(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "bsc")
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
    elif event["args"]["token0"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
    elif event["args"]["token0"] in ca.stables:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] in ca.stables:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
    else:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
    verified_check = api.get_verified(token_address, "bsc")
    info = api.get_token_data(token_address, "bsc")
    if (
        info[0]["decimals"] == ""
        or info[0]["decimals"] == "0"
        or not info[0]["decimals"]
    ):
        supply = int(api.get_supply(token_address, "bsc"))
    else:
        supply = int(api.get_supply(token_address, "bsc")) / 10 ** int(
            info[0]["decimals"]
        )
    status = ""
    renounced = ""
    tax = ""
    verified = ""
    if verified_check == "Yes":
        try:
            contract = web3.eth.contract(
                address=token_address, abi=api.get_abi(token_address, "bsc")
            )
            verified = "✅ Contract Verified"
        except Exception:
            verified = "⚠️ Contract Unverified"
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                renounced = "✅ Contract Renounced"
            else:
                renounced = "⚠️ Contract Not Renounced"
        except (Exception, TimeoutError, ValueError, StopAsyncIteration):
            renounced = "⚠️ Contract Not Renounced"
    else:
        verified = "⚠️ Contract Unverified"
    try:
        scan = api.get_scan(token_address, "bsc")
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
            except Exception as e:
                tax = f"⚠️ Tax: Unavailable"
        else:
            tax = f"⚠️ Tax: Unavailable"
        status = f"{verified}\n{tax}\n{renounced}"
    except Exception:
        status = "⚠️ Scan Unavailable"
    pool = int(tx["result"]["value"], 0) / 10**18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Liquidity: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1**18
        pool_text = (
            f'{pool} BNB (${"{:0,.0f}".format(pool_dollar)})\n'
            f'Total Liquidity: ${"{:0,.0f}".format(pool_dollar * 2)}'
        )
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f"New Pair Created (BSC)\n\n"
        f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
        f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
        f"{pool_text}\n\n"
        f"{status}\n",
        font=myfont,
        fill=(255, 255, 255),
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
            caption=f"*New Pair Created (BSC)*\n\n"
            f"{token_name[0]} ({token_name[1]}/{native[1]})\n\n"
            f"Token Address:\n`{token_address}`\n\n"
            f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
            f"{pool_text}\n\n"
            f"{status}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"Buy On Xchange", url=f"{url.xchange_buy_bsc}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart",
                            url=f"{url.dex_tools_bsc}{event['args']['pair']}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Token Contract",
                            url=f"{url.bsc_address}{token_address}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Deployer TX",
                            url=f"{url.bsc_tx}{event['transactionHash'].hex()}",
                        )
                    ],
                ]
            ),
        )


async def new_loan(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "arb")
    try:
        address = to_checksum_address(ca.lpool)
        contract = web3.eth.contract(address=address, abi=api.get_abi(ca.lpool, "bsc"))
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
        schedule_str = await api.format_schedule(schedule1, schedule2, "BNB")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        schedule_str = ""
        amount = ""
    cost = int(tx["result"]["value"], 0) / 10**18
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r"media/FreeMonoBold.ttf", 26)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
        f"New Loan Originated (BSC)\n\n"
        f"Loan ID: {event['args']['loanID']}\n"
        f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} BNB "
        f'(${"{:0,.0f}".format(api.get_native_price("bnb") * cost)})\n\n'
        f"Payment Schedule (UTC):\n{schedule_str}\n\n"
        f'Total: {amount} BNB (${"{:0,.0f}".format(api.get_native_price("bnb") * amount)})',
        font=myfont,
        fill=(255, 255, 255),
    )
    im1.save(r"media/blackhole.png")
    await application.bot.send_photo(
        os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        photo=open(r"media/blackhole.png", "rb"),
        caption=f"*New Loan Originated (BSC)*\n\n"
        f"Loan ID: {event['args']['loanID']}\n"
        f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} BNB "
        f'(${"{:0,.0f}".format(api.get_native_price("bnb") * cost)})\n\n'
        f"Payment Schedule (UTC):\n{schedule_str}\n\n"
        f'Total: {amount} BNB (${"{:0,.0f}".format(api.get_native_price("bnb") * amount)}',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Loan TX",
                        url=f"{url.bsc_tx}{event['transactionHash'].hex()}",
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
        .token(os.getenv("TELEGRAM_BOT_TOKEN_BSC"))
        .connection_pool_size(512)
        .build()
    )
    asyncio.run(main())
