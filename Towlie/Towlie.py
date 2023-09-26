import os
from dotenv import load_dotenv
from interactions import Client, slash_command
from cogs.reaction_roles import ReactionRoles
from cogs.ticket_system import TicketSystem
from cogs.gpt_prompt import GptPrompt

import openai
load_dotenv()

gpt_message_history = [{"role": "system", "content": "You are a chatbot."}]

bot = Client()

@slash_command(name="ask", description="Talk to Chat GPT")
async def ask(ctx, *, prompt):
    print("prompt" + prompt)
    channel = bot.get_channel(os.getenv("GPT_CHANNEL")) 

    if channel:
        global gpt_message_history
        openai.api_key = (os.getenv("OPENAI_API_KEY"))
        gpt_message_history.append({"role": "user", "content": prompt})
        print(gpt_message_history)
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=gpt_message_history,
            max_tokens=2000,
            temperature=0.7,
            presence_penalty=0.2,
            frequency_penalty=0.2
        )

        gpt_message_history.append(chat_completion['choices'][0]['message'])
        print(gpt_message_history)

        response = chat_completion['choices'][0]['message']['content']
        await ctx.send(f"{ctx.message.author.mention} {response}")
    else:
        await ctx.send("Could not find the specified channel")


@slash_command(name="nahnsu",description="Hi Nahnsu")
async def testing_command(ctx):
    # Fetch the desired channel
    channel = bot.get_channel(1134955892362719332) 

    # Check if channel exists
    if channel:
        # Send a message to the channel
        await channel.send("hello world")
    else:
        await ctx.send("Could not find the specified channel")

@bot.listen()
async def on_startup():
    print("Bot is ready!")

# @bot.event
# async def on_ready():
#     print(f'{bot.user} is connected to Discord!')
#     await bot.add_cog(ReactionRoles(bot))
#     await bot.add_cog(TicketSystem(bot))
#     await bot.add_cog(GptPrompt(bot))

bot.start(os.getenv('TOWLIE_TOKEN'))
