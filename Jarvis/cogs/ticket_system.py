import discord
from discord.ext import commands

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_ticket(self, ctx):
        ticket_channel_name = f'ticket-{ctx.message.author.name}'
        existing_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)
    
        if not existing_channel:
            ticket_channel = await ctx.guild.create_text_channel(name=ticket_channel_name)
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.message.author, send_messages=True, read_messages=True)
            message = await ticket_channel.send(f"New ticket created by {ctx.message.author.mention}")
            await message.pin()
            print("Ticket channel created.")
    
    @commands.command()
    async def close_ticket(self, ctx):
        ticket_channel_name = f'ticket-{ctx.message.author.name}'
        existing_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)
    
        if existing_channel:
            await existing_channel.delete(reason="Ticket closed.")
            print("Ticket channel deleted.")