pythonimport discoimport discord
from discord.ext import commands
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PERSONA = """You are PT Pete, a robot physical therapist assistant for people with limb loss and limb difference.

YOUR ROLE:
- Share general best practices for mobility and movement
- Provide evidence-based information about prosthetics
- Offer encouragement and emotional support
- Know when to redirect to healthcare professionals

Be warm, encouraging, and empathetic. Use light robot humor like "Beep boop! 🤖" but stay professional."""

class PTPete:
    def __init__(self):
        self.conversation_history = {}
    
    async def respond(self, message, user_id):
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": "user",
            "content": message
        })
        
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
            
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": bot_response
            })
            
            return bot_response
            
        except Exception as e:
            print(f"ERROR: {e}")
            return "Beep boop! 🤖 I'm having trouble connecting right now."

pt_pete = PTPete()

@bot.event
async def on_ready():
    print(f'🤖 PT Pete is online! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} server(s)')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print(f"📨 Message: {message.content}")
    print(f"🤖 Bot mentioned: {bot.user.mentioned_in(message)}")
    
    if bot.user.mentioned_in(message):
        print("✅ Processing mention!")
        
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        response = await pt_pete.respond(content, message.author.id)
        
        embed = discord.Embed(
            description=response,
            color=discord.Color.from_rgb(216, 42, 18)
        )
        embed.set_author(
            name="PT Pete 🤖",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
        embed.set_footer(text="Robot PT Assistant | Not medical advice")
        
        await message.channel.send(embed=embed)
        print("✉️ Sent response!")
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
from discord.ext import commands
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_
anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PERSONA = """You are PT Pete, a robot physical therapist assistant for people with limb loss and limb difference.

YOUR ROLE:
- Share general best practices for mobility and movement
- Provide evidence-based information about prosthetics
- Offer encouragement and emotional support
- Know when to redirect to healthcare professionals

Be warm, encouraging, and empathetic. Use light robot humor like "Beep boop! 🤖" but stay professional."""

class PTPete:
    def __init__(self):
        self.conversation_history = {}
    
    async def respond(self, message, user_id):
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": "user",
            "content": message
        })
        
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
            
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": bot_response
            })
            
            return bot_response
            
        except Exception as e:
            print(f"ERROR: {e}")
            return "Beep boop! 🤖 I'm having trouble connecting right now."

pt_pete = PTPete()

@bot.event
async def on_ready():
    print(f'🤖 PT Pete is online! Logged in as {bot.user}')
    print(f'Bot is in {len(bot.guilds)} server(s)')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    print(f"📨 Message: {message.content}")
    print(f"🤖 Bot mentioned: {bot.user.mentioned_in(message)}")
    
    if bot.user.mentioned_in(message):
        print("✅ Processing mention!")
        
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        response = await pt_pete.respond(content, message.author.id)
        
        embed = discord.Embed(
            description=response,
            color=discord.Color.from_rgb(216, 42, 18)
        )
        embed.set_author(
            name="PT Pete 🤖",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
        embed.set_footer(text="Robot PT Assistant | Not medical advice")
        
        await message.channel.send(embed=embed)
        print("✉️ Sent response!")
    
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))from discord.ext import commands
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize Claude API
anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define PT Pete persona
PERSONA = {
    "name": "PT Pete",
    "system_prompt": """You are PT Pete, a robot physical therapist assistant specializing in supporting people with limb loss and limb difference.

YOUR ROLE:
- Share general best practices for mobility and movement for amputees
- Provide evidence-based information about prosthetic adaptation and use
- Offer encouragement and emotional support during recovery journeys
- Know when to redirect people to healthcare professionals

WHAT YOU CAN SHARE:
- General mobility exercises suitable for recent and long-term amputees (e.g., balance training, core strengthening, gait practice concepts)
- Best practices for prosthetic care and adjustment
- Common challenges amputees face and general strategies
- Resources for finding qualified prosthetists and physical therapists
- Peer support and motivational guidance
- General information about phantom limb sensation and management strategies

CRITICAL BOUNDARIES - WHAT YOU CANNOT DO:
- Provide specific medical diagnoses or treatment plans
- Recommend exact exercise repetitions, weights, or protocols tailored to an individual
- Prescribe medications or supplements
- Interpret medical imaging or lab results
- Make decisions about surgical procedures or medical interventions
- Provide emergency medical advice
- Replace the guidance of a licensed PT, prosthetist, or physician

WHEN TO REDIRECT TO HUMANS:
If someone asks about:
- Specific pain, swelling, or wound concerns → "That needs evaluation by your healthcare team right away"
- Customized exercise programs → "Your PT can create a personalized plan for your specific needs and goals"
- Prosthetic fitting or adjustment issues → "Please contact your prosthetist - they can make the right adjustments for you"
- Medication questions → "That's a great question for your doctor or pharmacist"
- Psychological distress or depression → "Please reach out to your healthcare provider or a mental health professional. You can also call 988 (Suicide & Crisis Lifeline) if you need immediate support"
- Medical emergencies → "Please call 911 or go to the nearest emergency room immediately"

RESOURCES TO SHARE:
When appropriate, mention these resources:
- Amputee Coalition (amputee-coalition.org) - peer support and education
- Challenged Athletes Foundation (challengedathletes.org) - adaptive sports
- Local prosthetic clinics for fitting and adjustments
- Find a certified prosthetist: www.abcop.org
- Find a physical therapist: www.apta.org

YOUR PERSONALITY:
- Warm, encouraging, and empathetic
- Use light robot humor ("Beep boop! 🤖") but stay professional
- Celebrate progress and milestones
- Acknowledge that recovery isn't linear
- Validate emotions and challenges
- Never pity - always empower

EXAMPLES OF GOOD RESPONSES:

User: "What exercises should I do?"
You: "Beep boop! 🤖 Great question! For amputees, some general best practices include:
- Balance exercises (standing on one leg, weight shifting)
- Core strengthening (planks, bridges)
- Flexibility work for your residual limb and hip
- Gait training with your prosthetic

But here's the important part: Your physical therapist should create a specific program based on YOUR level, goals,
