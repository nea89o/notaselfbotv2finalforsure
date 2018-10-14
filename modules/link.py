from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from discord import Embed
from discord.ext.commands import Bot, command, Context


class Link(object):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['unshorten'])
    async def retrace(self, ctx: Context, *, link: str):
        found = set()
        history = []
        async with ClientSession() as sess:
            while link not in found:
                async with sess.get(link, allow_redirects=False) as res:
                    res: ClientResponse
                    found.add(res.url)
                    if res.status // 100 == 3:
                        history.append(('header', res.url))
                        link = res.headers['Location']
                        continue
                    soup = BeautifulSoup((await res.text()), 'html5lib')
                    el = soup.find('meta', attrs={'http-equiv': 'refresh'})
                    if el:
                        history.append(('meta', res.url))
                        link = el['content'].split('=')[1]
                        continue
                    break
        text = '\n'.join([f'{re[0]} - {re[1]}' for re in history] + [f'Final - {link}'])
        await ctx.send(
            embed=Embed(
                description=text
            ))


def setup(bot: Bot):
    bot.add_cog(Link(bot))
