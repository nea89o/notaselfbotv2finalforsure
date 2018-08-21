from discord import Guild
from discord.ext.commands import Bot, command, Context as CommandContext, guild_only


class RageQuitCog(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    @guild_only()
    async def ragequit(self, ctx: CommandContext):
        guild: Guild = ctx.guild
        await guild.leave()


def setup(bot: Bot):
    bot.add_cog(RageQuitCog(bot))
