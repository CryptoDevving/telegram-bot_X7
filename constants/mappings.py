import os
from constants import url, ca

from web3 import Web3


alchemy_eth = os.getenv("ALCHEMY_ETH")
alchemy_arb = os.getenv("ALCHEMY_ARB")
alchemy_poly = os.getenv("ALCHEMY_POLY")
alchemy_opti = os.getenv("ALCHEMY_OPTI")
key_bsc = os.getenv("BSC")
key_arb = os.getenv("ARB")
key_poly = os.getenv("POLY")
key_opti = os.getenv("OPTI")
key_ether = os.getenv("ETHER")


class TokensInfo:
    def __init__(
        self, name: str, ca: str, pair: str, chain: str, logo: str = ""
    ):
        self.name = name
        self.ca = ca
        self.pair = pair
        self.chain = chain
        self.logo = logo


class UrlInfo:
    def __init__(self, scan: str, dext: str, w3: str, api: str, key: str):
        self.scan = scan
        self.dext = dext
        self.w3 = w3
        self.api = api
        self.key = key


CHAINS = {
    "eth": UrlInfo(
        "https://etherscan.io/token/",
        "https://www.dextools.io/app/en/ether/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_eth}")),
        "https://api.etherscan.io/api",
        key_ether,
    ),
    "bsc": UrlInfo(
        "https://bscscan.com/token/",
        "https://www.dextools.io/app/en/bnb/pair-explorer/",
        Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/")),
        "https://api.bscscan.com/api",
        key_bsc,
    ),
    "arb": UrlInfo(
        "https://arbiscan.io/token/",
        "https://www.dextools.io/app/arbitrum/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_arb}")),
        "https://api.arbiscan.io/api",
        key_arb,
    ),
    "opti": UrlInfo(
        "https://optimistic.etherscan.io/token/",
        "https://www.dextools.io/app/optimism/pair-explorer/",
        Web3(Web3.HTTPProvider(f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_opti}")),
        "https://api-optimistic.etherscan.io/api",
        key_opti,
    ),
    "poly": UrlInfo(
        "https://polygonscan.com/token/",
        "https://www.dextools.io/app/polygon/pair-explorer/",
        Web3(
            Web3.HTTPProvider(
                f"https://polygon-mainnet.g.alchemy.com/v2/{alchemy_poly}"
            )
        ),
        "https://api.polygonscan.com/api",
        key_poly,
    ),
}

X7D = {
        "eth": (
            "(ETH)",
            url.ETHER_ADDRESS,
            "eth",    
        ),
        "arb": (
            "(ARB)",
            url.ARB_ADDRESS,
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_ADDRESS,
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_ADDRESS,
            "bnb",
        ),
        "opti": (
            "(OPTI)",
            url.OPTI_ADDRESS,
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_ADDRESS,
            "eth",
        ),
    }


X7DAO = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7DAO_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7DAO_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7DAO_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7DAO_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7DAO_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7DAO_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }


X7R = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7R_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7R_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7R_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7R_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7R_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7R_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }


X7101 = {
    "eth": (
        "(ETH)",
        url.ETHER_TOKEN,
        url.DEX_TOOLS_ETH,
        ca.X7101_PAIR_ETH,
        url.XCHANGE_BUY_ETH,
        "Etherscan",
        "eth",
    ),
    "arb": (
        "(ARB)",
        url.ARB_TOKEN,
        url.DEX_TOOLS_ARB,
        ca.X7101_PAIR_ARB,
        url.XCHANGE_BUY_ARB,
        "Arbscan",
        "eth",
    ),
    "poly": (
        "(POLYGON)",
        url.POLY_TOKEN,
        url.DEX_TOOLS_POLY,
        ca.X7101_PAIR_POLY,
        url.XCHANGE_BUY_POLY,
        "Polygonscan",
        "matic",
    ),
    "bsc": (
        "(BSC)",
        url.BSC_TOKEN,
        url.DEX_TOOLS_BSC,
        ca.X7101_PAIR_BSC,
        url.XCHANGE_BUY_BSC,
        "BSCscan",
        "bnb",
    ),
    "opti": (
        "(OP)",
        url.OPTI_TOKEN,
        url.DEX_TOOLS_OPTI,
        ca.X7101_PAIR_OPTI,
        url.XCHANGE_BUY_OPTI,
        "Optimismscan",
        "eth",
    ),
    "base": (
        "(BASE)",
        url.BASE_TOKEN,
        url.DEX_TOOLS_BASE,
        ca.X7101_PAIR_BASE,
        url.XCHANGE_BUY_BASE,
        "Basescan",
        "eth",
    ),
}


X7102 = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7102_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7102_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7102_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7102_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7102_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7102_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }


X7103 = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7103_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7103_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7103_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7103_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7103_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7103_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }


X7104 = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7104_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7104_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7104_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7104_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7104_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7104_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }


X7105 = {
        "eth": (
            "(ETH)",
            url.ETHER_TOKEN,
            url.DEX_TOOLS_ETH,
            ca.X7105_PAIR_ETH,
            url.XCHANGE_BUY_ETH,
            "Etherscan",
            "eth",
        ),
        "arb": (
            "(ARB)",
            url.ARB_TOKEN,
            url.DEX_TOOLS_ARB,
            ca.X7105_PAIR_ARB,
            url.XCHANGE_BUY_ARB,
            "Arbscan",
            "eth",
        ),
        "poly": (
            "(POLYGON)",
            url.POLY_TOKEN,
            url.DEX_TOOLS_POLY,
            ca.X7105_PAIR_POLY,
            url.XCHANGE_BUY_POLY,
            "Polygonscan",
            "matic",
        ),
        "bsc": (
            "(BSC)",
            url.BSC_TOKEN,
            url.DEX_TOOLS_BSC,
            ca.X7105_PAIR_BSC,
            url.XCHANGE_BUY_BSC,
            "BSCscan",
            "bnb",
        ),
        "opti": (
            "(OP)",
            url.OPTI_TOKEN,
            url.DEX_TOOLS_OPTI,
            ca.X7105_PAIR_OPTI,
            url.XCHANGE_BUY_OPTI,
            "Optimismscan",
            "eth",
        ),
        "base": (
            "(BASE)",
            url.BASE_TOKEN,
            url.DEX_TOOLS_BASE,
            ca.X7105_PAIR_BASE,
            url.XCHANGE_BUY_BASE,
            "Basescan",
            "eth",
        ),
    }

PAIRS = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hasMinimums","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"gasAmount","type":"uint256"}],"name":"mustBurn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint112","name":"minimumAmount","type":"uint112"}],"name":"setMinimumBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"feeAmountOverride","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swapWithDiscount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"sync","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"gasAmountToken0","type":"uint256"},{"internalType":"uint256","name":"gasAmountToken1","type":"uint256"}],"name":"syncSafe","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"tokenMinimumBalance","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint112","name":"amount","type":"uint112"}],"name":"withdrawTokensAgainstMinimumBalance","outputs":[{"internalType":"uint112","name":"","type":"uint112"}],"stateMutability":"nonpayable","type":"function"}]'


