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

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(GptPrompt(bot))

bot.run(os.getenv('GANGSTALICIOUS_TOKEN'))