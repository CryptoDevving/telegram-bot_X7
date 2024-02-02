# NFTS

from api import index as api
from constants import ca


def NFT_PRICES():
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


def NFT_FLOORS():
    return {
        "eth": {
            "eco": api.get_nft_floor(ca.ECO, "eth") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "eth") or 0,
            "dex": api.get_nft_floor(ca.DEX, "eth") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "eth") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "eth") or 0,
        },
        "arb": {
            "eco": api.get_nft_floor(ca.ECO, "arb") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "arb") or 0,
            "dex": api.get_nft_floor(ca.DEX, "arb") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "arb") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "arb") or 0,
        },
        "opti": {
            "eco": api.get_nft_floor(ca.ECO, "opti") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "opti") or 0,
            "dex": api.get_nft_floor(ca.DEX, "opti") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "opti") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "opti") or 0,
        },
        "poly": {
            "eco": api.get_nft_floor(ca.ECO, "poly") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "poly") or 0,
            "dex": api.get_nft_floor(ca.DEX, "poly") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "poly") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "poly") or 0,
        },
        "bsc": {
            "eco": api.get_nft_floor(ca.ECO, "bsc") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "bsc") or 0,
            "dex": api.get_nft_floor(ca.DEX, "bsc") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "bsc") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "bsc") or 0,
        },
        "base": {
            "eco": api.get_nft_floor(ca.ECO, "base") or 0,
            "liq": api.get_nft_floor(ca.LIQ, "base") or 0,
            "dex": api.get_nft_floor(ca.DEX, "base") or 0,
            "borrow": api.get_nft_floor(ca.BORROW, "base") or 0,
            "magister": api.get_nft_floor(ca.MAGISTER, "base") or 0,
        },
    }


def NFT_COUNTS():
    return {
        "eth": {
            "eco": int(api.get_nft_holder_count(ca.ECO, "eth")) or 0,
            "liq": int(api.get_nft_holder_count(ca.LIQ, "eth")) or 0,
            "dex": int(api.get_nft_holder_count(ca.DEX, "eth")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.BORROW, "eth")) or 0,
            "magister": int(api.get_nft_holder_count(ca.MAGISTER, "eth")) or 0,
        },
        "arb": {
            "eco": int(api.get_nft_holder_count(ca.ECO, "arb")) or 0,
            "liq": int(api.get_nft_holder_count(ca.LIQ, "arb")) or 0,
            "dex": int(api.get_nft_holder_count(ca.DEX, "arb")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.BORROW, "arb")) or 0,
            "magister": int(api.get_nft_holder_count(ca.MAGISTER, "arb")) or 0,
        },
        "opti": {
            "eco": int(api.get_nft_holder_count(ca.ECO, "opti")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.BORROW, "opti")) or 0,
            "dex": int(api.get_nft_holder_count(ca.DEX, "opti")) or 0,
            "liq": int(api.get_nft_holder_count(ca.LIQ, "opti")) or 0,
            "magister": int(api.get_nft_holder_count(ca.MAGISTER, "opti")) or 0,
        },
        "poly": {
            "eco": int(api.get_nft_holder_count(ca.ECO, "poly")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.BORROW, "poly")) or 0,
            "dex": int(api.get_nft_holder_count(ca.DEX, "poly")) or 0,
            "liq": int(api.get_nft_holder_count(ca.LIQ, "poly")) or 0,
            "magister": int(api.get_nft_holder_count(ca.MAGISTER, "poly")) or 0,
        },
        "bsc": {
            "eco": int(api.get_nft_holder_count(ca.ECO, "bsc")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.BORROW, "bsc")) or 0,
            "dex": int(api.get_nft_holder_count(ca.DEX, "bsc")) or 0,
            "liq": int(api.get_nft_holder_count(ca.LIQ, "bsc")) or 0,
            "magister": int(api.get_nft_holder_count(ca.MAGISTER, "bsc")) or 0,
        },
    }


def NFT_DISCOUNTS():
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
