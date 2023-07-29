import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

@bot.event
async def on_raw_reaction_add(payload):
    guild_id = 1127046052156018818
    channel_id= 1134688234018971769
    message_id = 1134734670693675128
    log_channel_id = 1134782095022104587

    if payload.guild_id != guild_id or payload.channel_id != channel_id or payload.message_id != message_id:
        return

    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
    
    if payload.event_type == 'REACTION_ADD':
        role = discord.utils.get(guild.roles, name="Couch Potato")
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.add_roles(role)
                log_channel = bot.get_channel(log_channel_id)
                await log_channel.send(f'Role {role.name} added to user {member.name}')
                print("done")

@bot.event
async def on_raw_reaction_remove(payload):
    guild_id = 1127046052156018818
    channel_id= 1134688234018971769
    message_id = 1134734670693675128
    log_channel_id = 1134782095022104587

    if payload.guild_id != guild_id or payload.channel_id != channel_id or payload.message_id != message_id:
        return

    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

    if payload.event_type == 'REACTION_REMOVE':
        role = discord.utils.get(guild.roles, name="Couch Potato")
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                log_channel = bot.get_channel(log_channel_id)
                await log_channel.send(f'Role {role.name} removed from user {member.name}')
                print("done")

@bot.command()
async def create_ticket(ctx):
    ticket_channel_name = f'ticket-{ctx.message.author.name}'
    existing_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)
    
    if not existing_channel:
        ticket_channel = await ctx.guild.create_text_channel(name=ticket_channel_name)
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
        await ticket_channel.set_permissions(ctx.message.author, send_messages=True, read_messages=True)
        message = await ticket_channel.send(f"New ticket created by {ctx.message.author.mention}")
        await message.pin()
        print("Ticket channel created.")
    
@bot.command()
async def close_ticket(ctx):
    ticket_channel_name = f'ticket-{ctx.message.author.name}'
    existing_channel = discord.utils.get(ctx.guild.channels, name=ticket_channel_name)
    
    if existing_channel:
        await existing_channel.delete(reason="Ticket closed.")
        print("Ticket channel deleted.")

bot.run('MTEzNDcxMTg4NDk4NjE4Nzg0OQ.G_ujyG.nu1rDxxeBXxkrkKUC_-bzEp2BfS0cTCc3Z1ZaE')