import asyncio
import typing
from itertools import cycle

from discord.ext import commands


class CustomStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_on = False

    @commands.command()
    async def custom_status(self, ctx, arg: typing.Optional[str] = 'start'):
        await ctx.message.delete()

        if arg == 'stop':
            if self.is_on:
                print('Turning off custom status...')
                self.is_on = False
            else:
                print("Custom status is not on.")
        elif arg == 'start':
            print('Turning on custom status...')
            self.is_on = True
            # todo: make statuses customizable via command
            statuses = cycle([
                {"custom_status": {"text": '', "emoji_name": "🐍"}},
                {"custom_status": {"text": '', "emoji_name": "🌗"}}
            ])
            await self.bot.loop.create_task(self._change_status(statuses))
        else:
            print('Invalid argument.')

    async def _change_status(self, statuses):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed() and self.is_on:
            current_status = next(statuses)
            await self.bot.user.edit_settings(**current_status)
            await asyncio.sleep(3)
        self.is_on = False
        await self.bot.user.edit_settings(**{'custom_status': None})


def setup(bot):
    bot.add_cog(CustomStatusCog(bot))
