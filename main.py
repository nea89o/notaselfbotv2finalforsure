from discord.ext.commands import Bot, when_mentioned_or

from config import config
from utils import load_all_modules

bot = Bot(
    command_prefix=when_mentioned_or('~'),
    self_bot=True,
)

load_all_modules(bot)

if __name__ == '__main__':
    bot.run(config.token, bot=False)
