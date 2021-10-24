#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from utils import LOGGER
from contextlib import suppress
from config import Config
import calendar
import pytz
from datetime import datetime
import asyncio
import os
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, 
    MessageNotModified
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from utils import (
    cancel_all_schedules,
    edit_config, 
    is_admin, 
    leave_call, 
    restart,
    restart_playout,
    stop_recording, 
    sync_to_db,
    update, 
    is_admin, 
    chat_filter,
    sudo_filter,
    delete_messages,
    seek_file
)
from pyrogram import (
    Client, 
    filters
)

IST = pytz.timezone(Config.TIME_ZONE)
if Config.DATABASE_URI:
    from utils import db

HOME_TEXT = "<b>Hey  [{}](tg://user?id={}) 🙋‍♂️\n\nIam A Bot Built To Play or Stream Videos In Telegram VoiceChats.\nI Can Stream Any YouTube Video Or A Telegram File Or Even A YouTube Live.</b>"
admin_filter=filters.create(is_admin) 


@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Play", callback_data='help_play'),
                InlineKeyboardButton("Settings", callback_data=f"help_settings"),
                InlineKeyboardButton("Recording", callback_data='help_record'),
            ],
            [
                InlineKeyboardButton("Scheduling", callback_data="help_schedule"),
                InlineKeyboardButton("Controling", callback_data='help_control'),
                InlineKeyboardButton("Admins", callback_data="help_admin"),
            ],
            [
                InlineKeyboardButton("Misc", callback_data='help_misc'),
                InlineKeyboardButton("Config Vars", callback_data='help_env'),
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
        )
    if message.chat.type != "private" and message.from_user is None:
        k=await message.reply(
            text="I cant help you here, since you are an anonymous admin. Get help in PM",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"Help", url=f"https://telegram.dog/{Config.BOT_USERNAME}?start=help"),
                    ]
                ]
            ),)
        await delete_messages([message, k])
        return
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        "Learn to use the VCPlayer, Showing help menu, Choose from the below options.",
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
