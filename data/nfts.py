# NFTS

from api import index as api
from data import ca


def nft_prices():
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
    }

def nft_floors():
    return {
        "eth": {
            "eco": api.get_nft_floor(ca.eco, "eth") or 0,
            "liq": api.get_nft_floor(ca.liq, "eth") or 0,
            "dex": api.get_nft_floor(ca.dex, "eth") or 0,
            "borrow": api.get_nft_floor(ca.borrow, "eth") or 0,
            "magister": api.get_nft_floor(ca.magister, "eth") or 0,
        },
        "arb": {
            "eco": api.get_nft_floor(ca.eco, "arb") or 0,
            "liq": api.get_nft_floor(ca.liq, "arb") or 0,
            "dex": api.get_nft_floor(ca.dex, "arb") or 0,
            "borrow": api.get_nft_floor(ca.borrow, "arb") or 0,
            "magister": api.get_nft_floor(ca.magister, "arb") or 0,
        },
        "opti": {
            "eco": api.get_nft_floor(ca.eco, "opti") or 0,
            "borrow": api.get_nft_floor(ca.borrow, "opti") or 0,
            "dex": api.get_nft_floor(ca.dex, "opti") or 0,
            "liq": api.get_nft_floor(ca.liq, "opti") or 0,
            "magister": api.get_nft_floor(ca.magister, "opti") or 0,
        },
        "poly": {
            "eco": api.get_nft_floor(ca.eco, "poly") or 0,
            "borrow": api.get_nft_floor(ca.borrow, "poly") or 0,
            "dex": api.get_nft_floor(ca.dex, "poly") or 0,
            "liq": api.get_nft_floor(ca.liq, "poly") or 0,
            "magister": api.get_nft_floor(ca.magister, "poly") or 0,
        },
        "bsc": {
            "eco": api.get_nft_floor(ca.eco, "bsc") or 0,
            "borrow": api.get_nft_floor(ca.borrow, "bsc") or 0,
            "dex": api.get_nft_floor(ca.dex, "bsc") or 0,
            "liq": api.get_nft_floor(ca.liq, "bsc") or 0,
            "magister": api.get_nft_floor(ca.magister, "bsc") or 0,
        },
    }

def nft_counts():
    return {
        "eth": {
            "eco": int(api.get_nft_holder_count(ca.eco, "eth")) or 0,
            "liq": int(api.get_nft_holder_count(ca.liq, "eth")) or 0,
            "dex": int(api.get_nft_holder_count(ca.dex, "eth")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.borrow, "eth")) or 0,
            "magister": int(api.get_nft_holder_count(ca.magister, "eth")) or 0,
        },
        "arb": {
            "eco": int(api.get_nft_holder_count(ca.eco, "arb")) or 0,
            "liq": int(api.get_nft_holder_count(ca.liq, "arb")) or 0,
            "dex": int(api.get_nft_holder_count(ca.dex, "arb")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.borrow, "arb")) or 0,
            "magister": int(api.get_nft_holder_count(ca.magister, "arb")) or 0,
        },
        "opti": {
            "eco": int(api.get_nft_holder_count(ca.eco, "opti")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.borrow, "opti")) or 0,
            "dex": int(api.get_nft_holder_count(ca.dex, "opti")) or 0,
            "liq": int(api.get_nft_holder_count(ca.liq, "opti")) or 0,
            "magister": int(api.get_nft_holder_count(ca.magister, "opti")) or 0,
        },
        "poly": {
            "eco": int(api.get_nft_holder_count(ca.eco, "poly")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.borrow, "poly")) or 0,
            "dex": int(api.get_nft_holder_count(ca.dex, "poly")) or 0,
            "liq": int(api.get_nft_holder_count(ca.liq, "poly")) or 0,
            "magister": int(api.get_nft_holder_count(ca.magister, "poly")) or 0,
        },
        "bsc": {
            "eco": int(api.get_nft_holder_count(ca.eco, "bsc")) or 0,
            "borrow": int(api.get_nft_holder_count(ca.borrow, "bsc")) or 0,
            "dex": int(api.get_nft_holder_count(ca.dex, "bsc")) or 0,
            "liq": int(api.get_nft_holder_count(ca.liq, "bsc")) or 0,
            "magister": int(api.get_nft_holder_count(ca.magister, "bsc")) or 0,
        },
    }

def nft_discount():
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
