
from telegram import *
from telegram.ext import *

import os
from typing import Optional, Tuple

from constants import url
from hooks import api
import media


RESTRICTIONS = {
    'can_send_messages': False,
    'can_send_media_messages': False,
    'can_send_other_messages': False,
    'can_add_web_page_previews': False,
}


async def button_callback(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    action, _ = update.callback_query.data.split(":", 1)

    if action == "unmute":
        user_restrictions = {key: True for key in RESTRICTIONS}

        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=user_restrictions,
        )
        try:
            previous_welcome_message_id = context.bot_data.get('welcome_message_id')
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=previous_welcome_message_id)
        except Exception:
            pass


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:    
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.effective_message.id
        )
    except Exception:
        return


async def member(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    channel_id = update.effective_chat.id
    if str(channel_id) == os.getenv("MAIN_TELEGRAM_CHANNEL_ID"):
        result = await member(update.chat_member)
        if result is None:
            return

        was_member, is_member = result
        new_member = update.chat_member.new_chat_member
        new_member_id = new_member.user.id
        if new_member.user.username:
            new_member_username = f"@{new_member.user.username}"
        else:
            if new_member.user.last_name:
                new_member_username = f"{new_member.user.first_name} {new_member.user.last_name}"
            else:
                new_member_username = new_member.user.first_name

        if not was_member and is_member:
            previous_welcome_message_id = context.bot_data.get('welcome_message_id')
            if previous_welcome_message_id:
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=previous_welcome_message_id)
                except Exception:
                    pass

            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=new_member_id,
                permissions=RESTRICTIONS,
            )
            welcome_message = await update.effective_chat.send_video(
                video=open(media.WELCOMEVIDEO, 'rb'),
                caption=(
                    f"Welcome {api.escape_markdown(new_member_username)} to X7 Finance\n\n"
                    f"Home of Xchange - A censorship resistant DEX offering initial loaned liquidity across;\n\n"
                    f"• Ethereum\n"
                    f"• Binance Smart Chain\n"
                    f"• Arbitrum\n"
                    f"• Optimism\n"
                    f"• Polygon\n"
                    f"• Base Chain\n\n"
                    f"Verify as human and check out the links to get started!"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="I am human!",
                                callback_data=f"unmute:{new_member_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="Website",
                                url=url.WEBSITE,
                            ),
                            InlineKeyboardButton(
                                text="Xchange",
                                url=url.XCHANGE,
                            ),
                        ],
                    ]
                )
            )

            context.bot_data['welcome_message_id'] = welcome_message.message_id