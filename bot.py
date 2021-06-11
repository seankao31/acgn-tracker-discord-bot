from src.discord_bot import bot


with open('BOT_TOKEN.txt', 'r') as token_file:
    TOKEN = token_file.read()
    bot.run(TOKEN)
