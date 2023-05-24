from telegram.ext import *
from telegram import *
import api
import asyncio
import ca
from datetime import datetime, timezone
import keys
import logging
import media
from PIL import Image, ImageDraw, ImageFont
import random
import time
import url
from web3 import Web3
from web3.exceptions import Web3Exception

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

getblock_url = f'https://bsc.getblock.io/{keys.getblock}'
web3 = Web3(Web3.HTTPProvider(getblock_url))

factory = web3.eth.contract(address=ca.pancake, abi=api.get_abi(ca.pancake, "bsc"))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001, "bsc"))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002, "bsc"))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003, "bsc"))
time_lock = web3.eth.contract(address=ca.time_lock, abi=api.get_abi(ca.time_lock, "bsc"))

async def new_loan(event):
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Loan Originated (ETH)\n\n{event["loanID"]}\n\n'
            f'https://etherscan.io/tx/{event["transactionHash"].hex()}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        "-1001780235511",
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Loan Originated (ETH)*\n\n{event["loanID"]}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def new_pair(event):
    print("Pair found")
    tx = api.get_tx_from_hash(event["transactionHash"].hex(), "bsc")
    liq = api.get_liquidity(event["args"]["pair"], "bsc")
    if event["args"]["token0"] == ca.wbnb:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10 ** 18
    elif event["args"]["token0"] in ca.bscpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = 0
    elif event["args"]["token1"] in ca.bscpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = 0
    elif event["args"]["token0"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = dollar = int(weth) * 2 * api.get_native_price("eth") / 10 ** 18
    elif event["args"]["token0"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token0"], "bsc")
        token_name = api.get_token_name(event["args"]["token1"], "bsc")
        token_address = event["args"]["token1"]
        weth = liq["reserve0"]
        token = liq["reserve1"]
        dollar = int(weth) * 2 / 10 ** 18
    elif event["args"]["token1"] in ca.bscethpairs:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 / 10 ** 18
    else:
        native = api.get_token_name(event["args"]["token1"], "bsc")
        token_name = api.get_token_name(event["args"]["token0"], "bsc")
        token_address = event["args"]["token0"]
        weth = liq["reserve1"]
        token = liq["reserve0"]
        dollar = int(weth) * 2 * api.get_native_price("bnb") / 10 ** 18
    info = api.get_token_data(token_address, "bsc")
    if info[0]["decimals"] == "" or info[0]["decimals"] == "0" or not info[0]["decimals"]:
        supply = int(api.get_supply(token_address, "bsc"))
    else:
        supply = int(api.get_supply(token_address, "bsc")) / 10 ** int(info[0]["decimals"])
    if dollar == 0:
        liquidity_text = 'Total Liquidity: Unavailable'
    else:
        liquidity_text = f'Total Liquidity: ${"{:0,.0f}".format(dollar)}'
    verified = api.get_verified(token_address, "bsc")
    status = ""
    tax = ""
    renounced = ""
    lock = ""
    tax_warning = ""
    if verified == "Yes":
        print(f'V2 Pair Found')
        contract = web3.eth.contract(address=token_address, abi=api.get_abi(token_address, "eth"))
        verified = '✅ Contract Verified'
        time.sleep(10)
        scan = api.get_scan(token_address, "eth")
        if scan[f'{str(token_address).lower()}']["is_open_source"] == "1":
            try:
                if scan[f'{str(token_address).lower()}']["slippage_modifiable"] == "1":
                    tax_warning = "(Changeable)"
                else:
                    tax_warning = ""
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Error: {e}')
            try:
                if scan[f'{str(token_address).lower()}']["is_honeypot"] == "1":
                    print('Skip - Honey Pot')
                    return
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Error: {e}')
            try:
                if scan[f'{str(token_address).lower()}']["is_mintable"] == "1":
                    print('Skip - Mintable')
                    return
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Initial Error: {e}')
        if scan[f'{str(token_address).lower()}']["is_in_dex"] == "1":
            try:
                if scan[f'{str(token_address).lower()}']["sell_tax"] == "1" \
                        or scan[f'{str(token_address).lower()}']["buy_tax"] == "1":
                    print('Skip - Cannot Buy')
                    return
                buy_tax_raw = float(scan[f'{str(token_address).lower()}']["buy_tax"]) * 100
                sell_tax_raw = float(scan[f'{str(token_address).lower()}']["sell_tax"]) * 100
                buy_tax = int(buy_tax_raw)
                sell_tax = int(sell_tax_raw)
                if sell_tax > 10 or buy_tax > 10:
                    tax = f'⚠️ Tax: {buy_tax}/{sell_tax} {tax_warning}'
                else:
                    tax = f'✅️ Tax: {buy_tax}/{sell_tax} {tax_warning}'
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Tax Error: {e}')
                tax = f'⚠️ Tax: Unavailable {tax_warning}'
            if "lp_holders" in scan[f'{str(token_address).lower()}']:
                lp_holders = scan[f'{str(token_address).lower()}']["lp_holders"]
            try:
                locked_lp_list = [
                    lp for lp in scan[f'{str(token_address).lower()}']["lp_holders"]
                    if lp["is_locked"] == 1 and lp["address"] != "0x0000000000000000000000000000000000000000"]
                if locked_lp_list:
                    lp_with_locked_detail = [lp for lp in locked_lp_list if "locked_detail" in lp]
                    if lp_with_locked_detail:
                        lock =\
                            f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - {locked_lp_list[0]['percent'][:6]}%\n" \
                            f"Unlock - {locked_lp_list[0]['locked_detail'][0]['end_time']}"
                    else:
                        lock = f"✅ Liquidity Locked\n{locked_lp_list[0]['tag']} - {locked_lp_list[0]['percent'][:6]}%\n"
                else:
                    lock = ""
            except (Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
                print(f'Liquidity Error: {e}')
        else:
            tax = f'⚠️ Tax: Unavailable {tax_warning}'
        try:
            owner = contract.functions.owner().call()
            if owner == "0x0000000000000000000000000000000000000000":
                renounced = '✅ Contract Renounced'
        except (Exception, TimeoutError, ValueError, StopAsyncIteration):
            status = verified
    status = f'{verified}\n{tax}\n{renounced}\n{lock}'
    pool = int(tx["result"]["value"], 0) / 10 ** 18
    if pool == 0 or pool == "" or not pool:
        pool_text = "Launched Pool Amount: Unavailable"
    else:
        pool_dollar = float(pool) * float(api.get_native_price("bnb")) / 1 ** 18
        pool_text = f'Launched Pool Amount: {pool} BNB (${"{:0,.0f}".format(pool_dollar)})'
    status = f'{verified}\n{tax}\n{renounced}\n{lock}\n'
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.bsc_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'New Pair Created (BSC)\n\n'
            f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
            f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
            f'{pool_text}\n\n'
            f'{liquidity_text}\n\n'
            f'SCAN:\n'
            f'{status}\n',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        keys.alerts_id,
        photo=open(r"media\blackhole.png", 'rb'),
        caption=f'*New Pair Created (BSC)*\n\n'
                f'{token_name[0]} ({token_name[1]}/{native[1]})\n\n'
                f'Token Address:\n`{token_address}`\n\n'
                f'Supply: {"{:0,.0f}".format(supply)} ({info[0]["decimals"]} Decimals)\n\n'
                f'{pool_text}\n\n'
                f'SCAN:\n'
                f'{liquidity_text}\n\n'
                f'{status}', parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=f'Buy On Xchange (COMING SOON)', url=f'{url.xchange_buy_bsc}')],
             [InlineKeyboardButton(text='Chart', url=f'{url.dex_tools_bsc}{event["args"]["pair"]}')],
             [InlineKeyboardButton(text='Token Contract', url=f'{url.bsc_address}{token_address}')],
             [InlineKeyboardButton(text='Deployer TX', url=f'{url.bsc_tx}{event["transactionHash"].hex()}')], ]))
    print(f'V2 Pair sent: ({token_name[1]}/{native[1]})')

async def time_lock_extend(event):
    token_name = api.get_token_name(event["args"]["tokenAddress"], "eth")
    time = datetime.fromtimestamp(event["tokenAddress"], timezone.utc)
    im1 = Image.open((random.choice(media.blackhole)))
    im2 = Image.open(media.eth_logo)
    im1.paste(im2, (720, 20), im2)
    myfont = ImageFont.truetype(r'media\FreeMonoBold.ttf', 26)
    i1 = ImageDraw.Draw(im1)
    i1.text((26, 30),
            f'Token Unlock Time Extended (ETH)\n\n*{token_name}*\n\n'
            f'{event["tokenAddress"]}\n'
            f'{time}\n\n'
            f'https://etherscan.io/tx/{event["transactionHash"].hex()}',
            font=myfont, fill=(255, 255, 255))
    im1.save(r"media\blackhole.png")
    await application.bot.send_photo(
        "-1001780235511",
        photo=open(r"media\blackhole.png"),
        caption=f'*Token Unlock Time Extended (ETH)*\n\n*{token_name}*\n\n'
                f'{event["tokenAddress"]}\n'
                f'{time}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def log_loop(
        v2_pair_filter, ill001_filter, ill002_filter, ill003_filter, poll_interval):
    while True:
        try:
            for PairCreated in v2_pair_filter.get_new_entries():
                await new_pair(PairCreated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill001_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill002_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
            for LoanOriginated in ill003_filter.get_new_entries():
                await new_loan(LoanOriginated)
                application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
            await asyncio.sleep(poll_interval)
        except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
            print(f'Loop Error: {e}')
            break
        break

def main():
    print("Scanning BSC Network")
    pair_filter = factory.events.PairCreated.create_filter(fromBlock='latest')
    ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock='latest')
    ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock='latest')
    ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(log_loop(
            pair_filter, ill001_filter, ill002_filter, ill003_filter, 2)))
    except (Web3Exception, Exception, TimeoutError, ValueError, StopAsyncIteration) as e:
        print(f'Error: {e}')
        loop.close()
        asyncio.run(main())
    finally:
        loop.close()


if __name__ == "__main__":
    application = ApplicationBuilder().token(random.choice(keys.tokens)).connection_pool_size(512).build()
    asyncio.run(main())
