from telegram import *
from telegram.ext import *

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
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        hours, remainder = divmod(times.button_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        await update.message.reply_text(
            f"Next Click Me:\n\n{hours} hours and {minutes} minutes and {seconds} seconds")
    else:
        await update.message.reply_text(f"{text.mods_only}")
 