# MAPPINGS

import os
from constants import ca, urls
import media
from web3 import Web3
import random


DEFAULT_CHAIN = "eth"


class ChainInfo:
    def __init__(self, name: str, scan_name: str, id: str,  token: str, logo: str, xchange: str, scan_token: str, scan_address: str, scan_tx: str, gas: str, dext: str, opensea: str, blockspan: str, w3: str, api: str, key: str, com_multi: str, dev_multi: str, pairs: list):
        self.name = name
        self.scan_name = scan_name
        self.id = id
        self.token = token
        self.logo = logo
        self.xchange = xchange
        self.scan_token = scan_token
        self.scan_address = scan_address
        self.scan_tx = scan_tx
        self.gas = gas
        self.dext = dext
        self.opensea = opensea
        self.blockspan = blockspan
        self.w3 = w3
        self.api = api
        self.key = key
        self.com_multi = com_multi
        self.dev_multi = dev_multi
        self.pairs = pairs


CHAINS = {
    "eth": ChainInfo(
        "ETH",
        "Etherscan",
        "1",
        "eth",
        media.ETH_LOGO,
        urls.XCHANGE_BUY_ETH,
        urls.ETHER_TOKEN,
        urls.ETHER_ADDRESS,
        urls.ETHER_TX,
        urls.ETHER_GAS,
        "ether",
        "",
        "eth-main",
        urls.ETH_RPC,
        urls.ETHER_API,
        os.getenv('ETHER'),
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
    "base": ChainInfo(
        "Base",
        "Basescan",
        "8453",
        "eth",
        media.BASE_LOGO,
        urls.XCHANGE_BUY_BASE,
        urls.BASE_TOKEN,
        urls.BASE_ADDRESS,
        urls.BASE_TX,
        urls.ETHER_GAS,
        "base",
        "-base",
        "base-main",
        urls.BASE_RPC,
        urls.BASE_API,
        os.getenv('BASE'),
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
    "bsc": ChainInfo(
        "BSC",
        "BSCscan",
        "56",
        "bnb",
        media.BSC_LOGO,
        urls.XCHANGE_BUY_BSC,
        urls.BSC_TOKEN,
        urls.BSC_ADDRESS,
        urls.BSC_TX,
        urls.BSC_GAS,
        "bsc",
        "-binance",
        "",
        urls.BSC_RPC,
        urls.BSC_API,
        os.getenv('BSC'),
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
        "Arbitrum",
        "Arbiscan",
        "42161",
        "eth",
        media.ARB_LOGO,
        urls.XCHANGE_BUY_ARB,
        urls.ARB_TOKEN,
        urls.ARB_ADDRESS,
        urls.ARB_TX,
        urls.ETHER_GAS,
        "arbitrum",
        "-arbitrum",
        "arbitrum-main",
        urls.ARB_RPC,
        urls.ARB_API,
        os.getenv('ARB'),
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
        "Optimism",
        "Optimisticscan",
        "10",
        "eth",
        media.OPTI_LOGO,
        urls.XCHANGE_BUY_OPTI,
        urls.OPTI_TOKEN,
        urls.OPTI_ADDRESS,
        urls.OPTI_TX,
        urls.ETHER_GAS,
        "optimism",
        "-optimism",
        "optimism-main",
        urls.OPTI_RPC,
        urls.OPTI_API,
        os.getenv('OPTI'),
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
        "Polygon",
        "Polygonscan",
        "137",
        "matic",
        media.POLY_LOGO,
        urls.XCHANGE_BUY_POLY,
        urls.POLY_TOKEN,
        urls.POLY_ADDRESS,
        urls.POLY_TX,
        urls.POLY_GAS,
        "polygon",
        "-polygon",
        "poly-main",
        urls.POLY_RPC,
        urls.POLY_API,
        os.getenv('POLY'),
        ca.COM_MULTI_POLY,
        ca.DEV_MULTI_POLY,
        [ca.X7R_PAIR_POLY,
        ca.X7DAO_PAIR_POLY,
        ca.X7101_PAIR_POLY,
        ca.X7102_PAIR_POLY,
        ca.X7103_PAIR_POLY,
        ca.X7104_PAIR_POLY,
        ca.X7105_PAIR_POLY]
    )
}
