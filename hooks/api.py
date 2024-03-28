# API

import random, requests, os, time as t, json
from typing import Tuple
from datetime import datetime, timedelta
from moralis import evm_api
from pycoingecko import CoinGeckoAPI
from web3 import Web3
from constants import ca, mappings, urls


class Dextools:
    def __init__(self):
        self.plan = "trial"
        self.headers = {
        'accept': 'application/json',
        'x-api-key': os.getenv("DEXTOOLS_API_KEY")}
        self.url = f"http://public-api.dextools.io/{self.plan}/v2/"


    def get_dex(self, pair, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f'pool/{chain_info.dext}/{pair}'

        response = requests.get(self.url + endpoint, headers=self.headers)
        data = response.json()
        try:
            if data is not None:
                if "data" in data and "exchange" in data["data"] and "name" in data["data"]["exchange"]:
                    return data["data"]["exchange"]["name"]
                else:
                    return "Unknown DEX"
            else:
                return "Unknown DEX"
        except Exception:
            "Unknown DEX"
    

    def get_price(self, token, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f'token/{chain_info.dext}/{token}/price'

        response = requests.get(self.url + endpoint, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') is not None and 'price' in data['data']:
                price = data['data']['price']
                if "e-" in str(price):
                    price = "{:.8f}".format(price)
                elif price < 1:
                    price = "{:.8f}".format(price) 
                else:
                    price = "{:.2f}".format(price)

                one_hour_change = data['data']['variation1h']
                six_hour_change = data['data']['variation6h']
                one_day_change = data['data']['variation24h']

                emoji_up = "📈"
                emoji_down = "📉"
                one_hour = f"{emoji_up if one_hour_change is not None and one_hour_change > 0 else emoji_down} 1H Change: {round(one_hour_change, 2)}%" if one_hour_change is not None else f'{emoji_down} 1H Change: N/A'
                six_hour = f"{emoji_up if six_hour_change is not None and six_hour_change > 0 else emoji_down} 6H Change: {round(six_hour_change, 2)}%" if six_hour_change is not None else f'{emoji_down} 6H Change: N/A'
                one_day = f"{emoji_up if one_day_change is not None and one_day_change > 0 else emoji_down} 24H Change: {round(one_day_change, 2)}%" if one_day_change is not None else f'{emoji_down} 24H Change: N/A'

                change = {
                    "one_hour": one_hour,
                    "six_hour": six_hour,
                    "one_day": one_day
                    }

            else:
                price = "N/A"
                change = {
                    "one_hour": "📉 1H Change: N/A",
                    "six_hour": "📉 6H Change:N/A",
                    "one_day": "📉 2H Change: N/A",
                }

            return price, change
        else:
            return 0, "N/A"
        

    def get_token_info(self, pair, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f"token/{chain_info.dext}/{pair}/info"
        response = requests.get(self.url + endpoint, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            if data and "data" in data and data["data"]:
                total_supply = data["data"].get("totalSupply", 0)
                mcap = data["data"].get("mcap", 0)
                holders = data["data"].get("holders", 0)

                if mcap is not None:
                    formatted_mcap = "${:,.0f}".format(mcap)
                else:
                    fdv = data["data"].get("fdv", 0)
                    if fdv is not None:
                        formatted_mcap = f'${fdv:,.0f} (FDV)'
                    else:
                        formatted_mcap = "N/A"

                return {
                    "supply": total_supply,
                    "mcap": formatted_mcap,
                    "holders": holders
                }
            else:
                return {
                    "total_supply": 0,
                    "mcap": "N/A",
                    "holders": "N/A"
                }
        else:
            return {
                "supply": 0,
                "mcap": "N/A",
                "holders": "N/A"
            }
        
    def get_token_name(self, address, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f"token/{chain_info.dext}/{address}"
        response = requests.get(self.url + endpoint, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data and data["data"]:
                name = data["data"].get("name", "N/A")
                symbol = data["data"].get("symbol", "N/A")

                return {
                    "name": name,
                    "symbol": symbol
                }
            else:
                return {
                    "name": "N/A",
                    "symbol": "N/A"
                }
        else:
            return {
                "name": "N/A",
                "symbol": "N/A"
            }


    def get_liquidity(self, pair, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f'pool/{chain_info.dext}/{pair}/liquidity'

        response = requests.get(self.url + endpoint, headers=self.headers)

        if response.status_code == 200:
            try:
                data = response.json()

                total = data['data']['liquidity']
                token = data['data']['reserves']['mainToken']
                eth = data['data']['reserves']['sideToken']
                return {"total": f"${'{:,.0f}'.format(total)}",
                        "token": f"{'{:,.0f}'.format(token)}",
                        "eth": f"{'{:,.2f}'.format(eth)}"}

            except Exception:
                return {"total": "N/A",
                        "token": "N/A",
                        "eth:": "N/A"
                }
        else:
            return {"total": "N/A",
                    "token": "N/A",
                    "eth:": "N/A"
            }
        

    def get_volume(self, pair, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        endpoint = f"pool/{chain_info.dext}/{pair}/price"

        response = requests.get(self.url + endpoint, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            try:
                return f'${"{:,.0f}".format(float(data["data"]["volume24h"]))}'
            except Exception:
                return "N/A"
        else:
            return "N/A"


class CoinGecko:
    def __init__(self):
        self.url = f"https://api.coingecko.com/api/v3/"


    def get_ath(self, token):
        endpoint = (
            f"coins/{token}?localization=false&tickers=false&market_data="
            "true&community_data=false&developer_data=false&sparkline=false"
        )
        response = requests.get(self.url + endpoint)
        data = response.json()
        value = data["market_data"]
        return (
            value["ath"]["usd"],
            value["ath_change_percentage"]["usd"],
            value["ath_date"]["usd"],
        )


    def get_price(self, token):
        coingecko = CoinGeckoAPI()
        data = coingecko.get_price(
            ids=token,
            vs_currencies="usd",
            include_24hr_change="true",
            include_24hr_vol="true",
            include_market_cap="true")
        if "e-" in str(data[token]["usd"]):
            price = "{:.8f}".format(data[token]["usd"])
        elif data[token]["usd"] < 1:
            price = "{:.8f}".format(data[token]["usd"]) 
        else:
            price = "{:,.0f}".format(data[token]["usd"])

        if "e-" in str(data[token]["usd_24h_vol"]):
            volume = "${:.8f}".format(data[token]["usd_24h_vol"])
        elif data[token]["usd_24h_vol"] < 1:
            volume = "${:.8f}".format(data[token]["usd_24h_vol"]) 
        else:
            volume = "${:,.0f}".format(data[token]["usd_24h_vol"])
            
        price_change = data[token]["usd_24h_change"]
        if price_change is None:
            price_change = 0
        else:
            price_change = round(data[token]["usd_24h_change"], 2)
        market_cap = data[token]["usd_market_cap"]
        if market_cap is None or market_cap == 0:
            market_cap_formatted = " N/A"
        else:
            market_cap_formatted = "${:0,.0f}".format(float(market_cap))

        return {"price": price, "change": price_change, "mcap": market_cap_formatted, "volume": volume}


    def search(self, token):
        endpoint = f"search?query={token}"
        response = requests.get(self.url + endpoint)
        return response.json()


    def get_mcap(self, token):
        endpoint = f"simple/price?ids={token}&vs_currencies=usd&include_market_cap=true"
        response = requests.get(self.url + endpoint)
        data = response.json()
        return data[token]["usd_market_cap"]


class Defined:
    def __init__(self):
        self.url = "https://graph.defined.fi/graphql"
        self.headers = {
            "content_type": "application/json",
            "Authorization": os.getenv("DEFINED_API_KEY")
        }


    def get_price_change(self, address, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]

        current_timestamp = int(datetime.now().timestamp()) - 300
        one_hour_ago_timestamp = int((datetime.now() - timedelta(hours=1)).timestamp())
        twenty_four_hours_ago_timestamp = int((datetime.now() - timedelta(hours=24)).timestamp())
        seven_days_ago_timestamp = int((datetime.now() - timedelta(days=7)).timestamp())

        pricechange = f"""query {{
            getTokenPrices(
                inputs: [
                    {{ 
                        address: "{address}"
                        networkId: {chain_info.id}
                        timestamp: {current_timestamp}
                    }}
                    {{ 
                        address: "{address}"
                        networkId: {chain_info.id}
                        timestamp: {one_hour_ago_timestamp}
                    }}
                    {{ 
                        address: "{address}"
                        networkId: {chain_info.id}
                        timestamp: {twenty_four_hours_ago_timestamp}
                    }}
                    {{ 
                        address: "{address}"
                        networkId: {chain_info.id}
                        timestamp: {seven_days_ago_timestamp}
                    }}
                ]
            ) {{
                priceUsd
            }}
        }}"""
        try:
            response = requests.post(self.url, headers=self.headers, json={"query": pricechange})
            data = response.json()

            current_price = data["data"]["getTokenPrices"][0]["priceUsd"]
            one_hour_ago_price = data["data"]["getTokenPrices"][1]["priceUsd"]
            twenty_four_hours_ago_price = data["data"]["getTokenPrices"][2]["priceUsd"]
            seven_days_ago_price = data["data"]["getTokenPrices"][3]["priceUsd"]

            one_hour_change = round(((current_price - one_hour_ago_price) / one_hour_ago_price) * 100, 2)
            twenty_four_hours_change = round(
                ((current_price - twenty_four_hours_ago_price) / twenty_four_hours_ago_price) * 100, 2)
            seven_days_change = round(((current_price - seven_days_ago_price) / seven_days_ago_price) * 100, 2)

            emoji_up = "📈"
            emoji_down = "📉"

            one_hour_change_str = f"{emoji_up if one_hour_change > 0 else emoji_down} 1H Change: {one_hour_change}%"
            twenty_four_hours_change_str = f"{emoji_up if twenty_four_hours_change > 0 else emoji_down} 24H Change: {twenty_four_hours_change}%"
            seven_days_change_str = f"{emoji_up if seven_days_change > 0 else emoji_down} 7D Change: {seven_days_change}%"

            result = (
                f"{one_hour_change_str}\n"
                f"{twenty_four_hours_change_str}\n"
                f"{seven_days_change_str}"
            )
        except Exception as e:
            result = "  1H Change: N/A\n  24H Change: N/A\n  7D Change: N/A"
        return result


    def get_token_image(self, token, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]

        image = f'''
            query {{
                getTokenInfo(address:"{token}", networkId:{chain_info.id}) {{
                    imageLargeUrl
                }}
            }}
        '''

        response = requests.post(self.url, headers=self.headers, json={"query": image})
        data = response.json()
        if 'data' in data and 'getTokenInfo' in data['data']:
                token_info = data['data']['getTokenInfo']

                if token_info and 'imageLargeUrl' in token_info:
                    image_url = token_info['imageLargeUrl']
                    return image_url
                else:
                    return "N/A"
        else:
            return "N/A"


    def get_pair(self, address, chain):
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]
        
        pair_query = f"""query {{
            listPairsWithMetadataForToken (tokenAddress: "{address}" networkId: {chain_info.id}) {{
                results {{
                    pair {{
                        address
                    }}
                }}
            }}
            }}"""
        
        response = requests.post(self.url, headers=self.headers, json={"query": pair_query})
        data = response.json()
        if response.status_code == 200:
            data = response.json()
            pair = data.get('data', {}).get('listPairsWithMetadataForToken', {}).get('results', [])[0].get('pair', {}).get('address')
            return pair
        else:
            return None


    def get_volume(self, pair, chain):
        try:
            if chain in mappings.CHAINS:
                chain_info = mappings.CHAINS[chain]

            volume = f'''
                query {{
                getDetailedPairStats(pairAddress: "{pair}", networkId: {chain_info.id}, bucketCount: 1, tokenOfInterest: token1) {{
                    stats_day1 {{
                    statsUsd {{
                        volume {{
                        currentValue
                        }}
                    }}
                    }}
                }}
                }}
                '''

            response = requests.post(self.url, headers=self.headers, json={"query": volume})
            data = response.json()

            current_value = data['data']['getDetailedPairStats']['stats_day1']['statsUsd']['volume']['currentValue']
            return "${:,.0f}".format(float(current_value))
        except Exception as e:
                return "N/A"
        
        
class Opensea:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "X-API-KEY": os.getenv("OPENSEA_API_KEY")
        }
        self.url = f"https://api.opensea.io/v2/"
        

    def get_nft_collection(self, slug):
        endpoint = f"collections/{slug}"
        response = requests.get(self.url + endpoint, headers=self.headers)
        data = response.json()
        return data


    def get_nft_id(self, nft, identifier):
        endpoint = f"chain/ethereum/contract/{nft}/nfts/{identifier}"
        response = requests.get(self.url + endpoint, headers=self.headers)
        data = response.json()
        return data
    

# SCAN


def get_abi(contract: str, chain: str) -> str:
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"][0]["ABI"]


def get_block(chain: str, time: "int") -> str:
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=block&action=getblocknobytime&timestamp={time}&closest=before{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_daily_tx_count(contract: str, chain: str, ) -> int:
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    yesterday = int(t.time()) - 86400
    block_yesterday = get_block(chain, yesterday)
    block_now = get_block(chain, int(t.time()))
    tx_url = f"{chain_info.api}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
    tx_response = requests.get(tx_url)
    tx_data = tx_response.json()
    tx_entry_count = len(tx_data['result']) if 'result' in tx_data else 0
    internal_tx_url = f"{chain_info.api}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
    internal_tx_response = requests.get(internal_tx_url)
    internal_tx_data = internal_tx_response.json()
    internal_tx_entry_count = len(internal_tx_data['result']) if 'result' in internal_tx_data else 0
    entry_count = tx_entry_count + internal_tx_entry_count
    return entry_count


def get_gas(chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=gastracker&action=gasoracle{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_native_balance(wallet, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=account&action=balancemulti&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    amount_raw = float(data["result"][0]["balance"])
    return f"{amount_raw / 10 ** 18}"


def get_native_price(token):
    tokens_info = {
        "eth": {
            "url": "https://api.etherscan.io/api?module=stats&action=ethprice",
            "key": os.getenv("ETHER"),
            "field": "ethusd",
        },
        "bnb": {
            "url": "https://api.bscscan.com/api?module=stats&action=bnbprice",
            "key": os.getenv("BSC"),
            "field": "ethusd",
        },
        "matic": {
            "url": "https://api.polygonscan.com/api?module=stats&action=maticprice",
            "key": os.getenv("POLY"),
            "field": "maticusd",
        },
    }
    if token not in tokens_info:
        raise ValueError(f"Invalid token: {token}")
    url = f"{tokens_info[token]['url']}&{tokens_info[token]['key']}"
    response = requests.get(url)
    data = response.json()
    return float(data["result"][tokens_info[token]["field"]]) / 1**18


def get_pool_liq_balance(wallet, token, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.Session().get(url)
    data = response.json()
    return int(data["result"] or 0)


def get_stables_balance(wallet, token, chain):
    try:
        if chain not in mappings.CHAINS:
            raise ValueError(f"Invalid chain: {chain}")

        chain_info = mappings.CHAINS[chain]
        url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return int(data["result"][:-6])
    except Exception as e:
        return 0


def get_supply(token, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=stats&action=tokensupply&contractaddress={token}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_token_balance(wallet, token, chain):
    try:
        if chain not in mappings.CHAINS:
            raise ValueError(f"Invalid chain: {chain}")
        chain_info = mappings.CHAINS[chain]
        url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
        response = requests.get(url)
        data = response.json()
        return int(data["result"][:-18])
    except Exception:
        return 0


def get_tx_from_hash(tx, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=proxy&action=eth_getTransactionByHash&txhash={tx}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_tx(address, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=account&action=txlist&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_internal_tx(address, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=account&action=txlistinternal&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_verified(contract, chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return True if "SourceCode" in data["result"][0] else False


def get_x7r_supply(chain):
    if chain not in mappings.CHAINS:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = mappings.CHAINS[chain]
    url = f"{chain_info.api}?module=account&action=tokenbalance&contractaddress={ca.X7R}&address={ca.DEAD}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    supply = ca.SUPPLY - int(data["result"][:-18])
    return supply


# OTHER


async def burn_x7r(amount):
    try:
        alchemy_keys = os.getenv("ALCHEMY_ETH")
        alchemy_eth_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_keys}"
        w3 = Web3(Web3.HTTPProvider(alchemy_eth_url))
        sender_address = os.getenv("BURN_WALLET")
        recipient_address = ca.DEAD
        token_contract_address = ca.X7R
        sender_private_key = os.getenv("BURN_WALLET_PRIVATE_KEY")
        decimals = 18  
        amount_to_send_wei = amount * (10 ** decimals)

        token_transfer_data = (
            '0xa9059cbb'
            + recipient_address[2:].rjust(64, '0')
            + hex(amount_to_send_wei)[2:].rjust(64, '0')
        )

        nonce = w3.eth.get_transaction_count(sender_address)
        gas = w3.eth.estimate_gas({
            'from': sender_address,
            'to': token_contract_address,
            'data': token_transfer_data,
        })

        transaction = {
            'from': sender_address,
            'to': token_contract_address,
            'data': token_transfer_data,
            'gasPrice': w3.to_wei(w3.eth.gas_price / 1e9 , 'gwei'),
            'gas': gas,
            'nonce': nonce,
        }

        signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return f"{amount} X7R Burnt\n\n{urls.ETHER_TX}{tx_hash.hex()}"
    except Exception as e:
        return f'Error burning X7R: {e}'


def datetime_to_timestamp(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        timestamp = datetime_obj.timestamp()
        return timestamp
    except ValueError:
        return "Invalid datetime format. Please use YYYY-MM-DD HH:MM."


def timestamp_to_datetime(timestamp):
    try:
        datetime_obj = datetime.fromtimestamp(timestamp)
        datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M')
        return datetime_str
    except ValueError:
        return "Invalid timestamp."


def format_schedule(schedule1, schedule2, native_token):
    current_datetime = datetime.utcnow()
    next_payment_datetime = None
    next_payment_value = None

    def format_date(date):
        return datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")

    def calculate_time_remaining_str(time_remaining):
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"

    all_dates = sorted(set(schedule1[0] + schedule2[0]))

    schedule_list = []

    for date in all_dates:
        value1 = next((v for d, v in zip(schedule1[0], schedule1[1]) if d == date), 0)
        value2 = next((v for d, v in zip(schedule2[0], schedule2[1]) if d == date), 0)

        total_value = value1 + value2

        formatted_date = format_date(date)
        formatted_value = total_value / 10**18
        sch = f"{formatted_date} - {formatted_value} {native_token}"
        schedule_list.append(sch)

        if datetime.fromtimestamp(date) > current_datetime:
            if next_payment_datetime is None or datetime.fromtimestamp(date) < next_payment_datetime:
                next_payment_datetime = datetime.fromtimestamp(date)
                next_payment_value = formatted_value

    if next_payment_datetime:
        time_until_next_payment = next_payment_datetime - current_datetime
        time_remaining_str = calculate_time_remaining_str(time_until_next_payment)

        schedule_list.append(f"\nNext Payment Due:\n{next_payment_value} {native_token}\n{time_remaining_str}")

    return "\n".join(schedule_list)


def escape_markdown(text):
    characters_to_escape = ['*', '_', '`']
    for char in characters_to_escape:
        text = text.replace(char, '\\' + char)
    return text


def get_duration_years(duration):
    years = duration.days // 365
    months = (duration.days % 365) // 30
    weeks = ((duration.days % 365) % 30) // 7
    days = ((duration.days % 365) % 30) % 7
    return years, months, weeks, days


def get_duration_days(duration):
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes = (remainder % 3600) // 60
    return days, hours, minutes


def get_fact():
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    quote = response.json()
    return quote["text"]


def get_nft_data(nft, chain):
    try:
        if chain in mappings.CHAINS:
            chain_info = mappings.CHAINS[chain]

        url = f"https://api.blockspan.com/v1/collections/contract/{nft}?chain={chain_info.blockspan}"
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
            }
        )
        data = response.json()

        info = {"holder_count": 0, "floor_price": "N/A"}

        holder_count = data.get("total_tokens", None)
        if holder_count is not None:
            info["holder_count"] = int(holder_count)

        exchange_data = data.get("exchange_data")
        if exchange_data is not None:
            for item in exchange_data:
                stats = item.get("stats")
                if stats is not None:
                    floor_price = stats.get("floor_price")
                    if floor_price is not None:
                        info["floor_price"] = floor_price
                        break
        return info

    except Exception:
        return {"holder_count": 0, "floor_price": "N/A"}


def get_nft_holder_list(nft, chain):
    if chain in mappings.MORALIS_CHAINS:
        chain = mappings.MORALIS_CHAINS[chain]
    return evm_api.nft.get_nft_owners(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "format": "decimal", "address": nft},
    )


def get_proposers(chain):
    today = datetime.now().strftime("%Y-%m-%d")
    url_graphql = "https://streaming.bitquery.io/graphql"
    headers_graphql = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("BITQUERY_API_KEY")}'
    }

    graphql_query = f'''
    {{
      EVM(dataset: archive, network: {chain}) {{
        TokenHolders(
          date: "{today}"
          tokenSmartContract: "{ca.X7DAO}"
          where: {{ Balance: {{ Amount: {{ ge: "500000" }} }} }}
        ) {{
          uniq(of: Holder_Address)
        }}
      }}
    }}
    '''
    payload_graphql = json.dumps({'query': graphql_query})

    try:
        response_graphql = requests.post(url_graphql, headers=headers_graphql, data=payload_graphql)

        if response_graphql.status_code == 200:
            result = response_graphql.json()
            number_of_holders = result.get('data', {}).get('EVM', {}).get('TokenHolders', [])[0].get('uniq', '0')
            return int(number_of_holders)
        else:
            return "N/A"

    except requests.RequestException as e:
        return "N/A"


def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    data = response.json()
    quote = random.choice(data)
    quote_text = quote["text"]
    quote_author = quote["author"]
    if quote_author.endswith(", type.fit"):
        quote_author = quote_author[:-10].strip()

    return f'`"{quote_text}"\n\n-{quote_author}`'


def get_random_pioneer():
    number = f"{random.randint(1, 4480)}".zfill(4)
    return f"{urls.PIONEERS}{number}.png"


def get_scan(token: str, chain: str) -> dict:
    if chain in mappings.CHAINS:
        chain_info = mappings.CHAINS[chain]
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_info.id}?contract_addresses={token}"
    response = requests.get(url)
    return response.json()["result"]


def get_signers(wallet):
    url = f"https://safe-transaction-mainnet.safe.global/api/v1/safes/{wallet}/"
    response = requests.get(url)
    return response.json()


def get_snapshot():
    url = "https://hub.snapshot.org/graphql"
    query = {
        "query": 'query { proposals ( first: 1, skip: 0, where: { space_in: ["X7COMMUNITY.eth"]}, '
                 'orderBy: "created", orderDirection: desc ) { id title start end snapshot state choices '
                 "scores scores_total author }}"
    }
    response = requests.get(url, query)
    return response.json()


def get_today():
    now = datetime.now()
    url = f"http://history.muffinlabs.com/date/{now.month}/{now.day}"
    response = requests.get(url)
    return response.json()


def get_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    data = response.json()

    definition = None
    audio_url = None

    if data and isinstance(data, list):
        meanings = data[0].get("meanings", [])
        if meanings:
            for meaning in meanings:
                definitions = meaning.get("definitions", [])
                if definitions:
                    definition = definitions[0].get("definition")
                    break

        phonetics = data[0].get("phonetics", [])
        if phonetics:
            first_phonetic = phonetics[0]
            audio_url = first_phonetic.get("audio")

    return definition, audio_url