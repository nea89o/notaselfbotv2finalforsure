import re
from subprocess import Popen, PIPE
from typing import List
from typing import Pattern

from discord import Message, Embed, Color
from discord.ext.commands import Bot, Context as CommandContext, command

matcher: Pattern = re.compile(r'(?P<name>\w+)[^(]+\((?P<version>[^)]+)\)[^\-]+(?P<description>.*)')


class PyPiCog(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def pypi(self, ctx: CommandContext, search, *, text=''):
        message: Message = ctx.message
        proc = Popen(['pip', 'search', search], stdout=PIPE, stderr=PIPE)
        if proc.wait() != 0:
            await message.edit(
                embed=Embed(
                    color=Color.red(),
                    description='Failed to search for `{search}` on pypi.'))
        stdout, _ = proc.communicate()
        stdout = stdout.decode(encoding='utf-8')
        lines: List[str] = stdout.split('\n')
        content = lines[0] + ' '.join(line.strip() for line in lines[1:] if line.startswith('    '))
        match = matcher.match(content)
        if not match:
            await message.edit(
                embed=Embed(
                    color=Color.dark_orange(),
                    description=f"Weird response format:```\n{stdout[:512]}```"))
        name = match.group("name")
        version = match.group("version")
        description = match.group("description")
        await message.edit(
            content=text,
            embed=Embed(
                title=name,
                url=f"https://pypi.org/project/{name}/",
                description=description
            ).set_footer(text=version))


def setup(bot: Bot):
    bot.add_cog(PyPiCog(bot))
