from telegram import *
from telegram.ext import *

from data import  text


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


async def show_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
        group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
        channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
        text = (
            f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}.\n"
            f"It is a member of the groups with IDs {group_ids}\n"
            f"and administrator in the channels with IDs {channel_ids}.\n"
        )
        await update.effective_message.reply_text(text)
    else:
        await update.message.reply_text(f"{text.mods_only}")