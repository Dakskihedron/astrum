import datetime

github_link = "https://github.com/Dakskihedron/kitakami"

eightball_responses = [
    "it is certain",
    "it is decidedly so",
    "without a doubt",
    "yes - definitely",
    "you may rely on it",
    "as I see it, yes",
    "most likely",
    "outlook good",
    "yes",
    "signs point to yes",
    "reply hazy, try again",
    "ask again later",
    "better not tell you now",
    "cannot predict now",
    "concentrate and ask again",
    "don't count on it",
    "my reply is no",
    "my sources say no",
    "outlook is good",
    "very doubtful"  
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