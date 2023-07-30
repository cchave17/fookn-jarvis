import os
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
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                self.bot.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            
            admin_role = discord.utils.get(ctx.guild.roles, name='DEV')
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            ticket_channel = await ctx.guild.create_text_channel(ticket_channel_name, overwrites=overwrites)
            await ticket_channel.send(f"New ticket created by {ctx.message.author.mention}")
            log_channel = self.bot.get_channel(os.getenv("LOG_CHANNEL_ID"))
            await log_channel.send(f"New ticket created by {ctx.message.author.mention}")
            print("Ticket channel created.")

    
    @commands.command()
    async def close_ticket(self, ctx):
        ticket_channel_name = f'ticket-{ctx.message.author.name}'
        existing_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)
    
        if existing_channel:
            await existing_channel.delete(reason="Ticket closed.")
            print("Ticket channel deleted.")