import os
import random
from discord.ext import commands
from discord import app_commands
import discord

# ── Configuration ─────────────────────────────────────────────────────────────
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
PREFIX = "!"

if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise RuntimeError(
        "Missing Discord bot token. Set the DISCORD_BOT_TOKEN environment variable."
    )

# ── Bot Setup ──────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
tree = bot.tree

# ══════════════════════════════════════════════════════════════════════════════
# EVENTS
# ══════════════════════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Slash commands synced | Serving {len(bot.guilds)} guild(s)")

# ══════════════════════════════════════════════════════════════════════════════
# FUN / GAMES COMMANDS
# ══════════════════════════════════════════════════════════════════════════════
@tree.command(name="roll", description="Roll a dice (e.g. 1d20, 2d6).")
@app_commands.describe(dice="Dice notation like 1d6 or 2d20")
async def roll(interaction: discord.Interaction, dice: str = "1d6"):
    try:
        count, sides = map(int, dice.lower().split("d"))
        if count < 1 or sides < 2 or count > 20:
            raise ValueError
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)
        rolls_str = ", ".join(str(r) for r in rolls)
        await interaction.response.send_message(f"🎲 Rolled **{dice}**: [{rolls_str}] → **Total: {total}**")
    except (ValueError, AttributeError):
        await interaction.response.send_message("❌ Invalid dice format. Use something like `1d6` or `2d20`.", ephemeral=True)

@tree.command(name="coinflip", description="Flip a coin!")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await interaction.response.send_message(f"The coin landed on **{result}**!")

@tree.command(name="8ball", description="Ask the magic 8-ball a question.")
@app_commands.describe(question="Your question for the 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "✅ It is certain.", "✅ Without a doubt.", "✅ Yes, definitely.",
        "✅ You may rely on it.", "🤔 Ask again later.", "🤔 Cannot predict now.",
        "❌ Don't count on it.", "❌ My reply is no.", "❌ Very doubtful."
    ]
    await interaction.response.send_message(f"🎱 **{question}**\n> {random.choice(responses)}")

@tree.command(name="rps", description="Play Rock, Paper, Scissors against the bot.")
@app_commands.describe(choice="Your choice: rock, paper, or scissors")
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
])
async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)
    emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    user = choice.value
    outcomes = {
        ("rock", "scissors"): "win", ("paper", "rock"): "win", ("scissors", "paper"): "win",
        ("rock", "paper"): "lose", ("paper", "scissors"): "lose", ("scissors", "rock"): "lose",
    }
    result = outcomes.get((user, bot_choice), "tie")
    result_text = {"win": "🎉 You win!", "lose": "😔 You lose!", "tie": "🤝 It's a tie!"}[result]
    await interaction.response.send_message(
        f"You chose {emojis[user]} **{user}** | I chose {emojis[bot_choice]} **{bot_choice}**\n{result_text}"
    )

@tree.command(name="joke", description="Get a random joke.")
async def joke(interaction: discord.Interaction):
    jokes = [
        ("Why don't scientists trust atoms?", "Because they make up everything! 😄"),
        ("I told my wife she was drawing her eyebrows too high.", "She looked surprised. 😂"),
        ("Why don't skeletons fight each other?", "They don't have the guts. 💀"),
        ("What do you call a fish without eyes?", "A fsh! 🐟"),
        ("Why did the scarecrow win an award?", "Because he was outstanding in his field! 🌾"),
    ]
    setup, punchline = random.choice(jokes)
    await interaction.response.send_message(f"😂 **{setup}**\n||{punchline}||")

# ══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLER
# ══════════════════════════════════════════════════════════════════════════════
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if interaction.response.is_done():
        await interaction.followup.send(f"⚠️ An error occurred: `{error}`", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ An error occurred: `{error}`", ephemeral=True)
    raise error

# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════
bot.run(TOKEN)
