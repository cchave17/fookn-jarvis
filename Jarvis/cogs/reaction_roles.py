import os
import discord
from discord.ext import commands

GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MESSAGE_ID = os.getenv("MESSAGE_ID")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.guild_id) != GUILD_ID or str(payload.channel_id) != CHANNEL_ID or str(payload.message_id) != MESSAGE_ID:
            return

        guild = discord.utils.find(lambda g : str(g.id) == GUILD_ID, self.bot.guilds)
    
        if payload.event_type == 'REACTION_ADD':
            role = discord.utils.get(guild.roles, name="Couch Potato")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.add_roles(role)
                    log_channel = self.bot.get_channel(int(LOG_CHANNEL_ID))
                    await log_channel.send(f'Role {role.name} added to user {member.name}')
                    print("added role done")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.guild_id) != GUILD_ID or str(payload.channel_id) != CHANNEL_ID or str(payload.message_id) != MESSAGE_ID:
            return

        guild = discord.utils.find(lambda g : str(g.id) == GUILD_ID, self.bot.guilds)

        if payload.event_type == 'REACTION_REMOVE':
            role = discord.utils.get(guild.roles, name="Couch Potato")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                    log_channel = self.bot.get_channel(int(LOG_CHANNEL_ID))
                    await log_channel.send(f'Role {role.name} removed from user {member.name}')
                    print("remove role done")
