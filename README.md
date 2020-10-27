# Kitakami

Kitakami is a small lightweight Discord bot written in Python and powered by discord.py. Kitakami is designed to operate in low population servers where all members are assigned their own individual customisable roles.

Kitakami requires the following libraries:
- discord.py
- python-dotenv
- lxml
- requests
- beautifulsoup4

Which can be installed using the command `pip install -r requirements.txt`.

Required environment variables:
- `DISCORD_TOKEN=[bot_token]`
- `DISCORD_PREFIX=[prefix]`

If the bot is hosted on your own machine, the environment variables will need to go in a file named `.env`, in the root folder.
