# SPLITTERS

ECO_SPLIT = {
    "eth": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
    "opti": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
    "poly": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
    "arb": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
    "bsc": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
    "base": {
        "x7r_percentage": 0.10,
        "x7dao_percentage": 0.10,
        "x7_constellations_percentage": 0.10,
        "lending_pool_percentage": 0.20,
        "treasury_percentage": 0.50,
    },
}


TREASURY_SPLIT = {
    "eth": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,

    },
    "opti": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "developers_multisig_percentage": 0.15,
        "community_multisig_percentage": 0.30,

    },
    "poly": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "developers_multisig_percentage": 0.15,
        "community_multisig_percentage": 0.30,

    },
    "arb": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "developers_multisig_percentage": 0.15,
        "community_multisig_percentage": 0.30,

    },
    "bsc": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "developers_multisig_percentage": 0.15,
        "community_multisig_percentage": 0.30,

    },
    "base": {
        "profit_percentage": 0.49,
        "reward_pool_percentage": 0.06,
        "developers_multisig_percentage": 0.15,
        "community_multisig_percentage": 0.30,

    },
}

def GENERATE_ECO_SPLIT(chain, eth_value):
    chain_info = ECO_SPLIT.get(chain)
    if chain_info:
        x7r_percentage = chain_info["x7r_percentage"]
        x7dao_percentage = chain_info["x7dao_percentage"]
        x7_constellations_percentage = chain_info["x7_constellations_percentage"]
        lending_pool_percentage = chain_info["lending_pool_percentage"]
        treasury_percentage = chain_info["treasury_percentage"]
        treasury_share = eth_value * treasury_percentage

        x7r_share = eth_value * x7r_percentage
        x7dao_share = eth_value * x7dao_percentage
        x7_constellations_share = eth_value * x7_constellations_percentage
        lending_pool_share = eth_value * lending_pool_percentage

        return {
            "> X7R Liquidity": x7r_share,
            "> X7DAO Liquidity": x7dao_share,
            "> X7 Constellation Liquidity": x7_constellations_share,
            "> Lending Pool": lending_pool_share,
            "> Treasury Splitter": treasury_share,
        }
    

def GENERATE_TREASURY_SPLIT(chain, eth_value):
    chain_info = TREASURY_SPLIT.get(chain)
    if chain_info:
        profit_percentage = chain_info["profit_percentage"]
        community_multisig_percentage = chain_info["community_multisig_percentage"]
        developers_multisig_percentage = chain_info["developers_multisig_percentage"]

        profit_share = eth_value * profit_percentage
        community_multisig_share = eth_value * community_multisig_percentage
        developers_multisig_share = eth_value * developers_multisig_percentage

        if chain == "eth":
            reward_pool_percentage = chain_info["reward_pool_percentage"]
            reward_pool_share = eth_value * reward_pool_percentage
            return {
                "> Profit Sharing Splitter": profit_share,
                "> Pioneer Reward Pool": reward_pool_share,
                "> Operations Multi Sig": developers_multisig_share,
                "> Community Multi Sig": community_multisig_share,
            }
        else:
            return {
                "> Profit Sharing Splitter": profit_share,
                "> Operations Multi Sig": developers_multisig_share,
                "> Community Multi Sig": community_multisig_share,

            }
