
from telegram import *
from telegram.ext import *
import random
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
from web3 import Web3
from eth_utils import to_checksum_address

import media
from constants import text, url, ca
from hooks import api


async def messages(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chain  = "eth"
    web3 = Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_ETH')}"))
    number = random.randint(1, 9)
    await context.bot.send_chat_action(job.chat_id, "typing")
    if number == 1:
        eth_price = api.get_native_price(chain)
        eth_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, chain)
        eth_lpool_reserve_dollar = (float(eth_lpool_reserve) * float(eth_price))
        eth_lpool = api.get_native_balance(ca.LPOOL, chain)
        eth_lpool_dollar = (float(eth_lpool) * float(eth_price))
        eth_pool = round(float(eth_lpool_reserve) + float(eth_lpool), 2)
        eth_dollar = eth_lpool_reserve_dollar + eth_lpool_dollar

        bnb_price = api.get_native_price("bnb")
        bsc_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "bsc")
        bsc_lpool_reserve_dollar = (float(bsc_lpool_reserve) * float(bnb_price))
        bsc_lpool = api.get_native_balance(ca.LPOOL, "bsc")
        bsc_lpool_dollar = (float(bsc_lpool) * float(bnb_price))
        bsc_pool = round(float(bsc_lpool_reserve) + float(bsc_lpool), 2)
        bsc_dollar = bsc_lpool_reserve_dollar + bsc_lpool_dollar

        poly_price = api.get_native_price("matic")
        poly_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "poly")
        poly_lpool_reserve_dollar = (float(poly_lpool_reserve) * float(poly_price))
        poly_lpool = api.get_native_balance(ca.LPOOL, "poly")
        poly_lpool_dollar = (float(poly_lpool) * float(poly_price))
        poly_pool = round(float(poly_lpool_reserve) + float(poly_lpool), 2)
        poly_dollar = poly_lpool_reserve_dollar + poly_lpool_dollar

        arb_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "arb")
        arb_lpool_reserve_dollar = (float(arb_lpool_reserve) * float(eth_price))
        arb_lpool = api.get_native_balance(ca.LPOOL, "arb")
        arb_lpool_dollar = (float(arb_lpool) * float(eth_price))
        arb_pool = round(float(arb_lpool_reserve) + float(arb_lpool), 2)
        arb_dollar = arb_lpool_reserve_dollar + arb_lpool_dollar

        opti_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "opti")
        opti_lpool_reserve_dollar = (float(opti_lpool_reserve) * float(eth_price))
        opti_lpool = api.get_native_balance(ca.LPOOL, "opti")
        opti_lpool_dollar = (float(opti_lpool) * float(eth_price))
        opti_pool = round(float(opti_lpool_reserve) + float(opti_lpool), 2)
        opti_dollar = opti_lpool_reserve_dollar + opti_lpool_dollar

        base_lpool_reserve = api.get_native_balance(ca.LPOOL_RESERVE, "base")
        base_lpool_reserve_dollar = (float(base_lpool_reserve) * float(eth_price))
        base_lpool = api.get_native_balance(ca.LPOOL, "base")
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
        await context.bot.send_photo(
            chat_id=job.chat_id,
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
    if number == 2:
        burn = api.get_token_balance(ca.DEAD, ca.X7R, chain)
        percent = round(burn / ca.SUPPLY * 100, 2)
        burn_dollar = api.get_price(ca.X7R, chain) * float(burn)
        im2 = Image.open(media.X7R_LOGO)
        native = f"{str(burn_dollar / api.get_native_price('eth'))[:5]} ETH"
        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
                f"X7R (ETH) Tokens Burned:\n\n"
                f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
                f"{percent}% of Supply\n\n\n\n\n\n\n\n\n"
                f'UTC: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
            font = ImageFont.truetype(media.FONT, 28),
            fill =(255, 255, 255),
        )
        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await context.bot.send_photo(
            chat_id=job.chat_id,
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"\n\nX7R (ETH) Tokens Burned:\nUse `/burn [chain-name]` for other chains\n\n"
                f'{"{:0,.0f}".format(float(burn))} / {native} (${"{:0,.0f}".format(float(burn_dollar))})\n'
                f"{percent}% of Supply\n\n"
                f"{api.get_quote()}",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Burn Wallet",
                            url=f"{url.ETHER_ADDRESS}{ca.X7R}?a={ca.DEAD}",
                        )
                    ],
                ]
            ),
        )
    if number == 3:
        gas_price = web3.eth.gas_price / 10**9
        eth_price = api.get_native_price(chain)

        try:
            pair_data = "0xc9c65396" + ca.WETH[2:].lower().rjust(64, '0') + ca.DEAD[2:].lower().rjust(64, '0')
            pair_gas_estimate = web3.eth.estimate_gas({
                'from': web3.to_checksum_address(ca.DEPLOYER),
                'to': web3.to_checksum_address(ca.FACTORY),
                'data': pair_data,})
            pair_cost_in_eth = gas_price * pair_gas_estimate
            pair_cost_in_dollars = (pair_cost_in_eth / 10**9)* eth_price
            pair_text = f"Create Pair: {pair_cost_in_eth / 10**9:.2f} ETH (${pair_cost_in_dollars:.2f})"
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
            eco_split_text = f"Ecosystem Splitter Push: {eco_split_eth / 10**9:.3f} ETH (${eco_split_dollars:.2f})"
        except Exception as e:
            print(e)
            eco_split_text = "Ecosystem Splitter Push: N/A"
        try:
            treasury_split_gas = web3.eth.estimate_gas({
                'from': web3.to_checksum_address(ca.DEPLOYER),
                'to': web3.to_checksum_address(ca.TREASURY_SPLITTER),
                'data': split_data,})
            treasury_split_eth = gas_price * treasury_split_gas
            treasury_split_dollars = (treasury_split_eth / 10**9)* eth_price
            treasury_split_text = f"Treasury Splitter Push: {treasury_split_eth / 10**9:.3f} ETH (${treasury_split_dollars:.2f})"
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
            deposit_text = f"Mint X7D: {deposit_eth / 10**9:.3f} ETH (${deposit_dollars:.2f})"
        except Exception:
            deposit_text = "Mint X7D: N/A"
        await context.bot.send_photo(
            chat_id=job.chat_id,
            photo=api.get_random_pioneer(),
            caption=
                f"*Live Xchange Costs (ETH)*\nUse `/costs [chain-name]` for other chains\n\n"
                f"{pair_text}\n"
                f"{eco_split_text}\n"
                f"{treasury_split_text}\n"
                f"{deposit_text}\n\n"
                f"{api.get_quote()}",
            parse_mode = "markdown")
    if number == 4:
        token_liquidity = []
        weth_liquidity = []
        token_dollars = []
        weth_dollars = []
        pair_addresses = [ca.X7R_PAIR_ETH,
            ca.X7DAO_PAIR_ETH,
            ca.X7101_PAIR_ETH,
            ca.X7102_PAIR_ETH,
            ca.X7103_PAIR_ETH,
            ca.X7104_PAIR_ETH,
            ca.X7105_PAIR_ETH]

        for contract_address, pair in zip(ca.TOKENS, pair_addresses):
            token_price = api.get_price(contract_address, chain)
            liquidity_data = api.get_liquidity(pair, chain)
            token_liq = float(liquidity_data["reserve0"])
            weth_liq = float(liquidity_data["reserve1"]) / 10**18
            weth_dollar = weth_liq * float(api.get_native_price(chain))
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
        im2 = Image.open(media.ETH_LOGO)
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 36),
                f"X7 Finance Token Liquidity (ETH)\n\n"
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
        await context.bot.send_photo(
            chat_id=job.chat_id,
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
    if number == 5:
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

        x7r_remaining_time_str, x7r_unlock_datetime_str = calculate_remaining_time(web3, contract, ca.X7R_PAIR_ETH, now)
        x7dao_remaining_time_str, x7dao_unlock_datetime_str = calculate_remaining_time(web3, contract, ca.X7DAO_PAIR_ETH, now)

        await context.bot.send_photo(
            chat_id=job.chat_id,
            photo=api.get_random_pioneer(),
            caption=
                f"*X7 Finance Liquidity Locks* (ETH)\nfor other chains use `/locks [chain-name]`\n\n"
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
                            url=f"{url.ETHER_ADDRESS}{ca.TIME_LOCK}#readContract",
                        )
                    ],
                ]
            ),
        )
    if number == 6:
        floor_data = api.get_nft_data(ca.PIONEER, chain)
        floor = floor_data["floor_price"]
        native_price = api.get_native_price(chain)
        if floor != "N/A":
            floor_round = round(floor, 2)
            floor_dollar = floor * float(native_price)
        else:
            floor_round = "N/A"
            floor_dollar = 0 
        pioneer_pool = api.get_native_balance(ca.PIONEER, chain)
        each = float(pioneer_pool) / 639
        each_dollar = float(each) * float(native_price)
        total_dollar = float(pioneer_pool) * float(native_price)
        img = Image.open(random.choice(media.BLACKHOLE))
        i1 = ImageDraw.Draw(img)
        i1.text(
            (28, 36),
                f"X7 Pioneer NFT Info\n\n"
                f"Floor Price: {floor_round} ETH (${'{:0,.0f}'.format(floor_dollar)})\n"
                f"Pioneer Pool: {pioneer_pool[:3]} ETH (${'{:0,.0f}'.format(total_dollar)})\n"
                f"Per Pioneer: {each:.3f} ETH (${each_dollar:,.2f})\n\n\n\n\n\n\n\n"
                f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
            font = ImageFont.truetype(media.FONT, 28),
            fill = (255, 255, 255),
        )
        img.save(r"media/blackhole.png")
        await context.bot.send_photo(
            chat_id=job.chat_id,
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
    if number == 7:
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
        await context.bot.send_photo(
            chat_id=job.chat_id,
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
    if number == 8:
        native_price = api.get_native_price(chain)
        com_eth_raw = api.get_native_balance(ca.COM_MULTI_ETH, chain)
        com_eth = round(float(com_eth_raw), 2)
        com_dollar = float(com_eth) * float(native_price)
        treasury_eth = api.get_native_balance(ca.TREASURY_SPLITTER, chain)
        eco_eth = api.get_native_balance(ca.ECO_SPLITTER, chain)
        eco_dollar = float(eco_eth) * float(native_price)
        treasury_dollar = float(treasury_eth) * float(native_price)
        com_usdt_balance = api.get_stables_balance(ca.COM_MULTI_ETH, ca.USDT, chain)
        com_usdc_balance = api.get_stables_balance(ca.COM_MULTI_ETH, ca.USDC, chain)
        stables = com_usdt_balance + com_usdc_balance
        com_x7r_balance = api.get_token_balance(ca.COM_MULTI_ETH, ca.X7R, chain)
        com_x7r_price = com_x7r_balance * api.get_price(ca.X7R, chain)
        com_x7dao_balance = api.get_token_balance(ca.COM_MULTI_ETH, ca.X7DAO, chain)
        com_x7dao_price = com_x7dao_balance * api.get_price(ca.X7DAO, chain)
        com_x7d_balance = api.get_token_balance(ca.COM_MULTI_ETH, ca.X7D, chain)
        com_x7d_price = com_x7d_balance * native_price
        com_total = com_x7r_price + com_dollar + com_x7d_price + com_x7dao_price + stables
        im2 = Image.open(media.ETH_LOGO)
        im1 = Image.open((random.choice(media.BLACKHOLE)))
        im1.paste(im2, (720, 20), im2)
        i1 = ImageDraw.Draw(im1)
        i1.text(
            (28, 10),
                f"X7 Finance Treasury (ETH)\n\n"
                f"Community Wallet:\n{com_eth} ETH (${'{:0,.0f}'.format(com_dollar)})\n"
                f"{com_x7d_balance} X7D (${'{:0,.0f}'.format(com_x7d_price)})\n"
                f"{com_x7r_balance} X7R (${'{:0,.0f}'.format(com_x7r_price)})\n"
                f"{com_x7dao_balance} X7DAO (${'{:0,.0f}'.format(com_x7dao_price)})\n"
                f"${'{:0,.0f}'.format(stables)} USDT/C\n"
                f"Total: (${'{:0,.0f}'.format(com_total)})\n\n"
                f"Ecosystem Splitter:\n{eco_eth[:6]} ETH (${'{:0,.0f}'.format(eco_dollar)})\n\n"
                f"Treasury Splitter:\n{treasury_eth[:6]} ETH (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                f"UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
            font = ImageFont.truetype(media.FONT, 24),
            fill = (255, 255, 255),
        )

        img_path = os.path.join("media", "blackhole.png")
        im1.save(img_path)
        await context.bot.send_photo(
            chat_id=job.chat_id,
            photo=open(r"media/blackhole.png", "rb"),
            caption=
                f"*X7 Finance Treasury (ETH)*\nUse `/treasury [chain-name]` for other chains\n\n"
                f'Community Wallet:\n{com_eth} ETH (${"{:0,.0f}".format(com_dollar)})\n'
                f'{com_x7d_balance} X7D (${"{:0,.0f}".format(com_x7d_price)})\n'
                f'{"{:0,.0f}".format(com_x7r_balance)} X7R (${"{:0,.0f}".format(com_x7r_price)})\n'
                f'{"{:0,.0f}".format(com_x7dao_balance)} X7DAO (${"{:0,.0f}".format(com_x7dao_price)})\n'
                f"${'{:0,.0f}'.format(stables)} USDT/C\n"
                f'Total: (${"{:0,.0f}".format(com_total)})\n\n'
                f"Ecosystem Splitter: {eco_eth[:6]} ETH (${'{:0,.0f}'.format(eco_dollar)})\n"
                f"Treasury Splitter: {treasury_eth[:6]} ETH (${'{:0,.0f}'.format(treasury_dollar)})\n\n"
                f"{api.get_quote()}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Community Multi-sig Wallet",
                            url=f"{url.ETHER_ADDRESS}{ca.COM_MULTI_ETH}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Ecosystem Splitter Contract",
                            url=f"{url.ETHER_ADDRESS}{ca.ECO_SPLITTER}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Treasury Splitter Contract",
                            url=f"{url.ETHER_ADDRESS}{ca.TREASURY_SPLITTER}",
                        )
                    ],
                ]
            ),
        )
    if number == 9:
        messages = [text.ABOUT, text.AIRDROP, text.ECOSYSTEM,
            text.VOLUME, random.choice(text.QUOTES)]
        random_message = random.choice(messages)
        if random_message in text.QUOTES:
            message = f"*X7 Finance Whitepaper Quote*\n\n{random_message}"
        else:
            message = random_message

        await context.bot.send_message(
            chat_id=job.chat_id,
            text=f"{message}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="Xchange App", url=f"{url.XCHANGE}")],
                    [InlineKeyboardButton(text="Website", url=f"{url.WEBSITE}")],
                ]
            ),
        )


async def replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"{update.effective_message.text}"
    lower_message = message.lower()
    keyword_to_response = {
        "https://twitter": {
            "text": random.choice(text.X_REPLIES),
            "mode": None,
        },
        "https://x.com": {
            "text": random.choice(text.X_REPLIES),
            "mode": None,
        },
        "gm": {"sticker": media.GM},
        "gm!": {"sticker": media.GM},
        "new on chain message": {"sticker": media.ONCHAIN},
        "lfg": {"sticker": media.LFG},
        "goat": {"sticker": media.GOAT},
        "smashed": {"sticker": media.SMASHED},
        "wagmi": {"sticker": media.WAGMI},
        "slapped": {"sticker": media.SLAPPED},
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