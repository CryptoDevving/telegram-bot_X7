# TAX

info = {
    "eth": {
        "x7r": 3,
        "x7dao": 3,
        "x7100": 2,
        "liq_discount_x7r": 25,
        "liq_discount_x7dao": 15,
        "liq_discount_x7100": 50,
        "eco_discount_x7r": 10,
        "eco_discount_x7dao": 10,
        "eco_discount_x7100": 25,
        "magister_discount": 25,
    },
    "opti": {
        "x7r": 6,
        "x7dao": 6,
        "x7100": 2,
        "liq_discount_x7r": 25,
        "liq_discount_x7dao": 15,
        "liq_discount_x7100": 50,
        "eco_discount_x7r": 10,
        "eco_discount_x7dao": 10,
        "eco_discount_x7100": 25,
        "magister_discount": 25,
    },
    "poly": {
        "x7r": 6,
        "x7dao": 6,
        "x7100": 2,
        "liq_discount_x7r": 25,
        "liq_discount_x7dao": 15,
        "liq_discount_x7100": 50,
        "eco_discount_x7r": 10,
        "eco_discount_x7dao": 10,
        "eco_discount_x7100": 25,
        "magister_discount": 25,
    },
    "arb": {
        "x7r": 6,
        "x7dao": 6,
        "x7100": 2,
        "liq_discount_x7r": 25,
        "liq_discount_x7dao": 15,
        "liq_discount_x7100": 50,
        "eco_discount_x7r": 10,
        "eco_discount_x7dao": 10,
        "eco_discount_x7100": 25,
        "magister_discount": 25,
    },
    "bsc": {
        "x7r": 6,
        "x7dao": 6,
        "x7100": 2,
        "liq_discount_x7r": 25,
        "liq_discount_x7dao": 15,
        "liq_discount_x7100": 50,
        "eco_discount_x7r": 10,
        "eco_discount_x7dao": 10,
        "eco_discount_x7100": 25,
        "magister_discount": 25,
    },
}


def generate_info(network):
    network_info = info.get(network)
    if network_info:
        x7r = network_info["x7r"]
        x7dao = network_info["x7dao"]
        x7100 = network_info["x7100"]
        liq_discount_x7r = network_info["liq_discount_x7r"]
        liq_discount_x7dao = network_info["liq_discount_x7dao"]
        liq_discount_x7100 = network_info["liq_discount_x7100"]
        eco_discount_x7r = network_info["eco_discount_x7r"]
        eco_discount_x7dao = network_info["eco_discount_x7dao"]
        eco_discount_x7100 = network_info["eco_discount_x7100"]
        magister_discount = network_info["magister_discount"]

        network_info_str = (
            f"*X7 Finance Tax Info ({network.upper()})*\nUse `/tax [chain-name]` for other chains\n\n"
            f"X7R: {x7r}%\nX7DAO: {x7dao}%\n"
            f"X7101-X7105: {x7100}%\n\n"
            "*Tax with NFTs*\n"
            "Ecosystem Maxi:\n"
            f"X7R: {x7r - (x7r * eco_discount_x7r / 100)}%\n"
            f"X7DAO: {x7dao - (x7dao * eco_discount_x7dao / 100)}%\n"
            f"X7101-X7105: {x7100 - (x7100 * eco_discount_x7100 / 100)}%\n\n"
            "Liquidity Maxi:\n"
            f"X7R: {x7r - (x7r * liq_discount_x7r / 100)}%\n"
            f"X7DAO: {x7dao - (x7dao * liq_discount_x7dao / 100)}%\n"
            f"X7101-X7105: {x7100 - (x7100 * liq_discount_x7100 / 100)}%\n\n"
            "Magister:\n"
            f"X7R: {x7r - (x7r * magister_discount / 100)}%\n"
            f"X7DAO: {x7dao}%\n"
            f"X7101-X7105: {x7100 - (x7100 * magister_discount / 100)}%\n"
        )

        return network_info_str
