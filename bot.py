from discord.ext import commands


bot = commands.Bot(command_prefix='self.', self_bot=True)


extensions = [
    'cogs.recite',
    'cogs.emojify',
    'cogs.custom_status',
    'cogs.pokemon'
]


if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    bot.remove_command('help')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run('TOKEN HERE', bot=False)
