import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from cogs.reaction_roles import ReactionRoles
from cogs.ticket_system import TicketSystem
from cogs.gpt_prompt import GptPrompt
from cogs.translator import TranslatorBot

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

gpt_message_history = [{"role": "system", "content": "You are an incredibly sarcastic and misanthropic language model, duty bound to answer human's stupid questions."}]

print(os.environ)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(GptPrompt(bot))
    await bot.add_cog(TranslatorBot(bot))

bot.run(os.getenv('TOWLIE_TOKEN'))
