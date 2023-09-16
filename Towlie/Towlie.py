import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from cogs.reaction_roles import ReactionRoles
from cogs.ticket_system import TicketSystem
from cogs.gpt_prompt import GptPrompt

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

print(os.environ)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(GptPrompt(bot))

bot.run(os.getenv('TOWLIE_TOKEN'))

# import discord
# from googletrans import Translator

# intents = discord.Intents.all()

# # Initialize the bot
# client = discord.Client(intents=intents)

# translator = Translator()

# @client.event
# async def on_ready():
#     print("Bot is ready")

# @client.event
# async def on_message(message):
#     # Don't reply to ourselves
#     if message.author == client.user:
#         return

#     if message.content.startswith('!translate'):
#         _, src, dest, *text = message.content.split(" ")
#         text = ' '.join(text)
#         translation = translator.translate(text, src=src, dest=dest)
#         print(translation)
#         await message.channel.send(translation.text)

# # Run the bot with your token
# client.run('token_dont_show')
