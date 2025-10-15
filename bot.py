import discord
from discord.ext import commands, tasks
import os
from anthropic import Anthropic
from dotenv import load_dotenv
import requests

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Google Doc ID for PT Pete instructions
GOOGLE_DOC_ID = "1afW0zAXaPgu2qMDX3fEFovB9mmNBIpzsI03rWY2VdMU"

# Global variable to store persona
PERSONA = ""

def fetch_persona():
    """Fetch PT Pete persona from Google Doc"""
    try:
        import time
        # Add timestamp to prevent caching
        cache_buster = int(time.time())
        url = f"https://docs.google.com/document/d/1afW0zAXaPgu2qMDX3fEFovB9mmNBIpzsI03rWY2VdMU/export?format=txt&timestamp={cache_buster}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text
            print("[SUCCESS] Successfully loaded PT Pete instructions from Google Doc")
            print(f"[INFO] Loaded persona ({len(content)} characters)")
            return content
        else:
            print(f"[WARNING] Could not fetch Google Doc (status: {response.status_code}), using fallback")
            return "You are PT Pete, a friendly robot physical therapist assistant."
    except Exception as e:
        print(f"[ERROR] Error fetching Google Doc: {e}")
        return "You are PT Pete, a friendly robot physical therapist assistant."

# Fetch persona once at startup
print("[STARTUP] Fetching initial persona...")
PERSONA = fetch_persona()
print(f"[STARTUP] Initial persona loaded: {len(PERSONA)} characters")

@tasks.loop(seconds=10)
async def refresh_persona():
    """Refresh PT Pete instructions from Google Doc every 10 seconds"""
    global PERSONA
    print("[REFRESH] Refreshing PT Pete instructions from Google Doc...")
    PERSONA = fetch_persona()
    print(f"[REFRESH] Persona refreshed: {len(PERSONA)} characters")

class PTPete:
    def __init__(self):
        self.conversation_history = {}
    
    async def respond(self, message, user_id):
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        if not message or message.strip() == "":
            message = "hi"
        
        self.conversation_history[user_id].append({"role": "user", "content": message})
        
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
        
        try:
            response = anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,
                system=PERSONA,
                messages=self.conversation_history[user_id]
            )
            
            bot_response = response.content[0].text
            self.conversation_history[user_id].append({"role": "assistant", "content": bot_response})
            return bot_response
            
        except Exception as e:
            print(f"[ERROR] API Error: {e}")
            return "Beep boop! I'm having trouble connecting."

pt_pete = PTPete()

@bot.event
async def on_ready():
    print("[ON_READY] on_ready function called!")
    print(f'[ONLINE] PT Pete is online! Logged in as {bot.user}')
    print(f'[INFO] Loaded persona ({len(PERSONA)} characters)')
    print("[AUTO-REFRESH] Starting refresh task...")
    try:
        refresh_persona.start()
        print("[AUTO-REFRESH] Refresh task started successfully!")
        print("[AUTO-REFRESH] Auto-refresh enabled (checks every 10 seconds)")
    except Exception as e:
        print(f"[ERROR] Failed to start refresh task: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print(f"[MESSAGE] Message: {message.content}")
    print(f"[CHECK] Bot mentioned: {bot.user.mentioned_in(message)}")
    
    if bot.user.mentioned_in(message):
        print("[PROCESSING] Processing mention!")
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not content:
            content = "hi"
            
        print(f"[CLAUDE] Sending to Claude: '{content}'")
        response = await pt_pete.respond(content, message.author.id)
        
        embed = discord.Embed(description=response, color=discord.Color.from_rgb(216, 42, 18))
        embed.set_author(name="PT Pete", icon_url=bot.user.avatar.url if bot.user.avatar else None)
        embed.set_footer(text="Robot PT Assistant | Not medical advice")
        
        await message.channel.send(embed=embed)
        print("[SENT] Sent response!")
    
    await bot.process_commands(message)

if __name__ == "__main__":
    print("[MAIN] Starting bot...")
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
