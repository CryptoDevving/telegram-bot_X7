from data import ca


contract_mappings = {
        "X7100 Liquidity Hub": (("function setShares()\n"
        "function setRouter()\n"
        "function setOffRampPair()\n"
        "function setBalanceThreshold()\n"
        "function setLiquidityBalanceThreshold()\n"
        "function setLiquidityRatioTarget()\n"
        "function setLiquidityTokenReceiver()\n"
        "function setDistributionTarget()\n"
        "function setLendingPoolTarget()\n"
        "function setTreasuryTarget()\n"
        "function freezeTreasuryTarget()\n"
        "function freezeDistributeTarget()\n"
        "function freezeLendingPoolTarget()\n"
        "function freezeBalanceThreshold()\n"
        "function freezeLiquidityBalanceThreshold()"
        ), ca.x7100_liq_hub),
        "X7DAO Liquiidty Hub": (("function setShares()\n"
        "function setRouter()\n"
        "function setOffRampPair()\n"
        "function setBalanceThreshold()\n"
        "function setLiquidityRatioTarget()\n"
        "function setLiquidityTokenReceiver()\n"
        "function setDistributionTarget()\n"
        "function setAuxiliaryTarget()\n"
        "function setTreasuryTarget()\n"
        "function freezeTreasuryTarget()\n"
        "function freezeDistributeTarget()\n"
        "function freezeAuxiliaryTarget()\n"
        "function freezeBalanceThreshold()"
        ), ca.x7dao_liq_hub),
        "X7R Liquidity Hub": (("function setShares()\n"
        "function setRouter()\n"
        "function setOffRampPair()\n"
        "function setBalanceThreshold()\n"
        "function setLiquidityRatioTarget()\n"
        "function setLiquidityTokenReceiver()\n"
        "function setDistributionTarget()\n"
        "function setTreasuryTarget() \n"
        "function freezeTreasuryTarget()\n"
        "function freezeDistributeTarget()\n"
        "function freezeBalanceThreshold()"
        ), ca.x7r_liq_hub),
        "X7D":(("function setAuthorizedMinter()\n"
        "function setAuthorizedRedeemer()\n"
        "function setRecoveredTokenRecipient()\n"
        "function setRecoveredETHRecipient()"
        ), ca.x7d),
        "Ecosystem Splitter": (("function setWETH()\n"
        "function setOutlet()\n"
        "function freezeOutletChange()\n"
        "function setShares()\n"
        ), ca.eco_splitter),
        "Treasury Splitter":(("function setOtherSlotRecipient()\n"
        "function setOtherSlotShares()\n"
        ), ca.treasury_splitter),
        "Factory": (("function setFeeTo()\n"
        "function setDiscountAuthority()\n"
        "function setTrusted()\n"
        "function setFailsafeLiquidator()"
        ), ca.factory),
        "Borrowing Maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ),ca.borrow),
        "DEX Maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.dex),
        "Ecosystem Maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.eco),
        "Liquidity Maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.liq),
        "Magister":(("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.magister),
        "Pioneer":(("function setTransferUnlockFeeDestination()\n"
        "function setBaseURI()\n"
        "function setTransferUnlockFee()\n"
        "function SetAllowTokenOwnerVariantSelection()"
        ), ca.pioneer),
        "Lending Pool": (("function setEcosystemRecipientAddress()\n"
        "function setRouter()\n"
        "function setWETH()\n"
        "function setX7D()\n"
        "function setLoanTermActiveState()\n"
        "function setLiquidationReward()\n"
        "function setOriginationShares()\n"
        "function setPremiumShares()"
        ),ca.lpool),
        "Lending Pool Reserve":(("function setLendingPool()\n"
        "function setEcosystemRecipientAddress()\n"
        "function setX7D()\n"
        "function setEcosystemPayer()\n"
        "function fundLendingPool()\n"
        "function setRecoveredTokenRecipient()"
        ), ca.lpool_reserve),
        "Loans": (("function setLoanAuthority()\n"
        "function setBaseURI()\n"
        "function setUseBaseURIOnly()\n"
        "function setLoanLengthLimits()\n"
        "function setLoanAmountLimits()"
        ), ca.ill001), 
        "Token Time Lock": (("function setWETH()\n"
        "function setGlobalUnlockTimestamp()\n"
        "function extendGlobalUnlockTimestamp()\n"
        "function setTokenUnlockTimestamp()\n"
        "function extendTokenUnlockTimestamp()\n"
        "function setTokenOwner()"
        ), ca.time_lock),
        "Token Burner": (("function setRouter()\n"
        "function setTargetToken()"
        ), ca.burner),
        "X7100 Discount Authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        "function setMagisterNFT()\n"
        "function setX7DAO()\n"
        ), ca.x7100_discount),
        "X7DAO Discount Authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        ), ca.x7dao_discount),
        "X7R Discount Authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        "function setMagisterNFT()\n"
        ), ca.x7r_discount),
        "Lending Discount Authority":(("function setAuthorizedConsumer()\n"
        "function setTimeBasedDiscount()\n"
        "function setAmountBasedDiscount()\n"
        "function setDiscountNFT()\n"
        "function setConsumableDiscountNFT()\n"
        "function setDiscountNFTDiscounts()\n"
        "function setConsumableDiscountNFTDiscounts()"
        ), ca.lending_discount),
        "Xchange Discount Authority": (("function setDEXMaxiNFT()"
        ), ca.xchange_discount),
}


    



    
    
    

    



