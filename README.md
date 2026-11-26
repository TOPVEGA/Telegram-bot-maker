<div align="center">

# 🤖 VEGA Telegram Bot Manager

**A Pyrogram-based Telegram bot management system with child-bot creation, administration, broadcasting, and server monitoring.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Framework-Pyrogram-2CA5E0?style=for-the-badge)](https://docs.pyrogram.org/)
[![Redis](https://img.shields.io/badge/Database-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)

**VEGA & Logic** · By [@TopVeGa](https://t.me/TopVeGa)

</div>

## Features

### User interface
- Interactive private-chat control panel built with inline and rich Telegram buttons.
- Separate user and administrator menus.
- Callback-based navigation between management sections.
- Conversation state tracking for multi-step actions.
- `/start` entry point and `/cancel` to clear a user's pending workflow.

### Bot management
- Create a child bot through a guided flow that requests a BotFather token and session information.
- Store child-bot records in Redis.
- Start or stop an individual child bot.
- Start or stop all registered child bots.
- List registered bots and remove individual bots.
- Update child bots and perform bulk deletion.
- Run child bot processes in GNU Screen sessions.

### Statistics and monitoring
- Global and per-bot statistics.
- Bot status checks and filtering.
- Server information, system information, and installation information.
- List available Screen sessions.

### Session and account tools
- Change the configured session through the interactive workflow.
- Remove an account through the account-management flow.
- The source also contains a multi-session workflow that attempts channel joins and repeated `/start` interactions. Use this only with accounts and destinations you own or are explicitly authorized to test, and comply with Telegram's rules. It can trigger rate limits or account restrictions.

### Broadcast and user registry
- Maintain the private-chat user registry in Redis.
- Send a copied-message broadcast.
- Forward a message to registered users.
- Copy and pin a broadcast message where Telegram permissions allow.
- Track successful and failed deliveries and remove users that return `PeerIdInvalid`.
- Export the user list to a text backup and import user IDs from a `.txt` document.

### Administration and access control
- Promote and demote administrators.
- View administrator lists and the current user's permissions.
- Block and unblock users.
- View and clear the blocked-user list.
- Open or close the bot-creation system.
- Enable or disable user-to-owner message forwarding.
- Optional channel-membership checking with an in-memory cache.

### Developer and source information
- `/kim` displays the configured developer profile information.
- `/vega` (also registered in the source as `/One`) sends the project's source/promotional information.
- Startup attempts to register Telegram bot commands and notify a configured administrator.

## Project structure

```text
مصنع/
├── bot.py              # Creates the main Pyrogram client and starts the bot
├── main.py             # Main launcher; invokes start_bot()
├── requirements.txt    # Python package requirements
├── setup               # Bash installer for system and Python dependencies
├── start               # Simple launcher script
└── Maker/
    ├── __init__.py
    └── Maker.py        # Main plugin: menus, callbacks, Redis data, workflows
```

## Technology stack

- **Python** — application runtime.
- **Pyrogram** — Telegram Bot API client and update handlers.
- **Pyromod** — conversational input/listening support.
- **Redis** — persistent bot registry, user lists, blocked users, and workflow flags.
- **GNU Screen** — detached child-bot process management.
- **aiohttp** — asynchronous HTTP requests, including rich-message API calls.
- **PyTgCalls / ntgcalls** — included in the declared dependency set.
- **FFmpeg** — installed by the setup script.
- **Additional packages** — see `requirements.txt`.

## Installation

The included `setup` script targets Debian/Ubuntu-style Linux systems and uses `apt`, `sudo`, `pip3`, and Node.js/npm. Review the script before running it.

1. Install Python 3, pip, Git, Redis, GNU Screen, and FFmpeg on the host.
2. Configure a reachable Redis instance and its connection URL.
3. Install the Python dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Configure the values described in [Configuration](#configuration).
5. Ensure the child-bot template and plugin package expected by the source are present (see [Project limitations](#project-limitations)).
6. Start the application:

   ```bash
   bash start
   ```

   Or run:

   ```bash
   python3 main.py
   ```

## Configuration

The supplied `bot.py` currently contains hard-coded configuration values and a placeholder bot token. Before running the project, review and configure:

| Setting | Purpose |
|---|---|
| `BOT_TOKEN` in `bot.py` | Token of the manager bot, obtained from BotFather |
| `API_ID` and `API_HASH` | Telegram application credentials |
| `REDIS_URL` in `Maker/Maker.py` | Redis connection URL; the supplied default is a placeholder |
| `SUDOS` | Telegram user IDs with sudo-level access |
| `ADMINS` | Additional administrator IDs; initialized as an empty list |
| `Channel` | Channel used by the membership-check function |
| `channels_one` | Channel list used by the session workflow |
| `Channel_Name` | Display name used in bot messages |

The child-bot creation flow writes a `.env` file for each generated bot containing `BOT_USERNAME`, `BOT_TOKEN`, `SESSION`, `OWNER_ID`, and `LOGGER_ID`.

**Security:** Never publish bot tokens, API hashes, session strings, or Redis credentials. Do not commit real credentials to a public repository. If any real credential has already been exposed, revoke or rotate it.

## Runtime data

The source uses Redis keys scoped by the manager bot ID. These include:
- `users:<bot_id>` — registered user IDs.
- `bots:<bot_id>` — child-bot usernames and owner IDs.
- `blocked:<bot_id>` — blocked user IDs.
- `chats:<bot_id>` — stored chat IDs.
- Additional per-user keys for pending states, broadcast modes, and communication settings.

Child bot files are expected under `Maked/<username>/`, while Screen session names are derived from bot usernames.

## Commands

| Command | Description |
|---|---|
| `/start` | Open the bot's start/menu flow |
| `/kim` | Show developer information |
| `/vega` | Send source/project information |
| `/One` | Alias handled by the source-information handler |
| `/cancel` | Clear the current user's pending operations |

The control panel exposes additional actions through buttons rather than separate text commands.

## Project limitations

The supplied ZIP contains only nine archive entries. The inspected source references files and runtime components that are **not present in this archive**, including:
- A `Make/` child-bot template directory copied during bot creation.
- A child-bot `plugins` package launched with `python3 -m plugins`.
- A Redis service and GNU Screen on the host.

The dependency list also does not explicitly declare every imported package visible in the source (notably `redis` and `pytz`). Verify and install the required packages for the exact deployment environment. As supplied, the archive should not be assumed to be a complete, immediately runnable deployment.

The setup script writes a sample `.env` file, but the manager source shown here reads its primary token and several settings directly from Python code. Review the configuration flow before relying on `.env` alone.

## Responsible use

Operate the bot only in chats, channels, and accounts where you have permission. Respect Telegram rate limits, user privacy, platform terms, copyright, and the licenses of all third-party dependencies and media. Broadcasting and automated account actions should be limited to opted-in users and authorized tests.

## Credits

**VEGA**  
Developer reference in source: [@TopVeGa](https://t.me/TopVeGa)

Copyright and third-party rights remain with their respective owners. Check the original project license and dependency licenses before redistribution.

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                       Copyright | Footer                              -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:3B82F6,100:0F172A&height=4&width=40%&section=header" />
  <br><br>
  <p style="color: #9CA3AF; font-size: 14px;">
    <b style="color: #3B82F6;">Brand:</b> VEGA &amp; Logic &nbsp;|&nbsp;
    <b style="color: #3B82F6;">Copyright:</b> © 2015 - 2025
  </p>
  <p style="color: #6B7280; font-size: 12px;">
  </p>
</div>
<br>
<!-- Smooth Gradient Footer Background -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3B82F6,50:1E3A8A,100:0F172A&height=120&section=footer" width="100%" />

