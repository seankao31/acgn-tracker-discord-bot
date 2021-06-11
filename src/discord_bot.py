from discord.ext import commands


bot = commands.Bot(command_prefix='!acgn')

with open('BOT_TOKEN.txt', 'r') as token_file:
    TOKEN = token_file.read()
    bot.run(TOKEN)
