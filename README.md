# Astrum
Another Discord.py bot, with commands for editing individual user roles.
## Hosting
### Heroku
The bot has been designed to be hosted on Heroku. Environment variables will have to be provided in Settings/Config Vars on Heroku. The required variables can be found in the `.env-template` file. The required Python runtime and libraries will be automatically installed.
### Local Machine
The bot can be hosted on local machine such as a Raspberry Pi. You will need to rename the `.env-template` file to `.env` and provide the environment variables. Make sure Python 3.9 or newer is installed. The required libraries can be installed using:
```
pip install -U -r requirements.txt
```
## Additional Info
For the Danbooru API command, you will need to create a JSON file: `config.json` in the main directory, of which contains a key: `blacklist` with an array of blacklisted search tags for Danbooru. Otherwise the command will be disabled. An example of the JSON is shown below:
```
{
    "blacklist": [
        "list",
        "of",
        "blacklisted",
        "tags"
    ]
}
```