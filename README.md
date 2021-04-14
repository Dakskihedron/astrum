# Kitakami

Kitakami is a Discord bot written in Python and powered by discord.py. Kitakami is designed to operate in low population servers where all members are assigned their own individual customisable roles.

Kitakami requires the following libraries:
- discord.py
- python-dotenv
- lxml
- requests
- beautifulsoup4

which can all be installed using the command `pip install -r requirements.txt`

Required environment variables:
```
DISCORD_TOKEN=[bot_token]
DISCORD_PREFIX=[bot_prefix]
```

The bot was designed to be hosted using Heroku - just make sure to provide the environment variables in Settings/Config Vars. If you decide to host the bot on your own machine, you will need to create a file named `.env` in the root folder, and put the environment variables in it in the format shown above (minus the brackets).
