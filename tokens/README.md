<p align="center">
  <img src="https://assets.x7finance.org/images/svgs/x7.svg" alt="X7 Banner Logo" />
</p>

<br />
<div align="center"><strong>X7 Finance</strong></div>
<div align="center">Trust No One. Trust Code. Long Live DeFi</div>
<div align="center">X7 is a completely decentralized exchange - complete with it's innovative lending protocols.</div>
<br />
<div align="center">
<a href="https://www.x7finance.org/">Website</a> 
<span> · </span>
<a href="https://t.me/X7m105portal">Telegram</a> 
<span> · </span>
<a href="https://twitter.com/X7_Finance">Twitter</a>
</div>

##

### List your token on @X7Finance_bot

The following steps will guide you through how to list your token on @X7Finance_bot

##

### Create a new branch 

Create a new branch from 'main' on this repository

https://github.com/x7finance/telegram-bot/branches/new

### Create listing

Create a new file in the 'tokens' directory 

```bash
yourtokenname.py
```

with the folllowing lines:

```bash
from tokens import TokensInfo


info = TokensInfo(
    name="token-name",
    ca="token-contract-address",
    pair="pair-address",
    chain="deployed-chain",
    logo="logo-url"
)
```

Please ensure the "" remain

Token logo is optional, please make sure the file is no larger than 200x200px, if you do not submit a logo please use

```bash
logo=""
```

Save and commit your changes to your new branch

### Submit Listing

Open a new Pull Request to merge your branch into main

https://github.com/x7finance/telegram-bot/pulls

On approval your token will be added to the price bot

##