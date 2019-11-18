import asyncio
import os
from pathlib import Path
from random import randint

from discord.ext import commands


class LoopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_reciting = False
        self.text_path = Path(__file__).parent.parent

        # Variables used to resume last file
        self.current_line = 0
        self.current_file = None

    @property
    def current_file_name(self):
        if self.current_file:
            return self.current_file.split('.')[0]

    def turn_off(self):
        if self.is_reciting:
            print(f'Turning {self.current_file_name} off...')
            self.is_reciting = False
        else:
            print("There's nothing to stop.")

    async def resume(self, channel):
        if self.current_line:
            await self.bot.loop.create_task(self._recite(channel))
        else:
            print("There's nothing to resume.")

    @commands.command()
    async def recite(self, ctx, arg):
        await ctx.message.delete()

        if arg == 'stop':
            self.turn_off()
        elif arg == 'resume':
            await self.resume(ctx.message.channel)
        elif self.is_reciting:
            print(f'Already reciting {self.current_file_name}.')
        else:
            self.current_file = f'{arg}.txt'
            self.current_line = 0
            await self.bot.loop.create_task(self._recite(ctx.message.channel))

    async def _recite(self, channel):
        await self.bot.wait_until_ready()

        try:
            file = open(os.path.join(self.text_path, self.current_file), 'r')
        except FileNotFoundError:
            print(f'File {self.current_file} not found.')
            self.current_file = None
            return

        print(f'Turning {self.current_file_name} on...')
        self.is_reciting = True

        lines = file.read().splitlines()
        while not self.bot.is_closed() and self.is_reciting:
            line = lines[self.current_line]
            self.current_line += 1
            if line.strip():
                await channel.send(line)
                await asyncio.sleep(randint(5, 10))
        self.is_reciting = False
        file.close()


def setup(bot):
    bot.add_cog(LoopCog(bot))
