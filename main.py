import discord
from discord.ext import commands
from intents import intents
from dotenv import dotenv_values
import logging
import datetime
import utilities

handler = logging.FileHandler(filename="logs/error.log", encoding="utf-8", mode="w")
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.tree.sync()


@bot.hybrid_command(name="play")
async def play(ctx, playlist: str):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()


@bot.hybrid_command(name="join")
async def join_date(ctx, member: discord.Member):
    await ctx.send(
        f"{member.mention} joined the server at <t:{member.joined_at.timestamp()}>"
    )


@bot.hybrid_command(name="member-since")
async def member_since(ctx, member: discord.Member):
    difference = datetime.datetime.now(datetime.UTC) - member.joined_at
    await ctx.send(
        f"{member.mention} has been a server member for {utilities.format_time_delta(difference)}."
    )


if __name__ == "__main__":
    config = dotenv_values()
    bot.run(config["AUTH_TOKEN"], log_handler=handler, log_level=logging.ERROR)
