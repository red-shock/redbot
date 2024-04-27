import discord
from discord.ext import commands
from intents import intents
from dotenv import dotenv_values


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.tree.sync()


@bot.hybrid_command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")


if __name__ == "__main__":
    config = dotenv_values()
    bot.run(config["AUTH_TOKEN"])
