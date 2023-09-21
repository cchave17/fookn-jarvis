import os
import openai
from discord.ext import commands

gpt_message_history = [{"role": "system", "content": "You are a helpful assistant."}]


class GptPrompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = (os.getenv("OPENAI_API_KEY"))
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))

    @commands.command()
    @commands.has_any_role('DEV','Jarvis', 'Assistant to the Assistant Regional Manager','Weekend Shift Supervisor', 'OWL (Original Wave Lounger)', 'Cartman (WoW Episode)','Steamed Broccoli', 'Couch Potato')
    async def ask(self, ctx, *, prompt):
        global gpt_message_history
        gpt_message_history.append({"role": "user", "content": prompt})
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=gpt_message_history,
            max_tokens=2000,
            temperature=0.7,
            presence_penalty=0.2,
            frequency_penalty=0.2
        )

        gpt_message_history.append(chat_completion['choices'][0]['message'])

        response = chat_completion['choices'][0]['message']['content']
        await ctx.send(f"{ctx.message.author.mention} {response}")

    @commands.command()
    @commands.has_any_role('DEV','Jarvis', 'Assistant to the Assistant Regional Manager','Weekend Shift Supervisor', 'OWL (Original Wave Lounger)', 'Cartman (WoW Episode)','Steamed Broccoli', 'Couch Potato')
    async def translate(self, ctx, *args):
        prompt = f"Translate {args[0]} from {args[1]} to {args[2]}"

        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
            presence_penalty=0.2,
            frequency_penalty=0.2
        )

        response = chat_completion['choices'][0]['message']['content']
        await ctx.send(f"{ctx.message.author.mention} {response}")


