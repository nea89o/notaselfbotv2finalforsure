from string import digits

from discord import TextChannel
from discord.ext.commands import Converter, Context, Bot, BadArgument, converter


def is_int(text):
    return all(map(digits.__contains__, text))


class GuildConverter(Converter):
    async def convert(self, ctx: Context, argument):
        bot: Bot = ctx.bot
        try:
            return bot.get_guild(int(argument))
        except:
            try:
                return [guild for guild in bot.guilds if guild.name.casefold() == argument.casefold()][0]
            except:
                raise BadArgument(f"Could not find guild with id or name {argument}")


class MessageConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        bot: Bot = ctx.bot
        if is_int(argument):
            message = int(argument)
            channel: TextChannel = ctx.channel
        else:
            _, channel, message = list(map(int, filter(is_int, argument.split('/'))))
            channel: TextChannel = bot.get_channel(channel)

        if bot.user.bot:
            return await channel.get_message(message)
        else:
            return (await channel.history(around=message, limit=2).flatten())[1]


# noinspection PyUnusedLocal
def setup(bot: Bot):
    converter.MessageConverter = MessageConverter
    converter.GuildConverter = GuildConverter
