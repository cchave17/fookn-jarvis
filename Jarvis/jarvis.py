import discord
from discord.ext import commands
from cogs.reaction_roles import ReactionRoles
from cogs.ticket_system import TicketSystem

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(TicketSystem(bot))

bot.run('API_DISCORD_TOKEN')
