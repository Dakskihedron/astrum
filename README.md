# Kitakami

Kitakami is a small lightweight Discord bot written in Python and powered by discord.py. Kitakami is designed to operate in low population servers where all members are assigned their own individual customisable roles.

Kitakami requires the following libraries:
- discord.py
- python-dotenv
- lxml
- requests
- beautifulsoup4

Kitakami can be launched via pm2 with the included pm2.json script. The script requires Python 3.8. The `.env-template` file will have to be renamed to `.env` and a Discord bot token has to be provided where `[discord_bot_token]` is in order for the bot to work.
