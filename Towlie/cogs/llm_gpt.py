import os
import openai
from discord.ext import commands


class LlmGpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = (os.getenv("OPENAI_API_KEY"))
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))

    @commands.command()
    @commands.has_any_role('DEV','Jarvis', 'Assistant to the Assistant Regional Manager','Weekend Shift Supervisor', 'OWL (Original Wave Lounger)', 'Cartman (WoW Episode)','Steamed Broccoli', 'Couch Potato')
    async def ask(self, ctx, *, prompt):
        if ctx.channel.id != int(os.getenv("GPT_CHANNEL")):
            log_channel = self.bot.get_channel(self.log_channel_id)
            await log_channel.send(f'{ctx.message.author} tried to access GPT in channel {ctx.channel.name}')

            correct_channel = self.bot.get_channel(os.getenv("GPT_CHANNEL"))
            await ctx.send(f'{ctx.message.author.mention} that command is only acceptable in the {correct_channel.name} channel')
            return
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
            presence_penalty=0.2,
            frequency_penalty=0.2
        )

        response = chat_completion['choices'][0]['message']['content']
        await ctx.send(f"{ctx.message.author.mention} {response}")


# import os
# import openai
# from discord.ext import commands
# from discord_slash import cog_ext, SlashContext

# class LlmGpt(commands.Cog):
#     def __init__(self, bot, slash):
#         self.bot = bot
#         self.slash = slash
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))

#     @cog_ext.cog_slash(name="ask", description="Ask GPT a question.")
#     async def ask(self, ctx: SlashContext, prompt: str):
#         if ctx.channel.id != int(os.getenv("GPT_CHANNEL")):
#             log_channel = self.bot.get_channel(self.log_channel_id)
#             await log_channel.send(f'{ctx.author} tried to access GPT in channel {ctx.channel.name}')

#             correct_channel = self.bot.get_channel(os.getenv("GPT_CHANNEL"))
#             await ctx.send(f'{ctx.author.mention} that command is only acceptable in the {correct_channel.name} channel')
#             return
        
#         chat_completion = openai.ChatCompletion.create(
#             model="gpt-4-0613",
#             messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
#             max_tokens=500,
#             temperature=0.7,
#             presence_penalty=0.2,
#             frequency_penalty=0.2
#         )

#         response = chat_completion['choices'][0]['message']['content']
#         await ctx.send(f"{ctx.author.mention} {response}")
