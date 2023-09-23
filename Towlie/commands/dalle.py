import os
import openai
from interactions import SlashContext, slash_command, slash_option, OptionType

from dotenv import load_dotenv

load_dotenv()

openai.api_key = (os.getenv("OPENAI_API_KEY"))

@slash_command(name="image", description="Generate an image using DALL-E 2.")
@slash_option(
    name="prompt",
    description="The prompt you want to generate an image for.",
    required=True,
    opt_type=OptionType.STRING
)
async def generate_image(ctx: SlashContext, prompt: str):
    await ctx.defer()

    # Call the OpenAI API to generate the image
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response['data'][0]['url']

    # Send the image URL
    await ctx.send(f"Generated image: {image_url}")
