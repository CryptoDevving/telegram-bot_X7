import random


about = (
    "*X7 Finance - Home of Xchange*\n\n"
    "X7 Finance is an ecosystem of innovative smart contracts, and the centre of the ecosystem is the X7 Finance"
    ' Lending Pool, a pool that provides those with visionary ideas access to Initial Liquidity Loans "ILL".\n\n'
    "At its core, Initial Liquidity Loans will provide anyone with a good idea the ability to raise 10-1000X "
    "the amount of capital in their wallet to launch projects on Xchange.\n\n"
    "• The network effect of project launches will result in billions of dollars in trading volume on Xchange, "
    "a percentage of this volume will flow back into the ecosystem into our native X7 tokens.\n\n"
    "• X7 Finance has a novel DAO governance structure + IPFS website, that ensures complete decentralization "
    "and censorship-resistance.\n\n"
    "Our Telegram network and X are community-run, in the spirit of decentralization.\n\n"
    "• First target - Capturing 1% of the $100b daily trading volume on the Ethereum network.\n\n"
    '`"X7’s founding team believes that capital should be available to those with great ideas and that the '
    "unflinching reliability of code and distributed consensus can provide capital while eliminating significant "
    "downside risk.`\n\n#LongLiveDefi"
)

admin_commands = (
    "To be run in main chat\n\n"
    "/settings - Open the setting menu\n"
    "/setup - Setup the portal\n"
    "/difficulty - Set the CAPTCHA difficulty\n"
    "/antiflood - (Dis)Enable anti-flood mode\n"
    "/lock all - mutes chat\n"
    "/unlock all - unmute chat\n"
    "/shield - Start shield raid\n"
    "BuyBotTech - X7R\n"
    "BobbyBuyBot - X7DAO, X7101, X7102\n"
    "BubbleBuyBot - X7103, X7104, X7105\n"
)

airdrop = (
    "*X7 Finance Airdrop Information*\n\nThe rollout of the Ecosystem Contracts on BNB Smart Chain, Polygon "
    "(MATIC), Arbitrum, and Optimism has begun.\n\n"
    "We will go live with Xchange, borrowing, lending, revenue "
    "splitting, and profit splitting on other chains as soon as we can in concert with the full release on "
    "Ethereum.\n\nThe tokens however will not go live until we have built up a sufficient amount of initial "
    "liquidity for the tokens on any particular chain.\n\nWhen the tokens do go live all X7 token holders on "
    "Ethereum will be airdropped vested tokens and/or be given an opportunity to take a cash payout for their "
    "share of tokens. We will set prices and payouts to ensure that there will be no incentive to exit an "
    "Ethereum X7 Token position in order to gain an 'early' L1 or L2 ecosystem X7 token position. On the "
    "contrary, the more tokens held on Ethereum, the greater the reward will be when the tokens and ecosystem "
    "are released on other chains.\n\nThese airdrop snapshots will occur just prior to the token launch"
)

alumni = (
    "@Callmelandlord - The Godfather of the X7 Finance community, the OG, the creator - X7 God\n\n"
    "@WoxieX - Creator of the OG dashboard -  x7community.space\n\n"
    "@Zaratustra  - Defi extraordinaire and protocol prophet\n\n"
)

chain_error = f'Chain not recognised, please use "eth", "arb", "bsc", "poly" or "opti"'

commands = (
    "about - About X7 Finance\n"
    "alerts - Xchange Alerts Channel\n"
    "airdrop - Airdrop Info\n"
    "alumni - X7 Finance Alumni\n"
    "announcements - Announcements Channel\n"
    "ath - All Time High Info\n"
    "blocks - Block Info\n"
    "blog - X7 Finance Blog\n"
    "burn - X7R Burn Info\n"
    "buy - X7 Finance Buy Links\n"
    "buybacks - X7 Finance Buy Backs\n"
    "buyevenly - Buy Constellations Evenly\n"
    "channels - List of X7 Finance Channels\n"
    "chart - X7 Finance Charts\n"
    "check - Check 2 Input Addresses\n"
    "constellations - Constellation Info\n"
    "ca - Contract Addresses\n"
    "compare - Compare X7 tokens with another token\n"
    "countdown - 5,4,3,2,1\n"
    "dao - DAO Function Info\n"
    "deployer - Deployer Info\n"
    "docs - X7 Finance Docs\n"
    "dune - X7  Finance Dune Analytics Dashboard\n"
    "ecosystem - The X7 Finance Ecosystem\n"
    "fact - Daily Fact\n"
    "factory - X7 Finance Factory Contracts\n"
    "faq - X7 Finance FAQ Links\n"
    "fees - Xchange Fee Liquidation TXs\n"
    "fg - Market Fear/Greed Index\n"
    "gas - Network Gas Info\n"
    "giveaway - Giveaway Info\n"
    "holders - X7 Finance Holder Counts\n"
    "image - Image Generation\n"
    "joke - Daily Joke\n"
    "launch - X7 Finance Launch Date Info\n"
    "leaderboard - Fastest Pioneer Leaderboard\n"
    "links - X7 Finance Socials Links\n"
    "liquidate - Loan Liquidation Info\n"
    "liquidity - X7 Finance Liquidity Info\n"
    "loan - Specific Loan ID Info\n"
    "loans - Loan Term Details\n"
    "locks - Liquidity Locks Info\n"
    "me - Individual Fastest Pioneer details\n"
    "magisters - Magister Holder Info\n"
    "mcap - X7 Finance Market Cap Info\n"
    "media - X7 Finance Media Links\n"
    "mods - X7 Finance Mod roles\n"
    "nft - NFT details\n"
    "onchain - Last On Chain Message\n"
    "pairs - Xchange Pairs Info\n"
    "pfp - Create a Profile picture\n"
    "pioneer - Pioneer NFT Info\n"
    "pool - X7 Finance Lending Pool Info\n"
    "price - [followed by token] Token Price Info\n"
    "quote - Daily Quote\n"
    "referral - Refer a project to Xchange\n"
    "router - X7 Finance Router Info\n"
    "say - Text to Speech\n"
    "scan  - Scan a CA\n"
    "search - Search the Web\n"
    "signers - X7 Finance Multi Sig Signers\n"
    "smart - X7 Finance Smart Contract Details\n"
    "snapshot - X7 Finance Snapshot.org\n"
    "splitters - X7 Finance Splitters Info\n"
    "supply - Uniswap Supply Info\n"
    "tax - X7 Finance Token Tax Info\n"
    "time - World Time\n"
    "today - On This Day\n"
    "treasury - X7 Finance Treasury Info\n"
    "twitter - X7 Finance Twitter/X\n"
    "volume - Xchange Volume Info\n"
    "voting - DAO Voting Info\n"
    "wei - WEI Conversion\n"
    "wallet - Wallet Tracking\n"
    "website - X7 finance Website Links\n"
    "word - Word Definition\n"
    "whitepaper - X7 finance WP Link\n"
    "xchange - Xchange Links\n"
    "x7r - X7R Info\n"
    "x7d - X7D Info\n"
    "x7dao - X7DAO Info\n"
    "x7101 - X7101 Info\n"
    "x7102 - X7102 Info\n"
    "x7103 - X7103 Info\n"
    "x7104 - X7104 Info\n"
    "x7105 - X7105 Info\n"
)

delay = (
    "To ensure our code is trusted and that the release is flawless, X7's "
    "Leveraged DEX trading will not begin until we have published third party "
    "security audits. In the meantime, our Stochastic Topological Offensive "
    "Penetration, Probing, and Exploitation Researcher, STOPPER, has been "
    "executing millions of transactions on our private test network to ensure "
    "no edge case is missed.\n\n"
    "`A delayed game is eventually good, a bad game is bad forever.\n\n"
    "- Shigeru Miyamoto`"
)

discount = (
    "20 Lucrative X7 Borrowing Incentive NFTs have been minted, granting;\n\n"
    "50% Origination fee discount\n"
    "50% Premium fee discount\n\n"
    "These are a consumable utility NFT offering fee discounts when borrowing funds for initial liquidity on "
    "Xchange. The discount will be determined by the X7 Lending Discount Authority smart contract.\n\n"
    "Usage will cause a token owned by the holder to be burned\n\n"
    "To apply for a limited NFT see the link below\n\n"
    " --------------- \n\n"
    "There are four mechanisms to receive loan origination and premium discounts:\n\n"
    "1. Holding the Borrowing Maxi NFT\n"
    "2. Holding (and having consumed) the Borrowing Incentive NFT\n"
    "3. Borrowing a greater amount\n"
    "4. Borrowing for a shorter time\n\n"
    "All discounts are additive.\n\n"
    "The NFTs provide a fixed percentage discount. The Borrowing Incentive NFT is consumed upon "
    "loan origination.\n\n"
    "The latter two discounts provide a linear sliding scale, based on the minimum and maximum loan amounts and "
    "loan periods. The starting values for these discounts are 0-10% discount.\n\n"
    "The time based discount is imposing an opportunity cost of lent funds - and incentivizing taking out the "
    "shortest loan possible.\n"
    "The amount based discount is recognizing that a loan origination now is more valuable than a possible loan "
    "origination later.\n\nThese sliding scales can be modified to ensure they have optimal market fit."
)

ecosystem = (
    "*X7 Finance Ecosystem*\n\n• *X7R*\nX7's original launched token. Hodl as a percentage of all "
    "transaction fees are used to buy and burn tokens, reducing total supply of available tokens.\n\n"
    "• *X7DAO*\nHolders of X7DAO tokens will be able to vote on fee rates, loan terms, funding terms, "
    "tradable token tax terms, distribution of capital flows and any additional settings on and off chain. "
    "This includes the establishment of committees and other foundational efforts off chain.\n\n"
    "• *X7100 Constellation (X7101 - X7105)*\n"
    "A novel - eventually price consistent collection of five tokens. These act as the backstop to the "
    "Lending Pool. While continually raising its "
    "floor price - it also provides further opportunities to mint new X7Deposit tokens.\n\n"
    "• *X7 NFTs*\nNFTs within the ecosystem will be used to provide opportunities for staking, lending, "
    "discounts, rewards, access to higher governance privileges & much more.\n\n"
    "• *X7Deposit*\nWith insurance of the investor at heart - individuals and "
    "institutions will hold these tokens "
    "just as they would underwrite treasury bills and other stable assets. Holders of X7D will be able to "
    "mint a time-based interest-bearing NFT. X7D is always exchangeable with Ethereum at a 1-to-1 ratio.\n"
    "The X7 Finance protocol will only permit minting of new X7 Deposit tokens when on-chain reserves permit."
)

endorse = (
    "*XChange Pairs*\n\nThe X7 Dev team or the community team will not endorse any particular token or launch on Xchange.\n\n"
    "Xchange is a permissionless swap protocol. We encourage DeFi participants to exercise the same level of "
    "caution they always should when evaluating a swap opportunity.\n\nFor new token alerts see XChange Alerts channel below"
    "\n\n"
    "Trust No one, trust code. Long Live Defi"
)

evenly = (
    "*Buy All X7 Finance Constellation Tokens Evenly (ETH)*\n\n"
    "Simply connect to https://dapp.x7community.space/constellation via metamask mobile or desktop"
    " and enter your desired Eth amount\n\n"
    "Alternatively you can interact with the follow contract and follow the steps "
    "below:\n\n"
    "1. Head over to the Buy Evenly contract:\nhttps://etherscan.io/address/0x0419074afe1a137dfa6afd5b6af5"
    "771c3ffbea49#code\n"
    '1.1. Press on "Contract" If it\'s not already selected.\n2. Press on "Write contract"\n'
    '3. Press on "Connect to Web3" and connect your desired wallet to the website. \n'
    "4. Deposit the desired values\n4.1. depositIntoX7SeriesTokens -> amount of ETH you want to spend (e.g. 0.5).\n"
    "4.2. slippagePercent  -> desired slippage (e.g. 4)\n4.3 deadline -> Go to [epoch-converter]"
    '(https://www.epochconverter.com/) and add like 500 to the current epoch. Click "Timestamp to Human date" '
    'and verify that Relative is at least "In 1 minute" (e.g. 1667508502).\n'
    '4.4 Copy the epoch to the "deadline" field\n4.4 Press "Write" and confirm the transaction in your wallet.\n'
    "4.5 You should receive tokens to your wallet in few blocks.\n\n"
    "*Testrun TX*:\n"
    "https://etherscan.io/tx/0x321e5bb6cc1695d5d7085eceb92f01143b69c2274402aab46e4a0a47d069d0af\n\n"
    "Credit: @WoxieX"
)

mods = (
    "Marketing Team\n@Robthebank44\n@cryptod0c\n\n"
    "Sales Team\n@Gazuga\n\n"
    "Socials Team\n@Phlux\n@SlumdOg_shillionaire2022\n@DallasX7\n@Gavalars\n@KBCrypto11\n@CoastCorn\n\n"
    "Tech Team\n@Adz1DoubleD\n@MikeMurpher\n@cryptod0c\n@MikeX7F"
)

mods_only = "You do not have permission to do this. #TrustNoOne"

patience = "`Patience is bitter, but its fruit is sweet.\n\n- Aristotle`"

proposals = (
    "*Listing proposal:*\n"
    "X7 Finance does not prioritize paid listings. Instead, for CEXs to acquire the desired supply "
    "amount needed to list X7 on their exchange, they will need to purchase it from existing markets.\n\n"
    "*Marketing proposal:*\n"
    "X7 Finance does not incur expenses for requested marketing activities. Instead, our team leverages "
    "its extensive network and connections in the market to independently select and collaborate with "
    "relevant parties.\n\n"
    "If, despite this information, you still find it necessary to get in touch, you can always send a "
    "DM to our X account. Please be aware that responses to such DMs are not guaranteed."
)

refer = (
    "*XChange Referral Program*\n\nDriving new projects to take advantage of X7’s lending pool currently "
    "valued over 200k USD across 5 chains is a top priority to ensure successful adoption of XChange in the "
    "market. Every individual who refers a project that successfully launches on XChange,\n\n"
    "1. Earn $250 for each project you refer to XChange, for the first 10 projects\n\n"
    "2.Earn $500 for each additional project you refer to XChange beyond the first 10 projects\n\n"
    "3. There is no limit to how many projects you can refer.\n\n"
    "For example, if you refer 15 projects to X7, you will earn $2,500 for the first 10 and $2,500 for the "
    "last 5 for a total of $5,000. The more you refer, the more you earn.\n\n"
    "*How to participate*\n\n"
    "1. Refer a project to launch on XChange with an Initial Liquidity Loan (ILL) - (2 ETH minimum)\n\n"
    "2. Ensure the referred project confirms your referral to ensure the referral is valid. (X7 Finance "
    "Community Multi-Sig will have full discretion to validate or invalidate any referrals)\n\n"
    "3. Submit these details via this the form below\n\n"
    "4. Once the project launches successfully with an ILL, the reward will be deposited to your submitted "
    "wallet address 2 weeks after the launch of the project.\n\n"
    "NOTE: community multi-sig team has final discretion on payment. Any individual or group looking to "
    "exploit this program will not be eligible for a reward."
)

volume = (
    "*Driving XChange Volume\n\nOur focus is crystal clear: we're all about boosting trading volume on Xchange. Why? Because trading drives growth and growth drives rewards.\n\n"
    "*0.1% Back to the Ecosystem*\n\n"
    "With every trade made on Xchange, 0.1% flows back to the ecosystem. That's the power of X7 Finance.\n\n"
    "*Create Your Own Liquidity Pools*\n\n"
    "Create liquidity pools now to further fuel the ecosystem. Best performers? Those with low fees and proven high volume.\n\n"
    "*Achieve Volume with Just $1000*\n\n"
    "Did you know? You can achieve trading volume with as little as $500 in ETH and $500 in the paired token. Your contribution matters!"
)

quotes = [
    "Ethos\n\nX7’s founding team believes that capital should be available to those with great ideas and that the "
    "unflinching reliability of code and distributed consensus can provide capital while eliminating significant "
    "downside risk.",
    "Executive Summary\n\nX7 is an ecosystem of innovative smart contracts that provide those with visionary ideas "
    "access to leveraged seed capital without lenders incurring the risk of losing the principal.",
    "Total Addressable Market\n\nEthereum and ERC20 tokens have 24hr trading volume in the 100s of billions. We will "
    "consider X7 a success if 1% of all trading volume takes place on Xchange.",
    "Customers And Use Cases\n\nUnderstanding who our customers are, and what their needs and use cases are, is "
    "fundamental to finding product-market fit. We have identified 4 primary user personas that have distinct needs and"
    " have optimized the system to meet their requirements.\n\nProject Launchers - Seeking Capital\nThe whole reason "
    "to build a Leveraged DEX is to enable those without large capital to access institutional scale capital. These "
    "users' activity is the core business value that is being created.\n\nCapital Providers - Seeking Passive Returns\n"
    "From individuals to institutions, our platform is built with insurance for safe returns. X7 Finance’s architecture"
    " does not allow for over-capitalization or an under-reserve.\n\nSystem Governors - Seeking Leadership\n X7 Finance"
    " provides a limitless opportunity for market participants to bring positive change within the ecosystem with "
    "on-chain governance.\n\nTraders - Seeking Active Returns\nAll tradable pairs are designed to influence price "
    "appreciation between each moving part of the ecosystem. The X7 Finance ecosystem tokens’ built-in synergetic "
    "mechanisms feed each token’s trading market and provide limitless arbitrage opportunities and advanced trading "
    "strategies.",
    "Team\n\nX7 Finance is a globally distributed collective of developers. We strongly believe that who we are is "
    "irrelevant. Our expectation is that all actors, ourselves included, will act in a self-interested manner while "
    "building and operating the X7 ecosystem.",
    "The smart contract interactions and the DAO governance will express a system design built on this core thesis. "
    "The game theory driving actor behavior will enable the system to iterate to a globally optimal system state free "
    "from intervention by any one individual or state actor.",
    "Community Stealth Launch\n\nIn a DeFi world filled with meme tokens, larps, and “speculative” projects, X7 was "
    "stealth launched to bootstrap a community and be a test bed for the technology and ideas that the teams have been "
    "thinking about and working on in the background.  Overwhelmingly positive community reception for the project and "
    "the hunger of the community for our product has accelerated our timetables. As the full ecosystem comes to "
    "fruition it should be known that these ideas have been refined and improved upon by the community's amazing "
    "outpouring of ideas and behaviors. We thank everyone, members of the community, we are building this for you!",
    "X7 System Design Philosophy\n\nPermission-less, trust-less, censorship-resistant, decentralized architecture, "
    "decentralized governance.\n\nIn recent years, exchanges across the globe have been shutting their doors to "
    "customers simply because a sovereign state has decreed it. X7 is designed to overcome those shortcomings and give "
    "power back to the people",
    "X7 System Design Philosophy\n\nPermission-less - No individual, organization, or sovereign state actor shall "
    "infringe on the functionality and usability of X7’s system. We believe the world is better with free speech and "
    "freedom and our system is designed to prevent asking permission to interact with the system.",
    "X7 System Design Philosophy\n\nTrust-less - Exemplified by the “Problem Statement” section, traditional loan "
    "systems have a problem with trust. Principle among them, is the trust that your loan will be repaid. X7’s DEX is "
    "able to allow trust-less loans between the Lending Pool and the Initial Liquidity Loan Requestor, leading to "
    "higher market capitalization and access to capital.",
    "X7 System Design Philosophy\n\nCensorship Resistant - Multinational corporations exert massive control over the "
    "finances of everyday people and recent stories of Visa, Mastercard, and PayPal blacklisting ordinary citizens from"
    " transacting on their networks highlight the need for a system to be resilient and resistant to those forms of "
    "censorship.",
    "X7 System Design Philosophy\n\nDecentralized Architecture - Engineering a system to not have single points of "
    "failure is a difficult task. X7 will run all parts of the system in multiple locations and open-source the final "
    "product so anyone can run the source code anywhere.",
    "X7 System Design Philosophy\n\nDecentralized Governance - Designing management processes to be handled by a group"
    " is also a difficult task, but X7’s governance strategy is optimized to aggregate large groups’ opinions into "
    "smaller decisions to vote on.",
    "Borrow 10-1000 times the Ethereum in your wallet\n\nThrough our innovative Leveraged Initial Liquidity DEX we can "
    "provide massive initial seed capital to visionary entrepreneurs, organizations, and businesses.",
    "Lend your crypto, without downside risk\n\nPut your Ethereum to work earning a share of loan proceeds collected by"
    " holding our X7Deposit tokens. Exchangeable with Ethereum at a 1-to-1 ratio. The X7 protocol only permits minting "
    "of new X7Deposit tokens when ON CHAIN reserves permit it.",
    "Trade like a whale\n\nAll of the trading functionality and utility you have come to expect in a DEX and more. "
    "Swapping is simple, mobile optimized and offers lower fees than the other exchanges. A truly decentralized and "
    "censorship-resistant exchange.",
    "Democratic Decentralized Governance\n\nAfter launch and discovery of market equilibrium terms, all controls will "
    "be transferred to a Voting Contract. This contract has control over setting fee rates, loan terms, funding terms, "
    "tax terms, distribution of capital flows and any additional settings. Who can make and vote on proposals? Holders "
    "of X7DAO tokens and Magister NFTs.",
    "X7 Token Ecosystem\n\nX7 is designed to address the needs of four major quadrants within decentralized finance. "
    "The symbiotic nature of each segment in the X7 Finance ecosystem provides fluid insurance for lenders and mutual "
    "funding for all other market participants.",
    "X7100 Constellation\n\nA novel - eventually price consistent collection of five tokens. These act as the backstop "
    "to the Lending Pool. The X7100 series of tokens are burned on every transaction. While continually raising its "
    "floor price - it also provides further opportunities to mint new X7Deposit tokens.",
    "X7DAO\n\nHolders of X7DAO tokens will be able to vote on fee rates, loan terms, funding terms, tradable token tax "
    "terms, distribution of capital flows and any additional settings on and off chain. This includes the "
    "establishment of committees and other foundational efforts off chain.",
    "X7Deposit\n\nWith insurance of the investor at heart - individuals and institutions will hold these tokens just as"
    " they would underwrite treasury bills and other stable assets. Holders of X7D will be able to mint a time-based "
    "interest-bearing NFT. X7D is always exchangeable with Ethereum at a 1-to-1 ratio. The X7 Finance protocol will "
    "only permit minting of new X7 Deposit tokens when on-chain reserves permit.",
    "X7R\n\nX7's original launched token. Hodl as a percentage of all transaction fees are used to buy and burn tokens,"
    " reducing total supply of available tokens.",
    "Community\n\nAll official channels are run by community members in a decentralized fashion. We believe a "
    "distributed network of individuals and committees - free from central influence is paramount to the longevity of "
    "decentralized finance.",
    "At the heart of X7 is a peer-to-peer Automated Market Making (AMM) Decentralized Exchange (DEX) integrated with a "
    "novel trust-less, permission-less on-chain under-collateralized loan origination and servicing system known as "
    "the Lending Pool. Functioning similar to a bank, the Lending Pool takes deposits, converts them to loanable "
    "assets, manages the lifecycle of a loan issued to X7’s DEX, and distributes the loan profits to the ecosystem.",
    "Token holder Value\n\n Generating Token holder Value is fundamental for long term success of X7 Finance and our "
    "tokenomics have been architected with that in mind.\n\nOwn a piece of the profits generated by the X7 Finance "
    "project by holding any of the tokens:\n\nX7DAO, engineered to lead the ecosystem through it’s governance utility."
    "\n\nX7R, designed to reward long-term holders through deflationary mechanisms.\n\nThe Constellation tokens, X7101,"
    " X7102, X7103, X7104, X7105, are eventually price consistent allowing for arbitrage opportunities.",
    "Problem Summary\n\nFrom the beginning of human civilization, lenders have sought ways to mitigate the risk of "
    "losing their loaned principal. Several mechanisms have helped to reduce risk, the most common among them are "
    "“over-collateralization”, the process of having the underlying asset be more valuable than the loan amount (for "
    "example a house should be worth more than the mortgage), “know-your-customer”, the process of collecting personal"
    " data, income, credit scores and other information to compute the ability and likelihood of loan repayment and "
    "“default recovery”, the process of recovering the loan value through force or default (banks use the legal system"
    " and repossession agents).\n\nCryptocurrency’s immutability and security models make all of the traditional risks "
    "even greater. X7 solves all of these difficult problems by implementing a stop to liquidity events through the "
    "Xchange and Lending Pool architecture. This paper will explain the product functionality and architecture that "
    "enables X7 to operate.",
    "Multi-chain Rollout\n\nThe initial release of X7 Finance’s innovative token ecosystem and Xchange will be focused "
    "on the Ethereum blockchain. Our architecture and contracts will be able to run on all Ethereum Virtual "
    "Machine-compliant blockchains such as Binance Smart Chain (BSC), and Polygon, but to deliver a refined and "
    "polished experience we are taking a sequential blockchain release approach.",
    "Xchange\n\n● Permission-less, trust-less peer-to-peer AMM platform for swapping of ERC-20 tokens, seamless "
    "integration with Ethereum for swapping of ERC20-to-ERC20 and ETH-to-ERC20.\n● Add Initial Liquidity to any "
    "ETH-based pair with our permission-less, trust-less Initial Liquidity Loan (ILL) functionality, increasing "
    "liquidity and market capitalization.\n● First among peers, X7’s DEX’s front-end dApp will connect and function "
    "with all top Uniswap Interface-compliant DEX’s.",
    "Initial Liquidity Loan\n\n● Defined loan term created in a permission-less, trust-less fashion to be funded and "
    "originated by the Lending Pool.",
    "Lending Pool\n\n● Manage loan terms availability, respond to loan origination requests, and balance reserves "
    "ratios.\n● Manages deposits through a permission-less, trust-less fully collateralized mintable deposit token, "
    "with a 1-to-1 face value of ETH, that can be staked for a share of the profits.",
    "Constellation Token\n\n● Collateralized reserves for Lending Pool’s X7 Deposit tokens, with the functionality to "
    "accumulate token value and act as lender of last resort against X7Deposit token issuance.",
    "Decentralized Anonymous Organization\n\n● Manage operations of a system with a democratic decentralized governance"
    " model among self-interested on-chain actors.\n● Balance of power provided by a team mint and future high-cost "
    "mint NFTs to balance power and interests in the system.",
    "X7’s Decentralized Exchange is a peer-to-peer Automated Market Making (AMM) platform integrated with a novel "
    "trust-less, permission-less on-chain under-collateralized loan origination and servicing system known as the "
    "Lending Pool. This section will describe the core functionality of the operations of DEX.",
    "Technical Abstract\n\nXchange is built on a forked version of the Uniswap V2 Factory, Liquidity Pair, and Router "
    "contracts. There are two notable changes:\n● The Liquidity Pair contract has added safeguards to allow it to "
    "support leveraged liquidity additions that ensure the leverage remains collateralized and can be liquidated in the"
    " event of loan default and appropriately manage Liquidity Tokens during an active Initial Liquidity Loan.\n● The "
    "liquidity provider fee has been reduced from 0.3% to 0.2%. This reflects the reality that in many cases the "
    "liquidity providers for tokens are actually the token creators and the benefit they receive is more often via "
    "token price appreciation or token fees, not liquidity provision. Additionally, the User Interface will allow a "
    "seamless experience trading across other Uniswap V2 style decentralized exchange pairs (such as Uniswap or "
    "SushiSwap).",
    "Swap\n\nSimilar to Uniswap, token swaps in Xchange are a simple way to trade one ERC-20 token for another.\n\nFor "
    "end-users, swapping is intuitive: a user picks an input token and an output token. They specify an input amount, "
    "and the protocol calculates how much of the output token they’ll receive. They then execute the swap with one "
    "click, receiving the output token in their wallet immediately.\n\nSwaps in Xchange are different from trades on "
    "traditional centralized exchange platforms. Xchange does not use an order book to represent liquidity or determine"
    " prices. Xchange uses a constant product automated market maker mechanism to provide instant feedback on rates and"
    " slippage.",
    "Pricing\n\nSimilar to Uniswap, Xchange uses the constant product formula.",
    "Lending Pool Overview\n\nTo provide leverage to the system, the Lending Pool acts as the manager of both funds and"
    " loans. This contract will be interacted with by Xchange.",
    "Liquidity, Loans, Lending Pool Overview\n\nIn order for a Swap to occur, there must be liquidity in the system. "
    "Liquidity can be summarized as capital, ETH, provided to create a token’s price. X7 Finance is designed to provide"
    " initial liquidity to the pair in the form of loans. Those loans are originated from the Lending Pool and pairs "
    "are hosted on Xchange.",
    "Lending Pool Funding\n\nThe Lending Pool is funded through two primary mechanism, by external deposits made by "
    "any wallet and through money owned by the system.",
    "System Owed Money\n\nTo fund the Lending Pool, ETH from the X7 token ecosystem has been accumulating in the "
    "Ecosystem Splitter and will be the first liquidity deposited into the Lending Pool. This ETH will be locked "
    "forever and will grow over time. Users are also able to contribute to the Lending Pool via Deposits. The code owns"
    " this money and it will never leave the system.",
    "External Deposits\n\nUsers will be able to deposit ETH and receive an X7 deposit token. When X7Deposit is minted,"
    " it is a face value equivalent to ETH.\n\n1 X7D = 1 ETH\n\nWhen deposited, the ETH will enter the Lending Pool and"
    " be available for automated lending. The Lending Pool will maintain a reserve of constellation tokens sufficient "
    "to back any externally funded Lending Pool liquidity. X7D tokens can be wrapped in an NFT and staked. At maturity,"
    " this NFT will pay returns based on the rising constellation token floor.",
    "Lending Functionality\n\nLending is a fully automatic process managed fully by Xchange’s interfacing with the "
    "Lending Pool via Initial Liquidity Loans.\n\nFor end-users, wanting to participate in lending: a user selects the "
    "amount of Ether to deposit or withdraw from the Lending Pool. Receipts for deposit are issued in X7 deposit, "
    "redeemable 1-to-1 with Eth, and may be staked for a portion of the loan fees.",
    "Initial Liquidity Loan\n\nAn initial liquidity loan provides a mechanism to add initial liquidity to an automated "
    "market making trading pair with borrowed capital. The terms and conditions for borrowing this capital and "
    "returning it to the lender provide for the lender and the borrower to manage their cost of capital and repayment "
    "schedules in a way that supports the nature of the offering and the size and duration of the loan.",
    "Initial Liquidity Loan Terms\n\nLoan terms are defined by standalone smart contracts that provide the following:"
    "\n\n1. Loan origination fee\n2. Loan retention premium fee schedule\n3. Principal repayment condition/maximum loan"
    " duration\n4. Liquidation conditions and Reward\n5. Loan duration",
    "Loan Liquidation\n\nAnyone may liquidate eligible loans through a transaction. Doing so will result in the "
    "borrowed capital being returned to the lender (Lending Pool or third-party lender) and the liquidator will receive"
    " the liquidation bounty.",
    "Initial Liquidity Loan Origination\n\nInitial Liquidity Loans can be funded in two ways, Lending Pool originated "
    "loans and Tokenized loans that may be fulfilled by any wallet.",
    "Lending Pool Origination\n\nIf the Lending Pool has sufficient liquidity to fund a loan, the loan will immediately"
    " be funded and the AMM liquidity pair will be created. Loan origination fees will be collected and proceeds will "
    "be distributed throughout the X7 ecosystem. A portion of the origination fee will feed back into the Lending Pool"
    " to grow the capital available for automatic lending.",
    "Tokenized Loans\n\nWhen a leveraged pair loan is requested that cannot be serviced due to insufficient liquidity "
    "within the Lending Pool, the request will cause an NFT to be minted. This NFT can be claimed by funding the loan, "
    "and results in an instantaneous return to the claimer of part of the loan origination fee. Possession of the NFT "
    "grants the holder a portion of the premium returns in the future as well as rights to claim the initial lent "
    "principal.\n\nThis mechanism will allow for a more effective bootstrapping period during which the Lending Pool "
    "may not have the proper liquidity to meet loan demand.\n\nIt will also provide a means for the lending platform "
    "to meet truly extraordinary lending requirements where third party liquidity providers can provide massive initial"
    " liquidity for an immediate return.\n\nSince these loans will be represented by ownership of an NFT and the "
    "benefits accrue to the owner of the NFT, the NFT itself may be transferred, auctioned, bought, sold, or held by "
    "smart contract to create a variety of ways that a lender may attempt to maximize their profit, limit their short "
    "term exposure, or otherwise draw upon their lent capital before the loan term concludes.\n\nDeFi participants are "
    "encouraged to create private “Lending Pools” that will attempt to fund loans (a risk less activity) and pay "
    "returns to liquidity providers. The X7 ecosystem will not provide this particular capability.",
    "Lending Terms Governance\n\nThe lending process delegates the loan terms to standalone smart contracts (see "
    "whitepaper for more details). These loan terms contracts must be deployed, and then “added” or “removed” from the "
    "Lending Pool as “available” loan terms for new loans. The DAO will be able to add or remove these term contracts."
    "\n\nLoan term contracts may be created by any interested third party, enabling a market process by which new loan"
    " terms may be invented, provided they implement the proper interface.",
    "Borrowing\n\nMuch in the same way an IPO is underwritten by a bank as a market maker, the X7 borrowing capability"
    " provides this capacity within the context of the Uniswap V2 automated market maker technology.\n\nThe core "
    "borrowing functionality within X7 applies to Initial Liquidity Offerings.\n\nThis capability allows for new "
    "liquidity pairs to be created with borrowed ETH. This lowers cost to launch a project, increase liquidity, and "
    "reduces the amount of capital locked to a pair.\n\nXchange’s intuitive UI will allow an easy selection of terms."
    " Simply select the amount you wish to borrow and the Initial Liquidity Loan term you want to use, and the number "
    "of tokens you wish to include in the pair.",
    "Borrower’s Liquidity Tokens\n\nLiquidity Tokens are sent to the borrower’s specified address and remain in full "
    "control by the borrower. The borrower is free to lock the liquidity in any service they wish, transfer or hold "
    "them. Liquidity Tokens are not able to be redeemed for the liquidity while a loan is active.",
    "Default\n\nIn the case of a default through any of the terms violated specified on the Initial Liquidity Loan, the"
    " Loan becomes eligible for liquidation."
    "All dynamic aspects of the X7 ecosystem will ultimately rest with the DAO to decide upon.\n\nThe DAO will be "
    "responsible for modifying tokenomics, changing profit allocation, upgrading the upgradeable components, and "
    "determining the long-term fate of locked liquidity.\n\nThe X7DAO token is the voting token within the DAO, and a "
    "portion of project revenue will flow into the DAO token in the form of liquidity injections.\n\n The expected "
    "outcome is that DAO holders will maximize the medium and long-term gain of the DAO token. The ecosystem properly "
    "aligns this selfish profit motive with the efficient and healthy operation of the ecosystem.",
    "Borrower’s Liquidity Tokens\n\nLiquidity Tokens are sent to the borrower’s specified address and remain in full "
    "control by the borrower. The borrower is free to lock the liquidity in any service they wish, transfer or hold "
    "them. Liquidity Tokens are not able to re be redeemed for the liquidity while a loan is active",
    "Default\n\nIn the case of a default through any of the terms violated specified on the Initial Liquidity Loan, the"
    " Loan becomes eligible for liquidation.",
    "Governance Charter\n\nAll dynamic aspects of the X7 ecosystem will ultimately rest with the DAO to decide upon."
    "\n\nThe DAO will be responsible for modifying tokenomics, changing profit allocation, upgrading the upgradeable "
    "components, and determining the long-term fate of locked liquidity.\n\nThe X7DAO token is the voting token within "
    "the DAO, and a portion of project revenue will flow into the DAO token in the form of liquidity injections.\n\n"
    "The expected outcome is that DAO holders will maximize the medium and long-term gain of the DAO token. The "
    "ecosystem properly aligns this selfish profit motive with the efficient and healthy operation of the ecosystem.",
    "Governance Control Structure\n\nThe DAO shall operate through central governance contracts. For all functions the "
    "DAO may control, there will be two options:\n\n1. Make the relevant change\n2. Delegate the authority to make "
    "those kinds of changes to an address.",
    "DAO configuration\n\nThe core quorum and proposal thresholds are not configurable.\n\nHowever, it is not known "
    "a-priori how rapid voting phases should be. There is a tradeoff between speed of execution and time for "
    "deliberation that must be balanced. The initial durations for each proposal phase will be set as a starting point."
    " However, these durations may be changed (within hard-coded limits) to meet future governance needs.",
    "*Proposals and Voting*\n\nVoting will occur in multiple phases, each of which has either a minimum or maximum "
    "time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake their tokens as "
    "X7sDAO, a non-transferable staked version of X7DAO.\n\nA quorum is reached when more than 50% of circulating "
    "X7DAO has been staked as X7sDAO.\n\nOnce a quorum is reached and a minimum quorum-seeking time period has "
    "passed, the X7sDAO tokens are temporarily locked (and no more X7DAO tokens may be staked until the next Quorum "
    "seeking period) and the governance process moves to the next phase\n\n*Phase 2: Proposal creation*\nA proposal "
    "is created by running a transaction on the governance contract which specifies a specific transaction on a "
    "specific contract (e.g. setFeeNumerator(0) on the X7R token contract).\n\nProposals are ordered, and any "
    "proposals that are passed/adopted must be run in the order that they were created.\n\nProposals can be made "
    "by X7sDAO stakes of 500,000 tokens or more. Additionally, holders of Magister tokens may make proposals. "
    "Proposals may require a refundable proposal fee to prevent process griefing.\n\n*Phase 3: Proposal voting*\n"
    "Each proposal may be voted on once by each address. The voter may specify the weight of their vote between 0 "
    "and the total amount of X7sDAO they have staked.\n\nProposals pass by a majority vote of the quorum of X7sDAO "
    "tokens.\n\nA parallel voting process will occur with Magister tokens, where each Magister token carries one "
    "vote.\n\nIf a majority of magister token holders vote against a proposal, the proposal must reach an X7sDAO vote "
    "of 75% of the quorum of X7sDAO tokens.\n\n*Phase 4: Proposal adoption*\nDuring this phase, proposals that have "
    "passed will be enqueued for execution. This step ensures proper ordering and is a guard against various forms of "
    "process griefing.\n\n*Phase 5: Proposal execution*\nAfter proposal adoption, all passed proposals must be executed"
    " before a new Quorum Seeking phase may commence.",
    "Process Adaptation\n\nSince any change that the core DAO governance process can control may be delegated, novel "
    "other mechanisms for voting may be created and changes can be delegated to that new process.\n\nFor example, a "
    "trusted group of individuals could be delegated control, and that trusted group could run an off-chain trustful "
    "process of voting.\n\nIf this process was ever corrupted, the DAO could regain trust-less on-chain control through"
    " a majority vote.\n\nThe X7 developers believe this governance structure will enable novel future governance "
    "innovation while never permanently relinquishing control to any external authority.",
    "Tokenized Governance\n\nThe X7 DAO structure is highly codified and provides almost no direct latitude for human "
    "intervention. This is by design and is one of the greatest strengths of the X7 DAO governance structure.\n\nThere"
    " is however a chance that through collusion and the inaction of DAO holders a large DAO holder could submit a "
    "proposal that was in their best interest and and not the best interest of the project.\n\n To help provide a check"
    " and balance, a maximum of 49 Magister tokens can be minted. Seven of these tokens were minted and given to the "
    "X7 development team. The other 42 may be minted for a fee.\n\n Any proposal may be vetoed by a majority of minted "
    "Magister tokens. It will require a ¾ super majority DAO vote to overturn a Magister veto.\n\n An additional side "
    "effect of this governance feature is that the original ecosystem developers will retain a level of authority at "
    "the beginning of DAO control handover, but this authority can and will be diluted as Magister tokens are minted. "
    "The final governance influence of the original developers will become minimal once all Magister tokens have been"
    " minted, and once 8 additional Magister tokens are minted the original developers will no longer maintain a "
    "controlling voting block on Magister votes.",
    "X7 ecosystem token Liquidity Provider Tokens (LP)\n\nThe original stealth launched tokens had their liquidity "
    "tokens sent to the burn wallet. This was to instill confidence in investors of a stealth launch that there was no"
    " intention or ability to withdraw the capital in the liquidity pairs.\n\nWhile the X7 ecosystem of smart contracts"
    " is being built with the flexibility and resilience to last, it is possible that eventually a systemic upgrade "
    "will need to take place. All X7 ecosystem tokens LP tokens (initial + auto liquidity) are being locked in a "
    "time-lock contract. The default destination for this LP will be the burn wallet and the starting lock time will "
    "be 2 years. The DAO will be able to perform any of the following actions on the time lock contract:\n\n1. Extend "
    "the time lock\n2. Change the receiver\n\nWhen the time lock expires, the receiver address will be able to "
    "withdraw any of the tokens in any amount. This will allow trust-less, contract driven migrations from the old "
    "tokens to new uses for that LP. If no action is taken the LP will remain locked as no transactions will ever be "
    "received from the dead address.",
    "Tokenomics\n\nA typical structure for funding project operations from tokens is to collect a percentage of traded"
    " tokens and periodically swap those tokens in the ETH pair.\n\nThe variables associated with this activity are:\n"
    "1. Percent of swap transaction tokens collected on buys and sells\n2. The token balance threshold at which to swap"
    " tokens into ETH\n3. The maximum swap transaction size (to limit extreme downward price action and maximize token"
    " return).\n4. Allocation of swapped ETH:\na. Collected for operations\nb. Buy back and burn\nc. Buy back and add "
    "liquidity\n\nAll of these settings will be dynamic and modifiable to affect the allocations of capital throughout "
    "the ecosystem.",
    "Advanced Trading and Revenues\n\nThere will be a complex interplay between the transfer of funds between:\n\n● The"
    " Lending Pool\n● The staked (pegged) ETH token\n● The “constellation” token liquidity sink\n● The reward token\n"
    "● The dao token\n\nAt various moments money will flow between the Lending Pool, the constellation tokens, and the"
    " staked ETH token, and opportunistic traders may find swing trading or arbitrage trading profitable. This swing "
    "trading will drive tokens and fees back into the rest of the ecosystem and provide a solid financial vehicle for "
    "speculation on future growth.\n\nThis kind of trading is intended for advanced traders. The full breadth of "
    "strategies this ecosystem will support are not known apriori and will be discovered.",
    "X7R\n\nIn order to attract as many interested parties into the ecosystem and ensure that the number of people "
    "that can benefit from this decentralized system is maximized, a deflationary “benefit” or “reward” token will "
    "exist that will receive buybacks, burns, and liquidity additions.\n\nThis token will be most interesting to retail"
    " investors that want to be exposed to the overall upside without significant effort on their part.\n\n At the "
    "start, this token will have a token fee associated with trading it, but it is expected that the DAO will lower "
    "that fee to zero once there is less need for ad-hoc manual capital injection.\n\nThis token is expected to "
    "eventually be traded on every major centralized exchange.",
    "X7DAO\n\nAn ERC20 governance token which allows holders to vote on fee rates, loan terms, funding terms, "
    "tradable token tax terms, distribution of capital flows and any additional settings on and off chain. This "
    "includes the establishment of committees and other foundational efforts off chain.\n\nThere is a complex interplay"
    " between the various tokens and contracts within the X7 ecosystem. While the X7 development team will seed these "
    "contracts with reasonable percentages, rates, terms, etc. the optimal values are not known apriori.\n\nHolders of"
    " X7DAO tokens will be able to participate in proposals to modify various settings across the ecosystem.\n\nA "
    "portion of lending and DEX revenue will flow into the X7DAO liquidity pair as buybacks and liquidity additions as"
    " well as direct rewards to X7DAO voters.",
    "X7Deposit (X7D)\n\nA wrapped ETH token will exist to encourage capital injection into the Lending Pool. Users will"
    " mint these X7Deposit tokens at a 1:1 face value of ETH.\n\nIn the beginning of the X7 ecosystem, this will be "
    "similar to holding ETH, and there will be zero risk to adding ETH to the Lending Pool.\n\nX7Deposit tokens may be"
    " staked for rewards in the form of a perpetual annuity that performs against the growth of liquidity within "
    "the system.",
    "Tokenized X7D Deposits\n\nWhen X7Deposit is staked an NFT is generated which records the following:\n\n1. Amount "
    "of X7D it is redeemable for\n2. The locked liquidity floor price of the constellation tokens\n3. The X7D Token "
    "lockup period\n\nAfter the maturity date, the holder of the NFT will be able to withdraw profit and re-stake or "
    "withdraw their X7Deposit.\n\nProfits are determined by comparing the locked liquidity floor price of the "
    "constellation tokens at staking time to the current locked liquidity floor price. A large portion of the "
    "lending proceeds will go towards buying back and adding locked liquidity to the constellation tokens. This "
    "activity provides a mechanism for calculating an actual return that reflects the profit from lending.\n\nStaked "
    "X7D NFTs will have an intrinsic value above the X7D/ETH redemption face value and may be traded on NFT markets as"
    " a form of a future on the Lending Pool returns.",
    "Non-Fungible Tokens\n\nOver the last few years there have been plenty of examples of NFTs selling jpegs. But NFTs "
    "within the X7 ecosystem will be pure utility.\n\nThe mint price and NFT capabilities may be controlled by the DAO"
    " to ensure that any benefits are net-neutral or net-positive to the X7 ecosystem.",
    "Tokenized Discounts and Benefits\n\nWithin the X7 ecosystem, various parts of the system incur fees. LP trading "
    "fees on the decentralized exchange, loan origination fees, loan interest, and token swap fees. Providing a limited"
    " set of NFTs that provide discounts and other benefits will enable power users and community members to "
    "significantly reduce their cost of use and encourage adoption.",
    "Future Developments\n\nThe X7 ecosystem provides mechanisms not only for individual investors and lenders to "
    "profit from the ecosystem activities but also for the flow of capital into the hands of the DAO (and its "
    "delegates).\n\nOur expectation is that these funds will at first be focused on marketing and business development "
    "activities, but then in the future will fund other kinds of project needs, such as additional features and "
    "components to the blockchain ecosystem and the user interface.\n\nWe would find it plausible that the DAO could "
    "choose to contract out the development of novel loan term contracts or whole new sources of revenue for the "
    "project (which could in turn contribute to the ecosystem splitter).\n\nBelow is a non-exhaustive list of possible "
    "future developments.\n\n● Launch accessory services\n○ Token and Initial Liquidity Lockers\n○ Launchpad services"
    "\n○ Trust-less consensus-driven code audit services\n● Advanced Trading\n○ Leveraged trading capabilities, "
    "building on learned experience from leveraged initial liquidity and capital-protecting liquidity pairs\n○ Wrapped"
    " assets to expose the holder to various levels of profit exposure within the X7 ecosystem\n● Liquidity pairs with"
    " configurable or alternative automated marketing making capabilities\n● Non-native token (ETH, BNB, etc.) "
    "initial liquidity loans\n",
]

x_replies = [
    "Raid!",
    "LFG",
    "Send it!",
    "X raid!",
    "Like and repost!",
    "GO GO GO!",
    "X7 Force!",
    "Raid it Fam!",
    "Blow it up!",
    "Full force!",
    "Light it up!",
    "Shill time!",
    "Smash it!",
    "Slap it!",
    "Send it!",
    "If Phlux says it, You do it!",
    "Phlux it up!",
    "Full Send!",
    "Hit it Hard!",
    "Insert inspirational raid quote here!",
    "Let them know!",
    "RAIIIIIIIIIID",
    "For the Culture",
    "WAGMI",
    "Elon says repost",
    "Have you reached your X cap?",
    "For the win!",
    "Xcellent",
    "X fingers on fire!",
    "X like no tomorrow!",
    "Make waves on X!",
    "Ignite the reposts!",
    "Shout it from the X rooftops!",
    "Leave no X unliked!",
    "Conquer the Xverse!",
    "Go viral or go home!",
    "Engage the X!",
    "A X a day keeps the boredom away!",
    "X like nobody's watching!",
    "Unleash the Xstorm!",
    "X is calling, answer with a roar!",
    "Fuel the X hype train!",
    "X with the strength of a thousand hashtags!",
    "Let your X be the talk of the town!",
    "One X to rule them all!",
    "X, repost, conquer!",
    "Be the hero X needs!",
    "X your way to the top!",
    "X like a champion!",
    "Unleash your X prowess!",
    "Craft X that mesmerize!",
    "Elevate your X to new heights!",
    "X your way to stardom!",
    "Join the X elite!",
    "Master the art of the X!",
    "X with unyielding passion!",
    "Become a force to be reckoned with on X!",
    "Ignite the Xverse with your words!",
    "Spread X magic across the timeline!",
    "X with a purpose and leave an impact!",
    "Unleash your inner X influencer!",
    "Make your X the talk of the town!",
    "Unlock the secrets of X success!",
    "X fearlessly and embrace the reposts!",
    "Craft X that capture hearts and minds!",
    "Infuse your X with boundless creativity!",
    "Harness the power of the hashtag!",
    "X like a superstar and soar high!",
    "Make your X resonate with the masses!",
    "Become the X trendsetter you were meant to be!",
    "X with style, substance, and a touch of pizzazz!",
    "X like there's no tomorrow!",
    "Unleash your X superpowers!",
    "Level up your X!",
    "Join the X revolution!",
    "Repost with unstoppable passion!",
    "Make your reposts legendary!",
    "Master the art of the X!",
    "Become a X sensation!",
    "Dare to repost the impossible!",
    "Conquer the Xverse with your words!",
    "Repost your dreams into reality!",
    "Unlock the true potential of this X!",
    "Spread X joy with every X!",
    "Repost your way to greatness!",
    "Ignite the X fire within!",
    "Unleash the power of your X!",
    "Make this X go viral!",
    "Rule the X feed with an iron thumb!",
    "X boldly and fearlessly!",
    "Repost to make make heads turn!",
    "Amplify your message with every X!",
    "Repost to resonate with the world!",
    "Craft reposts that leave a lasting impact!",
]

voting = (
    "*Proposals and Voting*\n\nVoting will occur in multiple phases, each of which has either a minimum or maximum"
    " time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake their tokens as "
    "X7sDAO, a non-transferable staked version of X7DAO.\n\nA quorum is reached when more than 50% of circulating "
    "X7DAO has been staked as X7sDAO.\n\nOnce a quorum is reached and a minimum quorum-seeking time period has "
    "passed, the X7sDAO tokens are temporarily locked (and no more X7DAO tokens may be staked until the next Quorum"
    " seeking period) and the governance process moves to the next phase\n\n*Phase 2: Proposal creation*\nA "
    "proposal is created by running a transaction on the governance contract which specifies a specific transaction"
    " on a specific contract (e.g. setFeeNumerator(0) on the X7R token contract).\n\nProposals are ordered, and any"
    " proposals that are passed/adopted must be run in the order that they were created.\n\nProposals can be made "
    "by X7sDAO stakes of 500,000 tokens or more. Additionally, holders of Magister tokens may make proposals. "
    "Proposals may require a refundable proposal fee to prevent process griefing.\n\n*Phase 3: Proposal voting*\n"
    "Each proposal may be voted on once by each address. The voter may specify the weight of their vote between 0 "
    "and the total amount of X7sDAO they have staked.\n\nProposals pass by a majority vote of the quorum of X7sDAO "
    "tokens.\n\nA parallel voting process will occur with Magister tokens, where each Magister token carries one "
    "vote.\n\nIf a majority of magister token holders vote against a proposal, the proposal must reach an X7sDAO "
    "vote of 75% of the quorum of X7sDAO tokens.\n\n*Phase 4: Proposal adoption*\nDuring this phase, proposals that"
    " have passed will be enqueued for execution. This step ensures proper ordering and is a guard against various "
    "forms of process griefing.\n\n*Phase 5: Proposal execution*\nAfter proposal adoption, all passed proposals "
    "must be executed before a new Quorum Seeking phase may commence."
)