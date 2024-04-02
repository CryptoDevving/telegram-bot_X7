from telegram import *
from telegram.ext import *

import asyncio, os, requests, random, sentry_sdk, sys

from web3 import Web3
from eth_utils import to_checksum_address
from PIL import Image, ImageDraw, ImageFont

from constants import ca, urls
from hooks import api, db
import media


sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)
defined = api.Defined()
dextools = api.Dextools()
chain = "bsc"
chain_native = "bnb"
bsc_url = f"https://lb.drpc.org/ogrpc?network=bsc&dkey={os.getenv('DRPC_API_KEY')}"
web3 = Web3(Web3.HTTPProvider(bsc_url))


factory = web3.eth.contract(address=ca.FACTORY, abi=api.get_abi(ca.FACTORY, chain))
ill001 = web3.eth.contract(address=ca.ILL001, abi=api.get_abi(ca.ILL001, chain))
ill003 = web3.eth.contract(address=ca.ILL003, abi=api.get_abi(ca.ILL003, chain))


pair_filter = factory.events.PairCreated.create_filter(fromBlock="latest")
ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock="latest")
ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock="latest")


class FilterNotFoundError(Exception):
    def __init__(self, message="filter not found"):
        self.message = message
        super().__init__(self.message)


async def restart_script():
    python = sys.executable
    script = os.path.abspath(__file__)
    os.execl(python, python, script)


async def new_pair(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), chain)
    if event["args"]["token0"] == ca.WBNB:
        native_token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] == ca.WBNB:
        native_token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_address = event["args"]["token0"]
    elif event["args"]["token0"] in ca.BSCETHPAIRS:
        native_token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] in ca.BSCETHPAIRS:
        native_token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_info = dextools.get_token_name(event["args"]["token0"], chain)
    elif event["args"]["token0"] in ca.STABLES:
        native_token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_address = event["args"]["token1"]
    elif event["args"]["token1"] in ca.STABLES:
        native_token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_address = event["args"]["token0"]
    else:
        native_token_info = dextools.get_token_name(event["args"]["token1"], chain)
        token_info = dextools.get_token_name(event["args"]["token0"], chain)
        token_address = event["args"]["token0"]
    
    token_name = token_info["name"]
    symbol = token_info["symbol"]
    native = native_token_info["symbol"]
    
    if api.get_verified(token_address, chain):
        verified = "Contract Verified"
    else:
        verified = "Contract Unverified"
    status = ""
    renounced = ""
    tax = ""
    try:
        scan = api.get_scan(token_address, chain)
        token_address_str  = str(token_address).lower()
        if "owner_address" in scan[token_address_str]:
            if scan[token_address_str]["owner_address"] == "0x0000000000000000000000000000000000000000":
                renounced = "Contract Renounced"
            else:
                renounced = "Contract Not Renounced"
        if scan[token_address_str]["is_in_dex"] == "1":
            try:
                if (
                    scan[token_address_str]["sell_tax"] == "1"
                    or scan[token_address_str]["buy_tax"] == "1"
                ):
                    return
                buy_tax_raw = (
                    float(scan[token_address_str]["buy_tax"]) * 100
                )
                sell_tax_raw = (
                    float(scan[token_address_str]["sell_tax"]) * 100
                )
                buy_tax = int(buy_tax_raw)
                sell_tax = int(sell_tax_raw)
                if sell_tax > 10 or buy_tax > 10:
                    tax = f"Tax: {buy_tax}/{sell_tax}"
                else:
                    tax = f"Tax: {buy_tax}/{sell_tax}"
            except Exception:
                tax = f"Tax: Unavailable"
        else:
            tax = f"Tax: Unavailable"
        status = f"{verified}\n{tax}\n{renounced}"
    except Exception:
        status = "Scan Unavailable"
    pool = int(tx["result"]["value"], 0) / 10**18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Liquidity: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price(chain_native))
        pool_text = (
            f'{pool} {chain_native.upper()} (${"{:0,.0f}".format(pool_dollar)})\n'
            f'Total Liquidity: ${"{:0,.0f}".format(pool_dollar * 2)}'
        )
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    try:
        image_url = defined.get_token_image(token_address, chain)
        im2 = Image.open(requests.get(image_url, stream=True).raw)
    except:
        im2 = Image.open(media.ETH_LOGO)
    im1.paste(im2, (700, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
            f"New Pair Created ({chain.upper()})\n\n"
            f"{token_name} ({symbol}/{native})\n\n"
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
                f"*New Pair Created ({chain.upper()})*\n\n"
                f"{token_name} ({symbol}/{native})\n\n"
                f"Token Address:\n`{token_address}`\n\n"
                f"{pool_text}\n\n"
                f"{status}\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"Buy On Xchange",
                            url=f"{urls.XCHANGE_BUY_ETH}{token_address}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Chart",
                            url=f"{urls.DEX_TOOLS_ETH}{event['args']['pair']}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Token Contract",
                            url=f"{urls.ETHER_ADDRESS}{token_address}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Deployer TX",
                            url=f"{urls.ETHER_TX}{event['transactionHash'].hex()}",
                        )
                    ],
                ]
            ),
        )
        try:
            if event["args"]["token0"] == ca.WBNB or event["args"]["token1"] == ca.WBNB:
                if image_url is None:
                    image_url = "N/A"

                db.token_add(token_name[1], event["args"]["pair"], token_address, chain, image_url)

        except Exception as e:
            sentry_sdk.capture_exception(e)


async def new_loan(event):
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "arb")
    try:
        address = to_checksum_address(ca.LPOOL)
        contract = web3.eth.contract(address=address, abi=api.get_abi(ca.LPOOL, chain))
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
        schedule_str = api.format_schedule(schedule1, schedule2, "BNB")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        schedule_str = ""
        amount = ""
    cost = int(tx["result"]["value"], 0) / 10**18
    native_price = api.get_native_price("bnb")
    im1 = Image.open((random.choice(media.BLACKHOLE)))
    im2 = Image.open(media.BSC_LOGO)
    im1.paste(im2, (720, 20), im2)
    i1 = ImageDraw.Draw(im1)
    i1.text(
        (26, 30),
            f"New Loan Originated (BSC)\n\n"
            f"Loan ID: {event['args']['loanID']}\n"
            f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} BNB "
            f'(${"{:0,.0f}".format(native_price * cost)})\n\n'
            f"Payment Schedule (UTC):\n{schedule_str}\n\n"
            f'Total: {amount} BNB (${"{:0,.0f}".format(native_price * amount)})',
        font = ImageFont.truetype(media.FONT, 26),
        fill = (255, 255, 255),
    )
    im1.save(r"media/blackhole.png")
    await application.bot.send_photo(
        os.getenv("MAIN_TELEGRAM_CHANNEL_ID"),
        photo=open(r"media/blackhole.png", "rb"),
        caption=
            f"*New Loan Originated (BSC)*\n\n"
            f"Loan ID: {event['args']['loanID']}\n"
            f"Initial Cost: {int(tx['result']['value'], 0) / 10 ** 18} BNB "
            f'(${"{:0,.0f}".format(api.native_price * cost)})\n\n'
            f"Payment Schedule (UTC):\n{schedule_str}\n\n"
            f'Total: {amount} BNB (${"{:0,.0f}".format(native_price * amount)}',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"Loan TX",
                        url=f"{urls.BSC_TX}{event['transactionHash'].hex()}",
                    )
                ],
            ]
        ),
    )


async def log_loop(
    pair_filter, ill001_filter, ill003_filter, poll_interval
):
    while True:
        try:
            for PairCreated in pair_filter.get_new_entries():
                await new_pair(PairCreated)

            await asyncio.sleep(poll_interval)

            for LoanOriginated in ill001_filter.get_new_entries():
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
                log_loop(pair_filter, ill001_filter, ill003_filter, 2)
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
