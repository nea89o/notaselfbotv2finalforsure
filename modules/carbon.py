import re
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Pattern

from discord import File
from discord.ext.commands import Bot, command, Context

from .converters import CodeBlock

TEMP_DIR: Path = (Path(__file__).parent / '..' / 'carbon-temp').resolve()
TEMP_DIR.mkdir(parents=True, exist_ok=True)
regex: Pattern = re.compile(b" (/[^ ]+) ")


class Carbon(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def carbon(self, ctx: Context, *, code_block: CodeBlock):
        print('carbon thingies..')
        temp_file: Path = (TEMP_DIR / ('carbon.' + code_block.extension))
        with temp_file.open('w') as cf:
            cf.write(code_block.source)
        proc = Popen(['carbon-now', '-p', 'notaselfbot', '-l', str(TEMP_DIR), str(temp_file)], stdout=PIPE)
        proc.wait()
        stdout, _ = proc.communicate()
        match = None
        for match in regex.finditer(stdout):
            pass
        if not match:
            return await ctx.react('❌')
        path = match.group(1).decode('ascii')
        with open(path, 'br') as fp:
            await ctx.send(file=File(fp, 'carbon.png'))


def setup(bot: Bot):
    bot.add_cog(Carbon(bot))
