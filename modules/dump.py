import inspect
import re
from asyncio import sleep
from functools import wraps
from typing import List

from discord import User, Embed, Profile, Guild, Member, Permissions, Message, Role, Emoji, TextChannel
from discord.ext.commands import Bot, command, Context as CommandContext, Context
from discord.ext.commands import Paginator
from datetime import datetime

async def _context_react(self: Context, emoji):
    await self.message.add_reaction(emoji)


Context.react = _context_react


def dump_perms(permissions: Permissions):
    def perm_names():
        for perm, value in permissions:
            if value:
                yield perm

    return ', '.join(perm_names())


def then_delete(cmd):
    @wraps(cmd)
    async def func(*args, **kwargs):
        mes = await cmd(*args, **kwargs)
        if mes and hasattr(mes, 'delete'):
            await sleep(30)
            await mes.delete()

    return func


class DumpCog(object):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def show_off(self, ctx: CommandContext, name: str):
        paginator = Paginator(prefix="```py")
        for line in inspect.getsource(self.bot.get_command(name).callback).split('\n'):
            paginator.add_line(line.replace("`", "`\u200B"))
        for page in paginator.pages:
            await ctx.send(page)

    @command()
    async def raw(self, ctx: CommandContext, message: Message):
        content: str = message.content
        escaped = content.replace('```', '``\u200B`')
        await ctx.send(content=f'```\n{escaped}\n```')
        await ctx.react('✅')

    @command(aliases=['resolve'])
    @then_delete
    async def resolve_id(self, ctx: CommandContext, snowflake):
        snowflake = re.sub(r'[^0-9]', '', snowflake)
        if not snowflake:
            return await ctx.send("No id")
        snowflake = int(snowflake)
        if snowflake <= 0:
            return await ctx.send("Invalid id")
        when = (snowflake >> 22) + 1420070400000
        worker = (snowflake & 0x3E0000) >> 17
        process = (snowflake & 0x1F000) >> 12
        increment = snowflake & 0xFFF

        channel: TextChannel = self.bot.get_channel(snowflake)
        user: User = self.bot.get_user(snowflake)
        guild: Guild = self.bot.get_guild(snowflake)
        emoji: Emoji = self.bot.get_emoji(snowflake)
        roles: List[Role] = [role for guild in self.bot.guilds for role in guild.roles if role.id == snowflake]
        role: Role = roles[0] if len(roles) > 0 else None

        embed = Embed(title=f"ID: {snowflake}")
        embed.add_field(name="When", value=str(when) + ' / ' + str(datetime.fromtimestamp(when)))
        embed.add_field(name="Worker", value=str(worker))
        embed.add_field(name="Process", value=str(process))
        embed.add_field(name="Increment", value=str(increment))

        def add_if(name, thing, note=''):
            if thing:
                embed.add_field(name="Type", value=name)
                embed.add_field(name="Data", value=f"```\n{thing!r}\n```{note}")
                return True
            return False

        if not any(x for x in [
            add_if("Guild", guild, "This may also be the default channel of the @everyone role of that server"),
            add_if("Channel", channel),
            add_if("User", user),
            add_if("Role", role),
            add_if("Emoji", emoji),
        ]):
            embed.add_field(name="Type", value="Not found.")
        await ctx.send(embed=embed)

    @command()
    async def user(self, ctx: CommandContext, user: User, guild: Guild = None):
        if guild is None and ctx.guild is not None:
            guild: Guild = ctx.guild
        profile: Profile = await user.profile()
        description = ""
        if profile.nitro:
            description += f"i can haz animated emojis since {profile.premium_since}\n"
        if profile.hypesquad:
            description += f"they got some hype\n"
        if profile.partner:
            description += "insrt BLU INFINITY SYMBOL her\n"
        if profile.staff:
            description += "staff. if this is b1nzy, then FUCK him for banning selfbots\n"
        mutual: List[Guild] = profile.mutual_guilds

        mutual_text = '\n'.join(guild.name for guild in mutual)
        if len(mutual_text) > 512:
            mutual_text = f"Together in {len(mutual)} guilds. [Truncated]"

        em = Embed(
            title=str(user),
            description=description,
        )
        if guild:
            member: Member = guild.get_member(user.id)
            if member:
                if guild.owner_id == member.id:
                    em.add_field(name="Owner", value="Yeah", inline=True)
                em.colour = member.color
                em.add_field(name="Joined Guild", value=member.joined_at, inline=True)
                em.add_field(name="Permissions", value=dump_perms(member.guild_permissions), inline=True)
        em.set_author(name=user.display_name, icon_url=user.avatar_url)
        em.add_field(name="Mutual guilds", value=mutual_text, inline=True)
        em.add_field(name="Joined Discord", value=user.created_at, inline=True)
        for connection in profile.connected_accounts:
            em.add_field(name=connection['type'], value=('☑' if connection['verified'] else '') + connection['name'],
                         inline=True)
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)
        await ctx.react('✅')


def setup(bot: Bot):
    bot.add_cog(DumpCog(bot))
