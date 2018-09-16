from string import digits

from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Converter, Context, Bot, BadArgument, converter

LANGUAGES = {
    'python': ['py', 'py3'],
    'javascript': ['js'],
    'c': ['c'],
    'cpp': ['c++', 'cpp', 'cxx'],
    'go': ['go'],
    'bash': [],
    'xml': [],
    'html': [],
}

LANGUAGES_INV = {
    **{v: k for k, v in LANGUAGES.items() for v in v},
    **{k: k for k in LANGUAGES.keys()},
}

EXTENSIONS = dict(
    python='py',
    c='c',
    cpp='cpp',
    bash='sh',
    javascript='js',
)


class CodeBlock:
    missing_error = 'Missing code block. Please use the following markdown\n\\`\\`\\`language\ncode here\n\\`\\`\\`'

    def __init__(self, argument):
        try:
            block, code = argument.split('\n', 1)
        except ValueError:
            raise commands.BadArgument(self.missing_error)

        if not block.startswith('```') and not code.endswith('```'):
            raise commands.BadArgument(self.missing_error)

        language = block[3:]
        self.language = self._get_language(language.lower())
        self.source = code.rstrip('`')
        self.extension = self._get_extension(self.language)

    @staticmethod
    def _get_extension(language):
        return EXTENSIONS[language]

    @staticmethod
    def _get_language(language):
        return LANGUAGES_INV.get(language)


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
