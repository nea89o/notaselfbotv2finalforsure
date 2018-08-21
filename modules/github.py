from typing import List

from discord import Embed, Color
from discord.ext.commands import Bot, Group
from discord.ext.commands import Context as CommandContext, group
from github.NamedUser import NamedUser
from github.Repository import Repository

from config import config

github = config.github.github


def find_repo(search):
    repos: List[Repository] = list(github.get_repos())
    checks = [
        lambda r: r.id.lower() == search.lower(),
        lambda r: search.lower() in r.name.lower(),
        lambda r: search.lower() in repo.description.lower(),
    ]
    for check in checks:
        for repo in repos:
            if check(repo):
                return repo


class GithubCog(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @group(invoke_without_subcommand=True)
    async def github(self, ctx: CommandContext):
        pass

    github: Group = github

    @github.command()
    async def me(self, ctx: CommandContext):
        user: NamedUser = github.get_user()
        embed = Embed(
            color=Color.blurple(),
            title=user.login,
            description=user.bio,
            url=user.url,
        )
        embed.add_field(name='Followers', value=user.followers)
        embed.add_field(name='Following', value=user.following)
        embed.add_field(name='Repositories',
                        value=f'[{user.public_repos + user.total_private_repos}](https://github.com/{user.login})')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @github.command()
    async def repo(self, ctx: CommandContext, *, search):
        repo = find_repo(search)
        print(repo)
        print(search)
        if repo:
            embed = Embed(
                title=repo.id,
                description=repo.description,
                url=repo.html_url
            )
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(GithubCog(bot))
