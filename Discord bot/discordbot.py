import os
import discord
import requests
import asyncio
import youtube_dl
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# ✅ Load the Bot Token securely from environment variables
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Check if the token is missing
if not BOT_TOKEN:
    raise ValueError("🚨 Bot token is missing! Set DISCORD_BOT_TOKEN as an environment variable.")

# ✅ Enable Privileged Intents (Ensure these are enabled in the Developer Portal)
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Needed for welcome messages
intents.message_content = True  # Important for commands

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

# ✅ Store reminders and poll data
reminders = {}
polls = {}
music_queue = []

### 📌 Gemini API Function (For AI chat & summaries)
def gemini_query(message):
    if not GEMINI_API_KEY:
        return "🚨 Gemini API Key is missing!"
    
    response = requests.post(
        "https://api.gemini.com/v1/query",
        json={"input": message, "key": GEMINI_API_KEY}
    )
    return response.json().get('output', '⚠ Unable to fetch response')

### 📌 Event: Bot Ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    scheduler.start()  # Start the scheduler

### 📌 Event: Welcome New Members
@bot.event
async def on_member_join(member):
    await member.send(f"🎉 Welcome to the server, {member.name}! Enjoy your stay.")

### 📌 AI Chat (Gemini API)
@bot.command(name='chat')
async def chat(ctx, *, message: str):
    response = gemini_query(message)
    await ctx.send(response)

### 📌 Summarize Long Messages (Gemini API)
@bot.command(name='summarize')
async def summarize(ctx, *, text: str):
    summary = gemini_query(text)
    await ctx.send(f"**Summary:** {summary}")

### 📌 Set Reminder
@bot.command(name='remind')
async def set_reminder(ctx, time: str, *, message: str):
    try:
        reminder_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        delay = (reminder_time - datetime.now()).total_seconds()
        
        if delay <= 0:
            await ctx.send("🚫 Please specify a future time.")
            return
        
        job = scheduler.add_job(reminder, 'date', run_date=reminder_time, args=[ctx, message])
        reminders[ctx.author.id] = job
        await ctx.send(f"⏰ Reminder set for {time}")
    except ValueError:
        await ctx.send("⚠ Invalid time format! Use: **YYYY-MM-DD HH:MM:SS**")

async def reminder(ctx, message):
    await ctx.send(f"🔔 Reminder: {message}")

### 📌 Auto-Delete Expired Reminders
@scheduler.scheduled_job('interval', seconds=30)
async def check_expired_reminders():
    for user_id, job in list(reminders.items()):
        if job.next_run_time and job.next_run_time <= datetime.now():
            reminders.pop(user_id)
            job.remove()

### 📌 Poll Creation
@bot.command(name='poll')
async def create_poll(ctx, question: str, *options):
    if len(options) < 2:
        await ctx.send("⚠ Provide at least two options for the poll.")
        return

    poll_message = f"📊 **{question}**\n"
    for i, option in enumerate(options):
        poll_message += f"{chr(97+i)}. {option}\n"
    
    poll_message += "React with the corresponding letter to vote!"
    poll_msg = await ctx.send(poll_message)

    for i in range(len(options)):
        await poll_msg.add_reaction(chr(97+i))

### 📌 Music: Play Songs
@bot.command(name='play')
async def play(ctx, url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        music_queue.append(url2)

    await ctx.send(f"🎶 Added to queue: {url}")

### 📌 Music: Skip Song
@bot.command(name='skip')
async def skip(ctx):
    if music_queue:
        song = music_queue.pop(0)
        await ctx.send(f"⏭ Skipping: {song}")
    else:
        await ctx.send("🚫 No song in queue.")

# ✅ Run the bot
bot.run(BOT_TOKEN)
