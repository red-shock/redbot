import discord
from discord.ext import commands
from intents import intents
from dotenv import dotenv_values
import logging
import datetime

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


def format_time_delta(time: datetime.timedelta) -> str:
    seconds = time.total_seconds()
    years = int(seconds // 31536000)
    seconds -= years * 31536000
    months = int(seconds // 2592000)
    seconds -= months * 2592000
    weeks = int(seconds // 604800)
    seconds -= weeks * 604800
    days = int(seconds // 86400)
    seconds -= days * 86400
    time_list = [
        i
        for i in [
            f"{years} years",
            f"{months} months",
            f"{weeks} weeks",
            f"{days} days",
        ]
        if int(i[0]) != 0
    ]
    return (
        ", ".join(time_list[:-1]) + " and " + time_list[-1]
        if len(time_list) > 1
        else time_list[0]
    )


@bot.hybrid_command(name="member-since")
async def member_since(ctx, member: discord.Member):
    difference = datetime.datetime.now(datetime.UTC) - member.joined_at
    await ctx.send(
        f"{member.mention} has been a member for {format_time_delta(difference)}."
    )


if __name__ == "__main__":
    config = dotenv_values()
    bot.run(config["AUTH_TOKEN"], log_handler=handler, log_level=logging.ERROR)
