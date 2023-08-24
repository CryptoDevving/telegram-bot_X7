import os
import csv
import random
import time as t
from typing import Tuple
from datetime import datetime, timedelta

import tweepy
import base64
import requests

from data import ca
from moralis import evm_api
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()

bsc = os.getenv("BSC")
ether = os.getenv("ETHER")
poly = os.getenv("POLY")
opti = os.getenv("OPTI")
arb = os.getenv("ARB")
base = os.getenv("BASE")
COINGECKO_URL = "https://api.coingecko.com/api/v3"


class ChainInfo:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key


chains_info = {
    "eth": ChainInfo(
        "https://api.etherscan.io/api",
        ether,
    ),
    "bsc": ChainInfo("https://api.bscscan.com/api", bsc),
    "arb": ChainInfo("https://api.arbiscan.io/api", arb),
    "opti": ChainInfo("https://api-optimistic.etherscan.io/api", opti),
    "poly": ChainInfo("https://api.polygonscan.com/api", poly),
    "base": ChainInfo("https://api.basescan.org/api", base),
}


# SCAN


def get_abi(contract: str, chain: str) -> str:
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"][0]["ABI"]


def get_block(chain: str, time: "int") -> str:
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=block&action=getblocknobytime&timestamp={time}&closest=before{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_daily_tx_count(contract: str, chain: str,) -> int:
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    yesterday = int(t.time()) - 86400
    block_yesterday = get_block(chain, yesterday)
    block_now = get_block(chain, int(t.time()))
    tx_url = f"{chain_info.url}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
    tx_response = requests.get(tx_url)
    tx_data = tx_response.json()
    tx_entry_count = len(tx_data['result']) if 'result' in tx_data else 0
    internal_tx_url = f"{chain_info.url}?module=account&action=txlist&address={contract}&startblock={block_yesterday}&endblock={block_now}&page=1&offset=1000&sort=asc{chain_info.key}"
    internal_tx_response = requests.get(internal_tx_url)
    internal_tx_data = internal_tx_response.json()
    internal_tx_entry_count = len(internal_tx_data['result']) if 'result' in internal_tx_data else 0
    entry_count = tx_entry_count + internal_tx_entry_count 
    return entry_count


def get_gas(chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=gastracker&action=gasoracle{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_native_balance(wallet, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=balancemulti&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    amount_raw = float(data["result"][0]["balance"])
    return f"{amount_raw / 10 ** 18}"


def get_native_price(token):
    tokens_info = {
        "eth": {
            "url": "https://api.etherscan.io/api?module=stats&action=ethprice",
            "key": ether,
            "field": "ethusd",
        },
        "bnb": {
            "url": "https://api.bscscan.com/api?module=stats&action=bnbprice",
            "key": bsc,
            "field": "ethusd",
        },
        "matic": {
            "url": "https://api.polygonscan.com/api?module=stats&action=maticprice",
            "key": poly,
            "field": "maticusd",
        },
    }
    if token not in tokens_info:
        raise ValueError(f"Invalid token: {token}")
    url = f"{tokens_info[token]['url']}&{tokens_info[token]['key']}"
    response = requests.get(url)
    data = response.json()
    return float(data["result"][tokens_info[token]["field"]])


def get_pool_liq_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.Session().get(url)
    data = response.json()
    return int(data["result"] or 0)


def get_stables_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return int(data["result"][:-6])


def get_supply(token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=stats&action=tokensupply&contractaddress={token}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_token_balance(wallet, token, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={token}&address={wallet}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return int(data["result"][:-18])


def get_tx_from_hash(tx, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=proxy&action=eth_getTransactionByHash&txhash={tx}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=txlist&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_internal_tx(address, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=txlistinternal&sort=desc&address={address}{chain_info.key}"
    response = requests.get(url)
    return response.json()


def get_verified(contract, chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=contract&action=getsourcecode&address={contract}{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    return "Yes" if "SourceCode" in data["result"][0] else "No"


def get_x7r_supply(chain):
    if chain not in chains_info:
        raise ValueError(f"Invalid chain: {chain}")
    chain_info = chains_info[chain]
    url = f"{chain_info.url}?module=account&action=tokenbalance&contractaddress={ca.x7r}&address={ca.dead}&tag=latest{chain_info.key}"
    response = requests.get(url)
    data = response.json()
    supply = ca.supply - int(data["result"][:-18])
    return supply

# CG


def get_ath(token):
    url = (
        f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data="
        "true&community_data=false&developer_data=false&sparkline=false"
    )
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    return (
        value["ath"]["usd"],
        value["ath_change_percentage"]["usd"],
        value["ath_date"]["usd"],
    )


def get_cg_price(token):
    coingecko = CoinGeckoAPI()
    return coingecko.get_price(
        ids=token,
        vs_currencies="usd",
        include_24hr_change="true",
        include_24hr_vol="true",
        include_market_cap="true",
    )


def get_cg_search(token):
    url = "https://api.coingecko.com/api/v3/search?query=" + token
    response = requests.get(url)
    return response.json()


def get_mcap(token):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd&include_market_cap=true"
    response = requests.get(url)
    data = response.json()
    return data[token]["usd_market_cap"]


# ALCHEMY


def get_maxi_holdings(wallet):
    url = f'https://eth-mainnet.g.alchemy.com/nft/v2/{os.getenv("ALCHEMY_ETH")}/getNFTs?owner={wallet}&contractAddresses[]={ca.borrow}&contractAddresses[]={ca.liq}&contractAddresses[]={ca.dex}&contractAddresses[]={ca.eco}&withMetadata=false&pageSize=100'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    total_count = response_data.get("totalCount")
    return total_count


def get_pioneer_holdings(wallet):
    url = f'https://eth-mainnet.g.alchemy.com/nft/v2/{os.getenv("ALCHEMY_ETH")}/getNFTs?owner={wallet}&contractAddresses[]={ca.pioneer}&withMetadata=false&pageSize=100'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    response_data = response.json()
    total_count = response_data.get("totalCount")
    return total_count


# MORALIS


def get_liquidity(pair, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    return evm_api.defi.get_pair_reserves(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "pair_address": pair},
    )


def get_nft_holder_list(nft, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    return evm_api.nft.get_nft_owners(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"chain": chain, "format": "decimal", "address": nft},
    )


def get_price(token, chain):
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    api_key = os.getenv("MORALIS_API_KEY")
    result = evm_api.token.get_token_price(
        api_key=api_key,
        params={"address": token, "chain": chain},
    )
    return result["usdPrice"]
    

def get_token_data(token: str, chain: str) -> dict:
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result


def get_token_name(token: str, chain: str) -> Tuple[str, str]:
    chain_mappings = {
        "eth": "eth",
        "arb": "arbitrum",
        "poly": "polygon",
        "bsc": "bsc",
        "opti": "optimism",
    }
    if chain in chain_mappings:
        chain = chain_mappings[chain]
    result = evm_api.token.get_token_metadata(
        api_key=os.getenv("MORALIS_API_KEY"),
        params={"addresses": [f"{token}"], "chain": chain},
    )
    return result[0]["name"], result[0]["symbol"]


# BLOCKSPAN


def get_nft_holder_count(nft, chain):
    try:
        chain_mappings = {
            "eth": "eth-main",
            "arb": "arbitrum-main",
            "poly": "poly-main",
            "bsc": "bsc-main",
            "opti": "optimism-main",
            "base": "base-main",
        }
        if chain in chain_mappings:
            chain = chain_mappings[chain]
        url = f"https://api.blockspan.com/v1/collections/contract/{nft}?chain={chain}"
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
            },
        )
        data = response.json()
        return data.get("total_tokens", "0")
    except Exception as e:
        return 0


def get_nft_floor(nft, chain):
    try:
        chain_mappings = {
            "eth": ("eth-main", "ETH"),
            "arb": ("arbitrum-main", "ETH"),
            "poly": ("poly-main", "MATIC"),
            "bsc": ("bsc-main", "BNB"),
            "opti": (
                "optimism-main",
                "ETH",
            ),
            "base": ("base-main"),
        }
        if chain in chain_mappings:
            chain, chain_native = chain_mappings[chain]
        url = f"https://api.blockspan.com/v1/collections/contract/{nft}?chain={chain}"
        response = requests.get(
            url,
            headers={
                "accept": "application/json",
                "X-API-KEY": os.getenv("BLOCKSPAN_API_KEY"),
            },
        )
        data = response.json()
        exchange_data = data.get("exchange_data")
        if exchange_data is not None:
            for item in exchange_data:
                stats = item.get("stats")
                if stats is not None:
                    floor_price = stats.get("floor_price")
                    if floor_price is not None:
                        return floor_price
            return "N/A"
        else:
            return "N/A"
    except Exception as e:
        return "N/A"


# OPENSEA

def get_os_nft_collection(slug):
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    response = requests.get(url, headers={"X-API-KEY": os.getenv("OPENSEA_API_KEY")})
    data = response.json()
    return data


def get_os_nft_id(nft, id):
    url = f"https://api.opensea.io/v2/chain/ethereum/contract/{nft}/nfts/{id}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv("OPENSEA_API_KEY")
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


## DEFINED


def get_price_change(address):
    url = "https://api.defined.fi"

    headers = {
        "content_type": "application/json",
        "x-api-key": os.getenv("DEFINED_API_KEY")
    }

    current_timestamp = int(datetime.now().timestamp()) - 300
    one_hour_ago_timestamp = int((datetime.now() - timedelta(hours=1)).timestamp())
    twenty_four_hours_ago_timestamp = int((datetime.now() - timedelta(hours=24)).timestamp())
    seven_days_ago_timestamp = int((datetime.now() - timedelta(days=7)).timestamp())

    pricechange = f"""query {{
        getTokenPrices(
            inputs: [
                {{ 
                    address: "{address}"
                    networkId: 1
                    timestamp: {current_timestamp}
                }}
                {{ 
                    address: "{address}"
                    networkId: 1
                    timestamp: {one_hour_ago_timestamp}
                }}
                {{ 
                    address: "{address}"
                    networkId: 1
                    timestamp: {twenty_four_hours_ago_timestamp}
                }}
                {{ 
                    address: "{address}"
                    networkId: 1
                    timestamp: {seven_days_ago_timestamp}
                }}
            ]
        ) {{
            priceUsd
        }}
    }}"""

    response = requests.post(url, headers=headers, json={"query": pricechange})
    data = response.json()
    current_price = data["data"]["getTokenPrices"][0]["priceUsd"]
    one_hour_ago_price = data["data"]["getTokenPrices"][1]["priceUsd"]
    twenty_four_hours_ago_price = data["data"]["getTokenPrices"][2]["priceUsd"]
    seven_days_ago_price = data["data"]["getTokenPrices"][3]["priceUsd"]

    one_hour_change = round(((current_price - one_hour_ago_price) / one_hour_ago_price) * 100, 2)
    twenty_four_hours_change = round(((current_price - twenty_four_hours_ago_price) / twenty_four_hours_ago_price) * 100, 2)
    seven_days_change = round(((current_price - seven_days_ago_price) / seven_days_ago_price) * 100, 2)

    result = f"1H Change: {one_hour_change}%\n24H Change: {twenty_four_hours_change}%\n7D Change: {seven_days_change}%"

    return result



def get_token_image(token):
    url = "https://api.defined.fi"

    headers = {
        "content_type": "application/json",
        "x-api-key": os.getenv("DEFINED_API_KEY")
    }

    image = f'''
        query {{
            getTokenInfo(address:"{token}", networkId:1) {{
                imageLargeUrl
            }}
        }}
    '''

    
    response = requests.post(url, headers=headers, json={"query": image})
    data = response.json()
    image_url = data['data']['getTokenInfo']['imageLargeUrl']
    return image_url


def get_volume(pair):
    url = "https://api.defined.fi"

    headers = {
        "content_type": "application/json",
        "x-api-key": os.getenv("DEFINED_API_KEY")
    }

    volume = f'''
        query {{
        getDetailedPairStats(pairAddress: "{pair}", networkId: 1, bucketCount: 1, tokenOfInterest: token1) {{
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

    response = requests.post(url, headers=headers, json={"query": volume})
    data = response.json()

    current_value = data['data']['getDetailedPairStats']['stats_day1']['statsUsd']['volume']['currentValue']
    return current_value


# OTHER


def datetime_to_timestamp(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        timestamp = datetime_obj.timestamp()
        return timestamp
    except ValueError:
        return "Invalid datetime format. Please use YYYY-MM-DD HH:MM."


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


def get_giveaway_entries():
    with open("logs/entries.csv", "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        column_data = []
        for row in csv_reader:
            if len(row) > 0 and row[0] != "":
                column_data.append(row[0])
    return [entry[-5:] for entry in column_data]


def get_pair_entries(ticker):
    data = []
    with open('logs/tokens.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    csv_data = data
    matching_data = []
    for row in csv_data:
        if row[0].lower() == ticker.lower():
            matching_data.append({
                'ticker': row[0],
                'pair': row[1],
                'ca': row[2],
                'chain': row[3],
                'image_url': row[4]
            })
    
    return  matching_data


def get_holders(token):
    base_url = "https://api.ethplorer.io/getTokenInfo"
    url = f"{base_url}/{token}{os.getenv('ETHPLORER_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    return data.get("holdersCount")



def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    data = response.json()
    quote = random.choice(data)
    quote_text = quote["text"]
    quote_author = quote["author"]
    if quote_author.endswith(", type.fit"):
        quote_author = quote_author[:-10].strip()

    return f'`"{quote_text}"\n\n-{quote_author}`'


def get_random_pioneer_number():
    return f"{random.randint(1, 4480)}".zfill(4)


def get_scan(token: str, chain: str) -> dict:
    chains = {"eth": 1, "bsc": 56, "arb": 42161, "opti": 10, "poly": 137}
    chain_number = chains.get(chain)
    if not chain_number:
        raise ValueError(f"{chain} is not a valid chain")
    url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_number}?contract_addresses={token}"
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


def get_split(eth_value):
    founding_dev_percentage = 0.07
    pioneer_reward_pool_percentage = 0.06
    community_multisig_percentage = 0.32
    developers_multisig_percentage = 0.13
    x7r_percentage = 0.10
    x7dao_percentage = 0.10
    x7_constellations_percentage = 0.10
    lending_pool_percentage = 0.20
    treasury_percentage = 0.50
    treasury_share = eth_value * treasury_percentage
    founding_dev_share = treasury_share * founding_dev_percentage * 7
    pioneer_reward_pool_share = treasury_share * pioneer_reward_pool_percentage
    community_multisig_share = treasury_share * community_multisig_percentage
    developers_multisig_share = treasury_share * developers_multisig_percentage
    x7r_share = eth_value * x7r_percentage
    x7dao_share = eth_value * x7dao_percentage
    x7_constellations_share = eth_value * x7_constellations_percentage
    lending_pool_share = eth_value * lending_pool_percentage

    return {
        "X7R": x7r_share,
        "X7DAO": x7dao_share,
        "X7 Constellations": x7_constellations_share,
        "Lending Pool": lending_pool_share,
        "Treasury": treasury_share,
        "Founding X7 Devs Total": founding_dev_share,
        "Pioneer Reward Pool": pioneer_reward_pool_share,
        "Community Multi Sig": community_multisig_share,
        "Developers Multi Sig": developers_multisig_share,
    }


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


def push_github(location, message):
    headers = {
        'Authorization': f'Bearer {os.getenv("GITHUB_PAT")}'
    }
    response = requests.get(
        f'https://api.github.com/repos/x7finance/telegram-bot/contents/{location}',
        headers=headers
    )

    if response.status_code == 200:
        content = response.json()
        sha = content['sha']

        with open(location, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        response = requests.put(
            f'https://api.github.com/repos/x7finance/telegram-bot/contents/{location}',
            headers=headers,
            json={
                'message': message,
                'content': encoded_content,
                'sha': sha
            }
        )


# TWITTER


auth = tweepy.OAuthHandler(os.getenv("TWITTER_API"), os.getenv("TWITTER_API_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS"), os.getenv("TWITTER_ACCESS_SECRET"))
twitter = tweepy.API(auth)
twitter_v2 = tweepy.Client(os.getenv("TWITTER_BEARER"))
