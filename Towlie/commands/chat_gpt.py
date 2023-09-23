import os
import openai
from interactions import slash_command, SlashContext, slash_option, OptionType
from dotenv import load_dotenv


load_dotenv()
# Initialize OpenAI API
openai.api_key = (os.getenv("OPENAI_API_KEY"))

@slash_command(name='ask', description='Ask GPT a question')
@slash_option(name="question", description="The question you want to ask.", required=True, opt_type=OptionType.STRING)
async def ask_gpt(ctx: SlashContext, question: str):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.7,
        presence_penalty=0.2,
        frequency_penalty=0.2
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    await ctx.send(answer)
