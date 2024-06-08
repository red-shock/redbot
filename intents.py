from discord import Intents

intents = Intents.none()

# set to true to remove songs if banned
intents.moderation = True

intents.guild_messages = True
intents.message_content = True
intents.voice_states = True
