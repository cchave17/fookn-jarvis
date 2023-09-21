import os
import googletrans
from discord.ext import commands


class TranslatorBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))

    @commands.command()
    @commands.has_any_role('DEV','Jarvis', 'Assistant to the Assistant Regional Manager','Weekend Shift Supervisor', 'OWL (Original Wave Lounger)', 'Cartman (WoW Episode)','Steamed Broccoli', 'Couch Potato')
    async def translate_help(self, ctx, *args):

        response = "Call the translate bot with the !translate command. Then, the text you want to translate, the destination language code, and the source langauges code. \n E.g.: !translate \"Please work\" en fr"
        await ctx.send(f"{ctx.message.author.mention} {response}")

    @commands.command()
    @commands.has_any_role('DEV','Jarvis', 'Assistant to the Assistant Regional Manager','Weekend Shift Supervisor', 'OWL (Original Wave Lounger)', 'Cartman (WoW Episode)','Steamed Broccoli', 'Couch Potato')
    async def translate(self, ctx, *args):
        
        print("translate: " + args[0] + "\n from " + args[1] + " to " + args[2])
        translated_text = googletrans.Translator().translate(args[0], dest=args[1], src=args[2])
        print("output: " + translated_text.text)

        response = translated_text.text
        await ctx.send(f"{ctx.message.author.mention} {response}")