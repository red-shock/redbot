import discord
from discord.ext import commands
from intents import intents
from dotenv import dotenv_values
import logging
import datetime
import utilities
from preferences import Preferences

handler = logging.FileHandler(filename="logs/error.log", encoding="utf-8", mode="w")
bot = commands.Bot(command_prefix="!", intents=intents)
preferences = Preferences("preferences.toml")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if preferences.delete_duplicate_messages:
        async for prev_message in message.channel.history(
            limit=10, before=message.created_at
        ):
            if message.author.id == prev_message.author.id:
                if message.content == prev_message.content:
                    await message.delete()
                    return


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


@bot.hybrid_command(name="update-preferences")
async def update_preferences(ctx, delete_duplicates: bool = None):
    if ctx.author.resolved_permissions.administrator:
        if delete_duplicates != None:
            preferences.delete_duplicate_messages = delete_duplicates

        params = [*map(lambda x: x.name, ctx.command.clean_params.values())]
        await ctx.send(
            f"{ctx.author.mention} updated preferences to {', '.join([f"{param}={ctx.kwargs[param]}" for param in params])}"
        )


if __name__ == "__main__":
    config = dotenv_values()
    bot.run(config["AUTH_TOKEN"], log_handler=handler, log_level=logging.ERROR)
