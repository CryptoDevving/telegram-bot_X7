# DAO

from constants import ca

CONTRACT_MAPPINGS = {
    "X7100 Liquidity Hub": ((
        "setShares\n"
        "setRouter\n"
        "setOffRampPair\n"
        "setBalanceThreshold\n"
        "setLiquidityBalanceThreshold\n"
        "setLiquidityRatioTarget\n"
        "setLiquidityTokenReceiver\n"
        "setDistributionTarget\n"
        "setLendingPoolTarget\n"
        "setTreasuryTarget\n"
        "freezeTreasuryTarget\n"
        "freezeDistributeTarget\n"
        "freezeLendingPoolTarget\n"
        "freezeBalanceThreshold\n"
        "freezeLiquidityBalanceThreshold"
        ), ca.X7100_LIQ_HUB),
    "X7DAO Liquidity Hub": (
        ("setShares\n"
        "setRouter\n"
        "setOffRampPair\n"
        "setBalanceThreshold\n"
        "setLiquidityRatioTarget\n"
        "setLiquidityTokenReceiver\n"
        "setDistributionTarget\n"
        "setAuxiliaryTarget\n"
        "setTreasuryTarget\n"
        "freezeTreasuryTarget\n"
        "freezeDistributeTarget\n"
        "freezeAuxiliaryTarget\n"
        "freezeBalanceThreshold"
        ), ca.X7DAO_LIQ_HUB),
    "X7R Liquidity Hub": (
        ("setShares\n"
        "setRouter\n"
        "setOffRampPair\n"
        "setBalanceThreshold\n"
        "setLiquidityRatioTarget\n"
        "setLiquidityTokenReceiver\n"
        "setDistributionTarget\n"
        "setTreasuryTarget \n"
        "freezeTreasuryTarget\n"
        "freezeDistributeTarget\n"
        "freezeBalanceThreshold"
        ), ca.X7R_LIQ_HUB),
    "X7D": (
        ("setAuthorizedMinter\n"
        "setAuthorizedRedeemer\n"
        "setRecoveredTokenRecipient\n"
        "setRecoveredETHRecipient"
        ), ca.X7D),
    "Ecosystem Splitter": (
        ("setWETH\n"
        "setOutlet\n"
        "freezeOutletChange\n"
        "setShares\n"
        ), ca.ECO_SPLITTER),
    "Treasury Splitter": (
        ("freezeOutlet\n"
        "setOutletRecipient\n"
        "setSlotShares"
        ), ca.TREASURY_SPLITTER),
    "Factory": (
        ("setFeeTo\n"
        "setDiscountAuthority\n"
        "setTrusted\n"
        "setFailsafeLiquidator"
        ), ca.FACTORY),
    "Borrowing Maxi": (
        ("setMintFeeDestination\n"
        "setBaseURI\n"
        "setMintPrice"
        ), ca.BORROW),
    "DEX Maxi": (
        ("setMintFeeDestination\n"
        "setBaseURI\n"
        "setMintPrice"
        ), ca.DEX),
    "Ecosystem Maxi": (
        ("setMintFeeDestination\n"
        "setBaseURI\n"
        "setMintPrice"
        ), ca.ECO),
    "Liquidity Maxi": (
        ("setMintFeeDestination\n"
        "setBaseURI\n"
        "setMintPrice"
        ), ca.LIQ),
    "Magister": (
        ("setMintFeeDestination\n"
        "setBaseURI\n"
        "setMintPrice"
        ), ca.MAGISTER),
    "Pioneer": (
        ("setTransferUnlockFeeDestination\n"
        "setBaseURI\n"
        "setTransferUnlockFee\n"
        "SetAllowTokenOwnerVariantSelection"
        ), ca.PIONEER),
    "Lending Pool": (
        ("setEcosystemRecipientAddress\n"
        "setRouter\n"
        "setWETH\n"
        "setX7D\n"
        "setLoanTermActiveState\n"
        "setLiquidationReward\n"
        "setOriginationShares\n"
        "setPremiumShares"
        ), ca.LPOOL),
    "Lending Pool Reserve": (
        ("setLendingPool\n"
        "setEcosystemRecipientAddress\n"
        "setX7D\n"
        "setEcosystemPayer\n"
        "fundLendingPool\n"
        "setRecoveredTokenRecipient"
        ), ca.LPOOL_RESERVE),
    "Loans": (
        ("setLoanAuthority\n"
        "setBaseURI\n"
        "setUseBaseURIOnly\n"
        "setLoanLengthLimits\n"
        "setLoanAmountLimits"
        ), ca.ILL001),
    "Token Time Lock": (
        ("setWETH\n"
        "setGlobalUnlockTimestamp\n"
        "extendGlobalUnlockTimestamp\n"
        "setTokenUnlockTimestamp\n"
        "extendTokenUnlockTimestamp\n"
        "setTokenOwner"
        ), ca.TIME_LOCK),
    "Token Burner": (
        ("setRouter\n"
        "setTargetToken"
        ), ca.BURNER),
    "X7100 Discount Authority": (
        ("setEcosystemMaxiNFT\n"
        "setLiquidityMaxiNFT\n"
        "setMagisterNFT\n"
        "setX7DAO\n"
        ), ca.X7100_DISCOUNT),
    "X7DAO Discount Authority": (
        ("setEcosystemMaxiNFT\n"
        "setLiquidityMaxiNFT\n"
        ), ca.X7DAO_DISCOUNT),
    "X7R Discount Authority": (
        ("setEcosystemMaxiNFT\n"
        "setLiquidityMaxiNFT\n"
        "setMagisterNFT\n"
        ), ca.X7R_DISCOUNT),
    "Lending Discount Authority": (
        ("setAuthorizedConsumer\n"
        "setTimeBasedDiscount\n"
        "setAmountBasedDiscount\n"
        "setDiscountNFT\n"
        "setConsumableDiscountNFT\n"
        "setDiscountNFTDiscounts\n"
        "setConsumableDiscountNFTDiscounts"
        ), ca.LENDING_DISCOUNT),
    "Xchange Discount Authority": (
        ("setDEXMaxiNFT"
        ), ca.XCHANGE_DISCOUNT),
}
