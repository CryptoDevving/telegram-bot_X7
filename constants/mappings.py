import os
from constants import url, ca
import media

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
key_base = os.getenv("BASE")


class TokensInfo:
    def __init__(
        self, name: str, ca: str, pair: str, chain: str, logo: str = ""
    ):
        self.name = name
        self.ca = ca
        self.pair = pair
        self.chain = chain
        self.logo = logo


class ChainInfo:
    def __init__(self, name: str, token: str, logo: str, xchange: str, scan_token: str, scan_address: str, scan_tx: str, gas: str, dext: str, opensea: str, nft_holders: str, w3: str, api: str, key: str, com_multi: str, dev_multi: str, pairs: list):
        self.name = name
        self.token = token
        self.logo = logo
        self.xchange = xchange
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.gas = gas
        self.dext = dext
        self.opensea = opensea
        self.nft_holders = nft_holders
        self.w3 = w3
        self.api = api
        self.key = key
        self.com_multi = com_multi
        self.dev_multi = dev_multi
        self.pairs = pairs


CHAINS = {
    "eth": ChainInfo(
        "(ETH)",
        "eth",
        media.ETH_LOGO,
        url.XCHANGE_BUY_ETH,
        url.ETHER_TOKEN,
        url.ETHER_ADDRESS,
        url.ETHER_TX,
        url.ETHER_GAS,
        url.DEX_TOOLS_ETH,
        "",
        "eth-main",
        Web3(Web3.HTTPProvider(f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_eth}")),
        "https://api.etherscan.io/api",
        key_ether,
        ca.COM_MULTI_ETH,
        ca.DEV_MULTI_ETH,
        [ca.X7R_PAIR_ETH,
        ca.X7DAO_PAIR_ETH,
        ca.X7101_PAIR_ETH,
        ca.X7102_PAIR_ETH,
        ca.X7103_PAIR_ETH,
        ca.X7104_PAIR_ETH,
        ca.X7105_PAIR_ETH]
    ),
    "bsc": ChainInfo(
        "(BSC)",
        "bnb",
        media.BSC_LOGO,
        url.XCHANGE_BUY_BSC,
        url.BSC_TOKEN,
        url.BSC_ADDRESS,
        url.BSC_TX,
        url.BSC_GAS,
        url.DEX_TOOLS_BSC,
        "-binance",
        "",
        Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/")),
        "https://api.bscscan.com/api",
        key_bsc,
        ca.COM_MULTI_BSC,
        ca.DEV_MULTI_BSC,
        [ca.X7R_PAIR_BSC,
        ca.X7DAO_PAIR_BSC,
        ca.X7101_PAIR_BSC,
        ca.X7102_PAIR_BSC,
        ca.X7103_PAIR_BSC,
        ca.X7104_PAIR_BSC,
        ca.X7105_PAIR_BSC]
    ),
    "arb": ChainInfo(
        "(Arbitrum)",
        "eth",
        media.ARB_LOGO,
        url.XCHANGE_BUY_ARB,
        url.ARB_TOKEN,
        url.ARB_ADDRESS,
        url.ARB_TX,
        url.ETHER_GAS,
        url.DEX_TOOLS_ARB,
        "-arbitrum",
        "arbitrum-main",
        Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{alchemy_arb}")),
        "https://api.arbiscan.io/api",
        key_arb,
        ca.COM_MULTI_ARB,
        ca.DEV_MULTI_ARB,
        [ca.X7R_PAIR_ARB,
        ca.X7DAO_PAIR_ARB,
        ca.X7101_PAIR_ARB,
        ca.X7102_PAIR_ARB,
        ca.X7103_PAIR_ARB,
        ca.X7104_PAIR_ARB,
        ca.X7105_PAIR_ARB,]
        
    ),
    "opti": ChainInfo(
        "(Optimism)",
        "eth",
        media.OPTI_LOGO,
        url.XCHANGE_BUY_OPTI,
        url.OPTI_TOKEN,
        url.OPTI_ADDRESS,
        url.OPTI_TX,
        url.ETHER_GAS,
        url.DEX_TOOLS_OPTI,
        "-optimism",
        "optimism-main",
        Web3(Web3.HTTPProvider(f"https://opt-mainnet.g.alchemy.com/v2/{alchemy_opti}")),
        "https://api-optimistic.etherscan.io/api",
        key_opti,
        ca.COM_MULTI_OPTI,
        ca.DEV_MULTI_OPTI,
        [ca.X7R_PAIR_OPTI,
        ca.X7DAO_PAIR_OPTI,
        ca.X7101_PAIR_OPTI,
        ca.X7102_PAIR_OPTI,
        ca.X7103_PAIR_OPTI,
        ca.X7104_PAIR_OPTI,
        ca.X7105_PAIR_OPTI]
    ),
    "poly": ChainInfo(
        "(Polygon)",
        "matic",
        media.POLY_LOGO,
        url.XCHANGE_BUY_POLY,
        url.POLY_TOKEN,
        url.POLY_ADDRESS,
        url.POLY_TX,
        url.POLY_GAS,
        url.DEX_TOOLS_POLY,
        "-polygon",
        "poly-main",
        Web3(Web3.HTTPProvider(f"https://polygon-mainnet.g.alchemy.com/v2/{alchemy_poly}")),
        "https://api.polygonscan.com/api",
        key_poly,
        ca.COM_MULTI_POLY,
        ca.DEV_MULTI_POLY,
        [ca.X7R_PAIR_POLY,
        ca.X7DAO_PAIR_POLY,
        ca.X7101_PAIR_POLY,
        ca.X7102_PAIR_POLY,
        ca.X7103_PAIR_POLY,
        ca.X7104_PAIR_POLY,
        ca.X7105_PAIR_POLY]
    ),
    "base": ChainInfo(
        "(Base)",
        "eth",
        media.BASE_LOGO,
        url.XCHANGE_BUY_BASE,
        url.BASE_TOKEN,
        url.BASE_ADDRESS,
        url.BASE_TX,
        url.ETHER_GAS,
        url.DEX_TOOLS_BASE,
        "-base",
        "base-main",
        Web3(Web3.HTTPProvider(f"https://mainnet.base.org")),
        "https://api.basescan.org/api",
        key_base,
        ca.COM_MULTI_BASE,
        ca.DEV_MULTI_BASE,
        [ca.X7R_PAIR_BASE,
        ca.X7DAO_PAIR_BASE,
        ca.X7101_PAIR_BASE,
        ca.X7102_PAIR_BASE,
        ca.X7103_PAIR_BASE,
        ca.X7104_PAIR_BASE,
        ca.X7105_PAIR_BASE]
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


ALCHEMY_CHAINS = {
    "eth": f"https://eth-mainnet.g.alchemy.com/nft/v2/{os.getenv('ALCHEMY_ETH')}",
    "arb": f"https://arb-mainnet.g.alchemy.com/nft/v2/{os.getenv('ALCHEMY_ARB')}",
    "poly": f"https://polygon-mainnet.g.alchemy.com/nft/v2/{os.getenv('ALCHEMY_POLY')}",
    "bsc": "bsc",
    "opti": f"https://opt-mainnet.g.alchemy.com/nft/v2/{os.getenv('ALCHEMY_OPTI')}",
    "base": "base",
}


BLOCKSPAN_CHAINS = {
    "eth": "eth-main",
    "arb": "arbitrum-main",
    "poly": "poly-main",
    "bsc": "bsc-main",
    "opti": "optimism-main",
    "base": "base-main",
}


DEFINED_CHAINS = {
    "eth": "1",
    "arb": "42161",
    "poly": "137",
    "bsc": "46",
    "opti": "10",
    "base": "8453",
}


DEX_TOOLS_CHAINS = {
    "eth": "ether",
    "arb": "arbitrum",
    "poly": "polygon",
    "bsc": "bsc",
    "opti": "optimism",
    "base": "base",
}


MORALIS_CHAINS = {
    "eth": "eth",
    "arb": "arbitrum",
    "poly": "polygon",
    "bsc": "bsc",
    "opti": "optimism",
    "base": "base",
}
