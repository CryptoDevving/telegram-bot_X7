from telegram import *
from telegram.ext import *

import os, pytz, random, requests
from datetime import datetime
from dateutil import parser

from constants import text, url
from hooks import api
import media


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    tweet = context.args[0]
    start = tweet.index("status/")
    end = tweet.index("?", start + 1)
    tweet_id = tweet[start + 7 : end]
    response = api.twitter_v2.get_retweeters(tweet_id)
    status = api.twitter.get_status(tweet_id)
    retweet_count = status.retweet_count
    rt_names = "\n".join(f"{p}" for p in response.data)
    await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
    await update.message.reply_text(
        f"Reposted {retweet_count} times, by the following members:\n\n{rt_names}"
    )


async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        tweet = context.args[0]
        start = tweet.index("status/")
        end = tweet.index("?", start + 1)
        tweet_id = tweet[start + 7 : end]
        response = api.twitter_v2.get_retweeters(tweet_id)
        status = api.twitter.get_status(tweet_id)
        retweet_count = status.retweet_count
        rt_names = "\n".join(f"{p}" for p in response.data)
        await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
        await update.message.reply_text(f"{retweet_count} Entries:\n\n{rt_names}")
        await update.message.reply_text(
            f"The Winner is....\n\n{random.choice(response.data)}\n\n"
            f"Congratulations, Please DM @X7_Finance on X to verify your account"
        )
    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")


async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        username = random.choice(text.usernamelist)
        tweet = api.twitter.user_timeline(
            screen_name=username, count=1, include_rts="false", exclude_replies="true"
        )
        await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
        await update.message.reply_text(
            f"🚨🚨 Raid {username} 🚨🚨\n\n"
            f"{tweet[0].text}\n\n"
            f"https://twitter.com/intent/tweet?text=@X7_Finance&hashtags=LongLiveDefi&in_reply_to={tweet[0].id}\n\n"
            f"{random.choice(text.X_REPLIES)}",
            disable_web_page_preview=True,
        )
    else:
        await update.message.reply_text(f"{text.MODS_ONLY}")


async def spaces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    response = api.twitter_v2.get_spaces(user_ids=1561721566689386496)
    if response[0] is None:
        await update.message.reply_photo(
            photo=f"{url.PIONEERS}{api.get_random_pioneer_number()}.png",
            caption=f"X7 Finance X space\n\nPlease check back for more details"
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )
    else:
        data = f"{response[0]}"
        start = data.index("=")
        end = data.index(" ", start)
        space_id = data[start + 1 : end]

        def get_space():
            url = f"https://api.twitter.com/2/spaces/{space_id}?space.fields=scheduled_start,title"
            headers = {
                "Authorization": "Bearer {}".format(os.getenv("TWITTER_BEARER")),
                "User-Agent": "v2SpacesLookupPython",
            }
            response = requests.request("GET", url, headers=headers)
            result = response.json()
            return result["data"]

        space = get_space()
        then = parser.parse(space["scheduled_start"]).astimezone(pytz.utc)
        duration = then - datetime.utcnow()
        days, hours, minutes = api.get_duration_days(duration)
        await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
        await update.message.reply_text(
            text=f"Next X7 Finance X space:\n\n"
            f'{space["title"]}\n\n'
            f'{then.strftime("%A %B %d %Y %I:%M %p")} UTC\n\n'
            f"{days} days, {hours} hours and {minutes} minutes\n\n"
            f"[Click here](https://twitter.com/i/spaces/{space_id}) to set a reminder!"
            f"\n\n{api.get_quote()}",
            parse_mode="Markdown",
        )


async def tweet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    ext = " ".join(context.args)
    username = "@x7_finance"
    if ext == "":
        try:
            tweet = api.twitter.user_timeline(
                screen_name=username, count=1, exclude_replies=True, include_rts=False
            )
            await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
            await update.message.reply_text(
                f"Latest X7 Finance X Post\n\n{tweet[0].text}\n\n"
                f"{url.TWITTER}status/{tweet[0].id}\n\n"
                f"{random.choice(text.X_REPLIES)}"
            )
        except Exception as e:
            await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
            await update.message.reply_text(
                f"*X7 Finance X*\n\n" f"{random.choice(text.X_REPLIES)}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="X7 Finance X",
                                url=f"{url.TWITTER}",
                            )
                        ],
                    ]
                ),
            )
    if ext == "count":
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            tweet = api.twitter.user_timeline(
                screen_name=username, count=1, exclude_replies=True, include_rts=False
            )
            response = api.twitter_v2.get_retweeters(tweet[0].id)
            status = api.twitter.get_status(tweet[0].id)
            retweet_count = status.retweet_count
            count = "\n".join(f"{p}" for p in response.data)
            await update.message.reply_sticker(sticker=media.TWITTER_STICKER)
            await update.message.reply_text(
                f"Latest X7 Finance Tweet\n\n{tweet[0].text}\n\n"
                f"{url.TWITTER}status/{tweet[0].id}\n\n"
                f"Retweeted {retweet_count} times, by the following members:\n\n{count}"
            )
        else:
            await update.message.reply_text(f"{text.MODS_ONLY}")
