from discord import Message
from discord.ext.commands import Bot, command, Context


class BinaryCog(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def binary(self, ctx: Context, *, text: str):
        binary = ' '.join(bin(ord(ch))[2:].zfill(8) for ch in text)
        mes: Message = ctx.message
        await mes.edit(content=binary)

    @command()
    async def un_binary(self, ctx: Context, message: Message):
        text: str = message.content
        print(text)
        text.replace(' ', '').replace('\n', '')
        chunks, chunk_size = len(text), len(text) // 4
        await ctx.message.edit(
            content=f"Decoded message {message.jump_url}: "
                    f"{''.join([chr(int(text[i:i + chunk_size], 2)) for i in range(0, chunks, chunk_size)])}")


def setup(bot: Bot):
    bot.add_cog(BinaryCog(bot))
