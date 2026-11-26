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
import asyncio
from pyrogram import Client, idle
from pyromod import listen
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats


SET_CMDS = True

BOT_TOKEN = "......"

bot = Client(
    name="One",
    api_id=8186557,
    api_hash="efd77b34c69c164ce158037ff5a0d117",
    bot_token=BOT_TOKEN,
    plugins=dict(root="Maker")
)

bot_id = BOT_TOKEN.split(":")[0]


async def start_bot():
    await bot.start()
    print("[BOT] Bot started")

    if SET_CMDS:
        try:
            commands = [
                BotCommand("start", "Start the bot"),
                BotCommand("kim", "About developer"),
                BotCommand("vega", "Source code"),
            ]
            await bot.set_bot_commands(commands, scope=BotCommandScopeAllPrivateChats())
        except Exception as e:
            print(f"[BOT] set_bot_commands error: {e}")

        try:
            await bot.send_message(481322119, "<b>تم تشغيل النظام بنجاح</b>")
        except Exception as e:
            print(f"[BOT] notify admin error: {e}")

    await idle()
    try:
        if bot.is_connected:
            await bot.stop()
    except Exception:
        pass


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[MAIN] خطأ: {e}")
    finally:
        loop.close()