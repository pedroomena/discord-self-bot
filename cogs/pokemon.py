from asyncio import TimeoutError
from discord.ext import commands

from reverse_image_search import search


class PokemonCog(commands.Cog):
    CATCH = 'p!catch {pokemon_name}'
    POKECORD_ID = 365975655608745985

    def __init__(self, bot):
        self.bot = bot
        self.channels = set()

    @commands.command()
    async def pokemon(self, ctx, *, arg):
        await ctx.message.delete()

        channel_id = ctx.message.channel.id
        channel_verbose = f'{ctx.message.channel.name} ({ctx.message.guild.name})'

        if arg == 'here':
            self.channels.add(channel_id)
            print(f'Now catching Pokemons on channel {channel_verbose}')
        elif arg == 'clear':
            try:
                self.channels.remove(channel_id)
            except KeyError:
                print("I wasn't listening to this channel.")
            print(f"I'm not listening to channel {channel_verbose} anymore.")
        elif arg == 'clearall':
            self.channels = set()
            print(f"All channels cleared.")
        else:
            print("Invalid argument.")
        print(f"I'm now listening to {len(self.channels)} channels.")

    # todo: checker decorators
    @commands.Cog.listener()
    async def on_message(self, message):
        channel_id, author_id = message.channel.id, message.author.id

        if author_id != self.POKECORD_ID or channel_id not in self.channels:
            return

        if message.embeds and 'wild' in message.embeds[0].title:
            print('A wild pokémon has appeared!')
            pokemons = search(message.embeds[0].image.url)
            
            if pokemons:
                print('Trying the first time...'.format(pokemons[0]))
                await message.channel.send(self.CATCH.format(pokemon_name=pokemons[0]))

                try:
                    response = await self.bot.wait_for('message', timeout=3.0, check=self.has_caught)
                except TimeoutError:
                    response = None

                if response is not None:
                    print('Caught it!')
                    return

                if len(pokemons) > 1:
                    print('Gonna try a little more...')
                    poke_index = 1

                    while response is None and poke_index < len(pokemons):
                        print('Trying the {} time...'.format(poke_index + 1))
                        await message.channel.send(self.CATCH.format(pokemon_name=pokemons[poke_index]))
                        try:
                            response = await self.bot.wait_for('message', timeout=3.0, check=self.has_caught)
                        except TimeoutError:
                            response = None
                        poke_index += + 1
                if response is None:
                    print('Failed guessing the pokémon.')
                else:
                    print('Caught it!')
            else:
                print('Unable to fetch guesses from reverse image search.')

    @staticmethod
    def has_caught(m):
        return m.author.id == PokemonCog.POKECORD_ID and m.content and 'Congratulations ' in m.content


def setup(bot):
    bot.add_cog(PokemonCog(bot))
