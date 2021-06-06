# Astrum

Some Discord bot with role editing commands so you can stop asking your friend, the admin of the private server, to change your role name and colour for you. Besides that, there's a few misc and fun commands.

Required libraries can be installed using the command `pip install -r requirements.txt`

Format for environment variables:
```
DISCORD_TOKEN=[discord_bot_token]
BOT_PREFIX=[bot_prefix]
NASA_API_KEY=[nasa_api_key]
OWM_API_KEY=[open_weather_map_api_key]
```

The bot was designed to be hosted on Heroku − provide environment variables in Settings/Config Vars. However, it can also be hosted on a local machine − you will need to create a file named `.env` in the root folder and provide environment variables in the format shown above (minus the square brackets).
