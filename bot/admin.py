from telegram import *
from telegram.ext import *
from datetime import datetime, timedelta
import os

from data import  text, times


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        await update.message.reply_text(
            f"{text.admin_commands}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Rose Bot Anti-flood",
                            url="https://missrose.org/guide/antiflood/",
                        )
                    ],
                ]
            ),
        )
    else:
        await update.message.reply_text(f"{text.mods_only}")


async def games_lock(update, context):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        chat_id = update.message.chat_id
        context.chat_data[chat_id] = True
        await update.message.reply_text(f"Games locked in this chat. Play in private chat with @x7finance_bot or a group that is not locked.")
    else:
        await update.message.reply_text(f"{text.mods_only}")
    

async def games_unlock(update, context):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        chat_id = update.message.chat_id
        context.chat_data[chat_id] = False
        await update.message.reply_text("Games are now unlocked in this chat.")
    else:
        await update.message.reply_text(f"{text.mods_only}")


async def wen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == int(os.getenv("OWNER_TELEGRAM_CHANNEL_ID")):
        if times.button_time is not None:
            time = times.button_time
        else:    
            time = times.first_button_time
        target_timestamp = times.restart_time + time
        time_difference_seconds = target_timestamp - datetime.now().timestamp()
        time_difference = timedelta(seconds=time_difference_seconds)
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await update.message.reply_text(f"Next Click Me:\n\n{hours} hours, {minutes} minutes, {seconds} seconds")
    else:
        await update.message.reply_text(f"{text.mods_only}")
 