# NFTS

from constants import ca
from hooks import api


def DATA():
    return {
        "eth": {
            "eco": api.get_nft_data(ca.ECO, "eth"),
            "liq": api.get_nft_data(ca.LIQ, "eth"),
            "dex": api.get_nft_data(ca.DEX, "eth"),
            "borrow": api.get_nft_data(ca.BORROW, "eth"),
            "magister": api.get_nft_data(ca.MAGISTER, "eth"),
        },
        "arb": {
            "eco": api.get_nft_data(ca.ECO, "arb"),
            "liq": api.get_nft_data(ca.LIQ, "arb"),
            "dex": api.get_nft_data(ca.DEX, "arb"),
            "borrow": api.get_nft_data(ca.BORROW, "arb"),
            "magister": api.get_nft_data(ca.MAGISTER, "arb"),
        },
        "opti": {
            "eco": api.get_nft_data(ca.ECO, "opti"),
            "borrow": api.get_nft_data(ca.BORROW, "opti"),
            "dex": api.get_nft_data(ca.DEX, "opti"),
            "liq": api.get_nft_data(ca.LIQ, "opti"),
            "magister": api.get_nft_data(ca.MAGISTER, "opti"),
        },
        "poly": {
            "eco": api.get_nft_data(ca.ECO, "poly"),
            "borrow": api.get_nft_data(ca.BORROW, "poly"),
            "dex": api.get_nft_data(ca.DEX, "poly"),
            "liq": api.get_nft_data(ca.LIQ, "poly"),
            "magister": api.get_nft_data(ca.MAGISTER, "poly"),
        },
        "bsc": {
            "eco": api.get_nft_data(ca.ECO, "bsc"),
            "borrow": api.get_nft_data(ca.BORROW, "bsc"),
            "dex": api.get_nft_data(ca.DEX, "bsc"),
            "liq": api.get_nft_data(ca.LIQ, "bsc"),
            "magister": api.get_nft_data(ca.MAGISTER, "bsc"),
        },
        "base": {
            "eco": api.get_nft_data(ca.ECO, "base"),
            "liq": api.get_nft_data(ca.LIQ, "base"),
            "dex": api.get_nft_data(ca.DEX, "base"),
            "borrow": api.get_nft_data(ca.BORROW, "base"),
            "magister": api.get_nft_data(ca.MAGISTER, "base"),
        },
    }


def DISCOUNTS():
    return {
        "eco": {
            "X7R": 10,
            "X7DAO": 10,
            "X7100": 25,
        },
        "liq": {
            "X7R": 25,
            "X7DAO": 15,
            "X7100": 50,
        },
        "dex": {"LP Fee discounts while trading on Xchange"},
        "borrow": {"Fee discounts for borrowing funds for ILL on Xchange"},
        "magister": {
            "X7R": 25,
            "X7100": 25,
        },
    }


def MINT_PRICES():
    return {
        "eth": {
            "eco": "0.3 ETH - 500 Supply",
            "liq": "0.75 ETH - 250 Supply",
            "dex": "1.5 ETH - 150 Supply",
            "borrow": "2 ETH - 100 Supply",
            "magister": "50 ETH - 49 Supply",
        },
        "arb": {
            "eco": "0.3 ETH - 500 Supply",
            "liq": "0.75 ETH - 250 Supply",
            "dex": "1.5 ETH - 150 Supply",
            "borrow": "2 ETH - 100 Supply",
            "magister": "50 ETH - 49 Supply",
        },
        "opti": {
            "eco": "0.3 ETH - 500 Supply",
            "liq": "0.75 ETH - 250 Supply",
            "dex": "1.5 ETH - 150 Supply",
            "borrow": "2 ETH - 100 Supply",
            "magister": "50 ETH - 49 Supply",
        },
        "bsc": {
            "eco": "1.5 BNB - 500 Supply",
            "liq": "3.75 BNB - 250 Supply",
            "dex": "7.5 BNB - 150 Supply",
            "borrow": "10 BNB - 100 Supply",
            "magister": "150 BNB - 49 Supply",
        },
        "poly": {
            "eco": "390 MATIC - 500 Supply",
            "liq": "975 MATIC - 250 Supply",
            "dex": "1950 MATIC - 150 Supply",
            "borrow": "2600 MATIC - 100 Supply",
            "magister": "45000 MATIC - 49 Supply",
        },
        "base": {
            "eco": "0.3 ETH - 500 Supply",
            "liq": "0.75 ETH - 250 Supply",
            "dex": "1.5 ETH - 150 Supply",
            "borrow": "2 ETH - 100 Supply",
            "magister": "50 ETH - 49 Supply",
        },
    }

