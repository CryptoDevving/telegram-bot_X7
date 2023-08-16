from data import ca


contract_mappings = {
        "x7100 liquidity hub": (("function setShares()\n"
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
        "x7dao liquiidty hub": (("function setShares()\n"
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
        "x7r liquidity hub": (("function setShares()\n"
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
        "x7d":(("function setAuthorizedMinter()\n"
        "function setAuthorizedRedeemer()\n"
        "function setRecoveredTokenRecipient()\n"
        "function setRecoveredETHRecipient()"
        ), ca.x7d),
        "ecosystem splitter": (("function setWETH()\n"
        "function setOutlet()\n"
        "function freezeOutletChange()\n"
        "function setShares()\n"
        ), ca.eco_splitter),
        "treasury splitter":(("function setOtherSlotRecipient()\n"
        "function setOtherSlotShares()\n"
        ), ca.treasury_splitter),
        "factory": (("function setFeeTo()\n"
        "function setDiscountAuthority()\n"
        "function setTrusted()\n"
        "function setFailsafeLiquidator()"
        ), ca.factory),
        "borrowing maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ),ca.borrow),
        "dex maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.dex),
        "ecosystem maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.eco),
        "liquiidity maxi": (("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.liq),
        "magister":(("function setMintFeeDestination()\n"
        "function setBaseURI()\n"
        "function setMintPrice()"
        ), ca.magister),
        "pioneer":(("function setTransferUnlockFeeDestination()\n"
        "function setBaseURI()\n"
        "function setTransferUnlockFee()\n"
        "function SetAllowTokenOwnerVariantSelection()"
        ), ca.pioneer),
        "lending pool": (("function setEcosystemRecipientAddress()\n"
        "function setRouter()\n"
        "function setWETH()\n"
        "function setX7D()\n"
        "function setLoanTermActiveState()\n"
        "function setLiquidationReward()\n"
        "function setOriginationShares()\n"
        "function setPremiumShares()"
        ),ca.lpool),
        "lending pool reserve":(("function setLendingPool()\n"
        "function setEcosystemRecipientAddress()\n"
        "function setX7D()\n"
        "function setEcosystemPayer()\n"
        "function fundLendingPool()\n"
        "function setRecoveredTokenRecipient()"
        ), ca.lpool_reserve),
        "loans": (("function setLoanAuthority()\n"
        "function setBaseURI()\n"
        "function setUseBaseURIOnly()\n"
        "function setLoanLengthLimits()\n"
        "function setLoanAmountLimits()"
        ), ca.ill001), 
        "token time lock": (("function setWETH()\n"
        "function setGlobalUnlockTimestamp()\n"
        "function extendGlobalUnlockTimestamp()\n"
        "function setTokenUnlockTimestamp()\n"
        "function extendTokenUnlockTimestamp()\n"
        "function setTokenOwner()"
        ), ca.time_lock),
        "token burner": (("function setRouter()\n"
        "function setTargetToken()"
        ), ca.burner),
        "x7100 discount authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        "function setMagisterNFT()\n"
        "function setX7DAO()\n"
        ), ca.x7100_discount),
        "x7dao discount authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        ), ca.x7dao_discount),
        "x7r discount authority": (("function setEcosystemMaxiNFT()\n"
        "function setLiquidityMaxiNFT()\n"
        "function setMagisterNFT()\n"
        ), ca.x7r_discount),
        "lending discount authority":(("function setAuthorizedConsumer()\n"
        "function setTimeBasedDiscount()\n"
        "function setAmountBasedDiscount()\n"
        "function setDiscountNFT()\n"
        "function setConsumableDiscountNFT()\n"
        "function setDiscountNFTDiscounts()\n"
        "function setConsumableDiscountNFTDiscounts()"
        ), ca.lending_discount),
        "xchange discount authority": (("function setDEXMaxiNFT()"
        ), ca.xchange_discount),
}


    



    
    
    

    



