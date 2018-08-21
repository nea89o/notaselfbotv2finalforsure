from _contextvars import Context
from string import digits, ascii_uppercase, ascii_lowercase

from discord.ext.commands import Bot, command, Converter


class CopyPastaTextConverter(Converter):

    async def convert(self, ctx: Context, argument: str):
        allowed_characters = ascii_uppercase + ascii_lowercase + digits + '_- '
        if any(ch not in allowed_characters for ch in argument):
            return
        with open(f'copypasta/{argument}.txt') as fp:
            return fp.read().strip()


class CopyPasta(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command(aliases=['cp', 'copy-pasta', 'copypasta'])
    async def copy_pasta(self, ctx: Context, copy_pasta: CopyPastaTextConverter):
        await ctx.message.edit(content=str(copy_pasta))


def setup(bot: Bot):
    bot.add_cog(CopyPasta(bot))
