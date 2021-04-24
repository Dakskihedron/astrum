import datetime

github_link = "https://github.com/Dakskihedron/kitakami"

eightball_responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes - definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook is good",
    "Very doubtful"  
]

nsfw_blacklist = [
    "loli",
    "lolicon",
    "shota",
    "shotacon",
    "cub"
]

def date(target):
    return target.strftime("%a, %d %b %Y @ %I:%M:%S %p")