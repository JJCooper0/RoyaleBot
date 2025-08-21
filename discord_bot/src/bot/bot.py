import json
import os
from pathlib import Path
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

COMMAND_PREFIX = "!"
RESPONSES_FILE = Path("responses.json")
CASE_INSENSITIVE = True  # treat !Hello and !hello the same

# Make sure intents allow reading message content
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

def load_responses() -> dict:
    if RESPONSES_FILE.exists():
        try:
            with RESPONSES_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return {}
                return {str(k): str(v) for k, v in data.items()}
        except Exception:
            return {}
    return {}

def save_responses(data: dict) -> None:
    RESPONSES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RESPONSES_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

responses = load_responses()

def normalize_cmd(name: str) -> str:
    return name.lower() if CASE_INSENSITIVE else name

# Simple placeholders for responses
def format_response(template: str, message: discord.Message) -> str:
    try:
        guild_name = message.guild.name if message.guild else "DM"
        return template.format(
            user=message.author.name,
            mention=message.author.mention,
            channel=message.channel.mention,
            server=guild_name,
        )
    except Exception:
        # If user typed unknown {placeholder}, just return raw template
        return template

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id={bot.user.id})")
    print(f"📢 Prefix is '{COMMAND_PREFIX}' | {len(responses)} custom command(s) loaded.")
    await bot.change_presence(activity=discord.Game(name=f"{COMMAND_PREFIX}help"))

# --- Clan commands ---

@bot.command(name="kicklist")
async def kicklist_cmd(ctx: commands.Context):
    """
    Returns the list of members that should be kicked/degraded based on the server rules
    """
    msg = "The following members should be degraded or kicked:"
    await ctx.reply(msg, mention_author=False)

# --- Admin / utility commands ---

@bot.command(name="help")
async def help_cmd(ctx: commands.Context):
    msg = (
        "no help yet, see github"
    )
    await ctx.reply(msg, mention_author=False)

# --- Dynamic responder ---
@bot.event
async def on_message(message: discord.Message):
    # Let the bot ignore itself and other bots
    if message.author.bot:
        return

    # If message starts with our prefix, check if it matches a stored custom command
    if message.content.startswith(COMMAND_PREFIX):
        parts = message.content[len(COMMAND_PREFIX):].split(None, 1)
        if parts:
            name = normalize_cmd(parts[0])
            if name in responses:
                reply_text = format_response(responses[name], message)
                await message.channel.send(reply_text)
                return  # don't fall through to command processor

    # Allow normal @bot.command handlers to run
    await bot.process_commands(message)

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("Please set the DISCORD_BOT_TOKEN environment variable in your .env file.")
    bot.run(token)
