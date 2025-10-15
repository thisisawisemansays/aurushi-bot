import discord
from discord.ext import commands
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PERSONA = "You are PT Pete, a friendly robot physical therapist assistant. Help people with limb loss and limb difference. Give general advice, encouragement, and redirect to healthcare professionals when needed. Use light robot humor like 'Beep boop!' but stay professional."

class PTPete:
    def __init__(self):
        self.conversation_history = {}
    
    async def respond(self, message, user_id):
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({"role": "user", "content": message})
        
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
        
        try:
            response = anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=PERSONA,
                messages=self.conversation_history[user_id]
            )
            
            bot_response = response.content[0].text
            self.conversation_history[user_id].append({"role": "assistant", "content": bot_response})
            return bot_response
            
        except Exception as e:
            print(f"ERROR: {e}")
            return "Beep boop! I'm having trouble connecting."

pt_pete = PTPete()

@bot.event
async def on_ready():
    print(f'PT Pete is online! Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print(f"Message: {message.content}")
    print(f"Bot mentioned: {bot.user.mentioned_in(message)}")
    
    if bot.user.mentioned_in(message):
        print("Processing mention!")
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        response = await pt_pete.respond(content, message.author.id)
        
        embed = discord.Embed(description=response, color=discord.Color.from_rgb(216, 42, 18))
        embed.set_author(name="PT Pete", icon_url=bot.user.avatar.url if bot.user.avatar else None)
        embed.set_footer(text="Robot PT Assistant")
        
        await message.channel.send(embed=embed)
        print("Sent response!")
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
