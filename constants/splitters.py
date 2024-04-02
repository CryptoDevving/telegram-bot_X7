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
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
    },
    "opti": {
        "profit_percentage": 0.49,
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
    },
    "poly": {
        "profit_percentage": 0.49,
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
    },
    "arb": {
        "profit_percentage": 0.49,
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
    },
    "bsc": {
        "profit_percentage": 0.49,
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
    },
    "base": {
        "profit_percentage": 0.49,
        "pioneer_reward_pool_percentage": 0.06,
        "community_multisig_percentage": 0.32,
        "developers_multisig_percentage": 0.13,
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
        pioneer_reward_pool_percentage = chain_info["pioneer_reward_pool_percentage"]
        community_multisig_percentage = chain_info["community_multisig_percentage"]
        developers_multisig_percentage = chain_info["developers_multisig_percentage"]

        profit_share = eth_value * profit_percentage
        pioneer_reward_pool_share = eth_value * pioneer_reward_pool_percentage
        community_multisig_share = eth_value * community_multisig_percentage
        developers_multisig_share = eth_value * developers_multisig_percentage

        return {
            "> Profit Sharing Splitter": profit_share,
            "> Pioneer Reward Pool": pioneer_reward_pool_share,
            "> Community Multi Sig": community_multisig_share,
            "> Developers Multi Sig": developers_multisig_share,
        }
