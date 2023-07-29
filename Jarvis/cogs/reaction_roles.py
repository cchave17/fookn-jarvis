import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = 1127046052156018818
        channel_id= 1134688234018971769
        message_id = 1134734670693675128
        log_channel_id = 1134782095022104587

        if payload.guild_id != guild_id or payload.channel_id != channel_id or payload.message_id != message_id:
            return

        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
    
        if payload.event_type == 'REACTION_ADD':
            role = discord.utils.get(guild.roles, name="Couch Potato")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.add_roles(role)
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(f'Role {role.name} added to user {member.name}')
                    print("done")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = 1127046052156018818
        channel_id= 1134688234018971769
        message_id = 1134734670693675128
        log_channel_id = 1134782095022104587

        if payload.guild_id != guild_id or payload.channel_id != channel_id or payload.message_id != message_id:
            return

        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)

        if payload.event_type == 'REACTION_REMOVE':
            role = discord.utils.get(guild.roles, name="Couch Potato")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(f'Role {role.name} removed from user {member.name}')
                    print("done")