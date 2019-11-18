from discord.ext import commands


class EmojifyCog(commands.Cog):
    ABC = 'abcdefghijklmnopqrstuvxwyz'
    SPECIAL_CHARS = {
        ' ': '   ',
        '!': ':exclamation:',
        '?': ':question:',
        '1': ':one:', '2': ':two:', '3': ':three:', '4': ':four:', '5': ':five:', '6': ':six:', '7': ':seven:',
        '8': ':eight:', '9': ':nine:', '0': ':zero:',
        '#': ':hash:',
        '*': ':asterisk:'
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def emojify(self, ctx, *, arg):
        emojified = []
        for char in arg:
            emojified.append(self.SPECIAL_CHARS.get(char, f':regional_indicator_{char}:' if char in self.ABC else char))
        await ctx.message.edit(content=''.join(emojified))


def setup(bot):
    bot.add_cog(EmojifyCog(bot))
