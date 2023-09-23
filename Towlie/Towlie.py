from interactions import Client, Intents
import os
from commands.chat_gpt import ask_gpt
from commands.dalle import generate_image
from dotenv import load_dotenv

load_dotenv()

# Initialize bot
bot = Client(intents=Intents.DEFAULT)

# Run the bot
bot.start(os.getenv('TOWLIE_TOKEN'))