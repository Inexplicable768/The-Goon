
import asyncio
import json
import os
import random

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

### A DISCORD BOT MADE BY INEXPLICABLE768 ###
### THE GOON. WHO IS THE GOON? THE GOON IS ME ###
### ENJOY THE CODE IG ###

# setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)
client = discord.Client(intents=intents)
DATA_FOLDER = "./data"

user_agent = {
    "User-Agent": "https://replit.com/@mathematicaency/TheGoon#main.py, v1.0)"
}
custom_emojis = ["<:ocelot:1394152101864669235>", "<:lazermax:1394151691749949632>", "<:orangeman:1394151590553980998>",
                "<a:fdiscordmods:1394151257375113458>", "<:killme:1394151095122792448>", "<:missing:1394150968706469938>",
                "<:vincentvangofyourself:1394150760027127900>", "<:cornluke:1394150657577189479>", "<:max:1394150597514498128>",
                "<:letmegoon:1394150527528337419>", "<:garlicquentin:1394150107145965729>", "<:andrewvodka:1394150028163027076>",
                "<:thatspea:1394149976439001200>", "<:meltingdrew:1394149942301294765>", "<:idontmindthesmell:1394149520710832218>",
                "<:hammers:1394149453107040338>", "<:getajob:1394022666314322012>", "<:diddytesla:1394022591177429012>",
                "<:thegoon:1394022544218001459>"]
def read_points(server_id: str):
    filename = f"{server_id}_points.json"
    try:
        with open(filename, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"[{server_id}] Points file missing or corrupted. Will create new one.")
        return {}

def write_points(server_id, points):
    filename = os.path.join(f"{server_id}_points.json")
    try:
        with open(filename, 'w') as f:
            json.dump(points, f, indent=2)
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False
        
# this should help the bot stay in the call
class Silence(discord.PCMVolumeTransformer):
    def __init__(self):
        super().__init__(discord.FFmpegPCMAudio("pipe:0", pipe=True, stderr=None, before_options="-f lavfi -i anullsrc=r=48000:cl=stereo"))
    def read(self):
        return b'\x00' * 3840  # 20ms of stereo silence at 48kHz (2 channels * 2 bytes * 960 samples)

# constants
permissions_integer = 586005375540800
version = "v1.3.2"
# brainrot hangman
WORDS = ["bigger", 'hawk tuah', 'skibidi', 'fuck you', 'david marshall', 'omniman', 
         'kill your self', 'troth senchal', 'coomer', 'kambabala', 'make america gay again',
         'get off my tower', 'whats the pissue', 'tung tung tung sahur', 'bombardino crocadilo',
         'cotton picking cute', 'dennys footjob', 'sandwich', 'huniepopping cherrypopping',
         'speak to me', 'a steak', 'we need to goon', 'Beta', 'gyatt', ''
        ]
games = {}
numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
about_i = [
    "I am the goon *belches loudly*",
    "I have no idea why I exist why are you asking me nerd",
    "Tell me about you first", "We can be bees!", "Gaze upon my massive belly",
    "https://tenor.com/view/it's-been-awhile-its-been-a-while-omni-man-omni-man-meme-invincible-gif-17023911097105463424"
]

bird_images = [
    "https://plus.unsplash.com/premium_photo-1661962626711-8121c34826c2?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZnVubnklMjBiaXJkfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1680749512096-9bd509915e53?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZnVubnklMjBiaXJkfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1581362662614-dd27d9eb9291?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8ZnVubnklMjBiaXJkfGVufDB8fDB8fHww",
    "https://plus.unsplash.com/premium_photo-1669810168690-dfc19be1e765?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8ZnVubnklMjBiaXJkfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1620093339029-ad07db9d6d35?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1592620478369-e0e0d12e9564?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjJ8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1659884535789-539040dbbfeb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mjl8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1699735129464-4aad9f54fa7b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDN8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1705351978886-3b7d1e211753?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDV8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://plus.unsplash.com/premium_photo-1694621017917-bd784f857235?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTl8fGZ1bm55JTIwYmlyZHxlbnwwfHwwfHx8MA%3D%3D",
    "https://images.unsplash.com/photo-1694316286534-3304eb00c455?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTA5fHxmdW5ueSUyMGJpcmR8ZW58MHx8MHx8fDA%3D",
    "https://plus.unsplash.com/premium_photo-1674381523736-e6fdc5c1e708?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTExfHxmdW5ueSUyMGJpcmR8ZW58MHx8MHx8fDA%3D",
    "https://images.unsplash.com/photo-1699735129478-f89275a3e601?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTIxfHxmdW5ueSUyMGJpcmR8ZW58MHx8MHx8fDA%3D",
    "https://vistapointe.net/images/vladimir-putin-4.jpg"

]

verses = [
    "John 3:16", "Genesis 1:1", "Psalm 23:1", "Romans 8:28", "Philippians 4:13",
    "Proverbs 3:5", "Isaiah 41:10", "Matthew 6:33", "Jeremiah 29:11", "1 Corinthians 13:4",
    "Romans 12:2", "Joshua 1:9", "Hebrews 11:1", "1 John 4:8", "Psalm 46:10",
    "2 Timothy 1:7", "James 1:5", "Matthew 11:28", "Ephesians 2:8", "Galatians 5:22",
    "Isaiah 40:31", "Matthew 5:16", "Colossians 3:23", "Psalm 119:105", "1 Thessalonians 5:16",
    "Romans 5:8", "John 14:6", "Proverbs 18:10", "Romans 10:9", "1 Peter 5:7",
    "2 Chronicles 7:14", "Psalm 37:4", "John 8:12", "Romans 6:23", "Luke 6:31",
    "Philippians 4:6", "Proverbs 16:3", "Matthew 28:19", "1 Corinthians 10:13", "Psalm 34:18",
    "Isaiah 26:3", "Galatians 2:20", "1 John 1:9", "Exodus 14:14", "Psalm 121:1",
    "2 Corinthians 5:17", "Hebrews 13:5", "Acts 1:8", "Ephesians 6:11", "James 1:2",
    "Micah 6:8", "Matthew 22:37", "Lamentations 3:22", "Romans 15:13", "Isaiah 43:2",
    "1 Corinthians 15:58", "Philippians 2:3", "Ephesians 4:29", "Psalm 19:14", "Deuteronomy 31:6",
    "Colossians 3:2", "2 Corinthians 12:9", "Hebrews 4:12", "Matthew 7:7", "Romans 8:38",
    "Psalm 91:1", "Ecclesiastes 3:1", "1 Corinthians 6:19", "Proverbs 4:23", "Galatians 6:9",
    "Titus 2:11", "Nahum 1:7", "Zephaniah 3:17", "Mark 12:30", "Psalm 139:14",
    "Luke 1:37", "Matthew 5:14", "1 John 5:14", "James 4:7", "Proverbs 27:17",
    "Psalm 27:1", "Isaiah 53:5", "Ephesians 3:20", "Hebrews 10:24", "Colossians 2:6",
    "2 Peter 3:9", "1 Timothy 6:12", "Job 19:25", "Psalm 30:5", "Luke 11:9",
    "Romans 3:23", "John 10:10", "Isaiah 55:8", "Matthew 18:20", "Revelation 21:4",
    "Acts 2:38", "John 15:5", "Psalm 90:12", "Ephesians 5:2", "1 John 2:17",
    "2 Timothy 3:16", "Psalm 100:4", "Matthew 6:9", "Hebrews 12:1", "Jeremiah 17:7"
]

iris_songs = [
    "https://www.youtube.com/watch?v=nVSa9OJboIM",
    "https://www.youtube.com/watch?v=3HR52f-T7s8",
    "https://www.youtube.com/watch?v=U4ZspzDkm4Q",
    "https://www.youtube.com/watch?v=5y8AT2h04Q4",
    "https://www.youtube.com/watch?v=lj565P1LjaM",
    "https://www.youtube.com/watch?v=5y8AT2h04Q4",
    "https://www.youtube.com/watch?v=o8hmMQYcL2M",
    "https://www.youtube.com/watch?v=ih_ITHGM_Uo",
    "https://www.youtube.com/watch?v=L7yjXlmDZ_A",
    "https://www.youtube.com/watch?v=8AdYz4Y0pUs",
    "https://www.youtube.com/watch?v=drNBS0jjgh8",
    "https://www.youtube.com/watch?v=j4Eoy-8fejM",
    "https://www.youtube.com/watch?v=CwrsUzyqflU",
    "https://www.youtube.com/watch?v=c9cvcQGXMdw",
]
hawk_tuah_asmr = [
    ""
]
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'extract_flat': False
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# === utilities ===
def get_coordinates_from_zip(zip_code: int, country="US"):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": zip_code,
        "country": country,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "weather-info-goon"}
    response = requests.get(url, params=params, headers=headers)
    results = response.json()
    if results:
        lat = float(results[0]['lat'])
        lon = float(results[0]['lon'])
        return lat, lon
    return None, None


def far(celcius: float):
    return celcius * 1.8 + 32
def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02}:{minute:02}"
def clear_slop():
    pass

async def list_members(guild: discord.Guild):
    return [member async for member in guild.fetch_members(limit=50)]


# === events ===

@client.event
async def on_message(message):
    if message.author.bot:
        return
    print(message.content)
    if "fuck" in message.content:
        await message.channel.send("Oopsie poopsie you said a no no word.")
        
# loading event code
@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f"Connected to guild: {guild.name} (ID: {guild.id})")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally")

        for guild in bot.guilds:
            guild_obj = discord.Object(id=guild.id)
            synced_guild = await bot.tree.sync(guild=guild_obj)
            print(f"Synced {len(synced_guild)} commands to {guild.name}")

    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print(f"Bot is online as {bot.user}")

# when a member joins
@bot.event
async def on_member_join(member):
    channels = ['main', 'general', 'welcome', 'home', 'hello']
    for n in channels:
        channel = discord.utils.get(member.guild.text_channels, name=n)
        if channel:
            await channel.send(f"Hello, {member.mention} welcome.")
            await channel.send(
                "https://tenor.com/view/it's-been-awhile-its-been-a-while-omni-man-omni-man-meme-invincible-gif-17023911097105463424"
            )
            break
        else:
            print("Channel not found :(")




# === commands ===


@bot.tree.command(name="gpurge", description="remove the last n messages in the channel. Admin use only. Can take max 1000")
@app_commands.checks.has_permissions(administrator=True)
async def gpurge(interaction: discord.Interaction, amount: int):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command can only be used in a text channel.")
        return
    if amount > 1000:
        await interaction.response.send_message("You can only delete up to 1000 messages at a time.")
        return
    await interaction.response.defer()
    deleted = await interaction.channel.purge(limit=amount)


@bot.tree.command(name="about", description="A totally normal about message")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(about_i))

@bot.tree.command(name="debug", description="Intended for admins. A way to see if the bot is working and see info about the server")
async def debug(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bot User Id {bot.user} \n Connected to guild: {interaction.guild.name}\n (ID: {interaction.guild.id}) \nBot version: {version} \nBot latency: {round(bot.latency * 1000)} ms \n Bot permissions: {permissions_integer}")

@bot.tree.command(name="ping_me", description="Ping the bot to see latency")
async def ping_me(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Ping Latency: {latency} ms")


@bot.tree.command(name="roll_die", description="Roll an n sided die")
async def roll_die(interaction: discord.Interaction, sides: int):
    choice = random.randint(1, sides)
    await interaction.response.send_message(f":game_die: You rolled a: {choice}")


@bot.tree.command(name="flip_coin",
                  description="Flip a coin, what else do you want...")
async def flip_coin(interaction: discord.Interaction):
    await interaction.response.send_message(f"Coin Flip: {random.choice(['Heads', 'Tails'])}")


@bot.tree.command(
    name="random_user",
    description=
    "Picks a random user from the server. Do what you want with this info, im not your mom"
)
async def random_user(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return 
    members = await list_members(interaction.guild)
    selected = random.choice(members)
    await interaction.response.send_message(f"Selected: {selected.display_name}")


@bot.tree.command(name="marry_kiss_kill",
                  description="A totally family friendly game. Choose 1 to marry, 1 to kiss, 1 to kill. YOU HAVE TO.")
async def marry_boff_kill(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return 
    members = await list_members(interaction.guild)
    selected = random.sample(members, 3)
    await interaction.response.send_message(f"MBK: {', '.join(m.display_name for m in selected)}")

@bot.tree.command(name="drinking_game", description="Take a drink every time what the goon says happens")
async def drinking_game(interaction: discord.Interaction):
    await interaction.response.send_message("DONT DRINK KIDS")

@bot.tree.command(
    name="phasmo_item",
    description="Helpful for phasmophobia tarot card roulette or other uses")
async def phasmo_item(interaction: discord.Interaction):
    items = [
        "Video Camera", "Photo Camera", "Tripod", "D.O.T.S", "UV Light",
        "Salt", "Sanity Pills", "Smudge & Matches", "Sound Recorder",
        "Sound Sensor", "Crucifix", "Para-mic", "EMF Reader", "Thermometer",
        "Candle", "Notepad", "Spirit Box", "Motion Sensor", "Headgear",
        "Flashlight"
    ]
    await interaction.response.send_message(f"Item Selected: {random.choice(items)}")


@bot.tree.command(name="phasmo_ghosts", description="Bet on a random ghost")
async def phasmo_ghosts(interaction: discord.Interaction):
    ghosts = [
        "Spirit", "Wraith", "Phantom", "Poltergeist", "Banshee", "Jinn",
        "Mare", "Revenant", "Shade", "Demon", "Yurei", "Oni", "Yokai", "Hantu",
        "Goryo", "Myling", "Onryo", "The Twins", "Raiju", "Obake", "The Mimic",
        "Moroi", "Deogen", "Thaye"
    ]
    await interaction.response.send_message(f"Ghost Selected: {random.choice(ghosts)}")

@bot.tree.command(name="custom_emoji_list", description="List of custom emojis by the goon")
async def custom_emoji_list(interaction: discord.Interaction):
    await interaction.response.send_message(custom_emojis)

@bot.tree.command(name="custom_emoji_react", description="React to the previous message with a custom emoji")
async def custom_emoji_react(interaction: discord.Interaction, emoji: str):
    index = [i for i, s in enumerate(custom_emojis) if emoji in s]
    if not len(index):
        await interaction.response.send_message("Invalid emoji")
        return
    messages = [msg async for msg in interaction.channel.history(limit=5)]
    for msg in messages:
        try:
            await msg.add_reaction(custom_emojis[index[0]])
            return
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Failed to react: {str(e)}", ephemeral=True)
            return
    
@bot.tree.command(name="custom_emoji", description="Send a custom emoji via the goon")
async def custom_emoji(interaction: discord.Interaction, emoji: str):
    index = [i for i, s in enumerate(custom_emojis) if emoji in s]
    if not len(index):
        await interaction.response.send_message("Invalid emoji")
        return
    messages = await interaction.channel.history(limit=2).flatten()
    if len(messages) < 2:
        print("Error no messages")
    else:
        previous_message = messages[1]  
        await previous_message.send_message(custom_emojis[index[0]])
    

@bot.tree.command(name="bird_picture",
                  description="Why youd need this im not sure but here it is")
async def bird_picture(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(bird_images))


@bot.tree.command(name="weather", description="wanna touch grass today")
async def weather(interaction: discord.Interaction, zipcode: int):
    lat, lon = get_coordinates_from_zip(zipcode)
    if lat is None:
        await interaction.response.send_message("Could not find location for that ZIP code.")
        return

    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "precipitation"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "current_weather" not in data:
            raise KeyError("Missing 'current_weather'")

        weather = data["current_weather"]
        await interaction.response.send_message(f"Weather at {zipcode}:")
        await interaction.followup.send(
            f"Temperature: {weather['temperature']}°C / {far(float(weather['temperature'])):.1f}°F"
        )
        await interaction.followup.send(f"Wind Speed: {weather['windspeed']} km/h")
        await interaction.followup.send(
            f"Rain (next 3 hours): {data['hourly']['precipitation'][0]} mm , {data['hourly']['precipitation'][1]} mm, {data['hourly']['precipitation'][2]} mm")

    except Exception as e:
        print("Weather error:", e)
        await interaction.response.send_message("Failed to fetch weather data.")


@bot.tree.command(name="random_list", description="pick from a list of things")
async def random_list(interaction: discord.Interaction, args: str):
    """Choose a random item from a user-given list"""
    if not args:
        await interaction.response.send_message("Please give me a list to pick from.")
        return
    await interaction.response.send_message(f"Selected: {random.choice(args)}")


@bot.tree.command(name="iris",
                  description="play a PEAK song from IRIS offical")
async def iris(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(iris_songs))


@bot.tree.command(name="did_you_pray_today", description="Did you pray today?")
async def did_you_pray_today(interaction: discord.Interaction):
    await interaction.response.send_message("Did you pray today?")
    await interaction.followup.send("https://www.youtube.com/watch?v=cMsoDefWep8")


@bot.tree.command(name="asmr",
                  description="sends a relaxing asmr video... yes")
async def asmr(interaction: discord.Interaction):
    await interaction.response.send_message("Sleep fam")
    await interaction.followup.send("https://www.youtube.com/watch?v=rvoLyfQSN1w")


@bot.tree.command(name="dragonforce", description="epic")
async def dragonforce(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.youtube.com/watch?v=cqH1kMG5P0Q")



@bot.tree.command(name="roulette", description="Test your luck at roulette")
async def roulette(interaction: discord.Interaction, color: str, num: str, money: int = 100) -> None:
    """Play Roulette. Bet on a number or color. enter NONE for number to bet on color only"""
    color = color.strip().lower()
    number = random.randint(0, 36)
    if number == 0:
        winning_color = 'green'
    elif number % 2 == 0:
        winning_color = 'black'
    else:
        winning_color = 'red'

    await interaction.response.send_message("The ball landed on {} {}".format(winning_color, number))

    # Check for wins
    if color == winning_color and num == 'NONE' and winning_color != 'green':
        money *= 2
        await interaction.followup.send(
            "You won with a payout of 2:1. Your money is now {}".format(money))
    elif color == 'NONE' and num == str(number) or winning_color == color and winning_color == 'green':
        money *= 36
        await interaction.followup.send(
            "You won with a payout of 35:1. Your money is now {}".format(money))
    else:
        await interaction.followup.send("You lost! Your money is now {}".format(money))

    await interaction.followup.send("Thanks for playing! Use the command again to play another round.")


@bot.tree.command(name='blackjack', description="Play blackjack")
async def blackjack(interaction: discord.Interaction, money: int = 100):
    """Play Blackjack"""
    deck = [n + ' of ' + s for n in numbers for s in suits]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    await interaction.response.send_message("Card: {}".format(player_hand[0]))
    await interaction.followup.send("hit or stand?")
    while True:
        response = await bot.wait_for(
            'message', check=lambda message: message.author == interaction.user)
        if response.content.lower() == 'hit':
            player_hand.append(deck.pop())
            await interaction.followup.send("Card: {}".format(player_hand[-1]))
            if sum([int(card.split()[0]) for card in player_hand]) > 21:
                await interaction.followup.send("Bust! You lose.")
                break
        elif response.content.lower() == 'stand':
            while sum([int(card.split()[0]) for card in dealer_hand]) < 17:
                dealer_hand.append(deck.pop())
            await interaction.followup.send("Dealer's hand: {}".format(dealer_hand))
            if sum([int(card.split()[0]) for card in dealer_hand]) > 21:
                await interaction.followup.send("Dealer busts! You win.")
                money *= 2
                await interaction.followup.send("Your money is now {}".format(money))
            elif sum([int(card.split()[0]) for card in player_hand]) > sum(
                    [int(card.split()[0]) for card in dealer_hand]):
                await interaction.followup.send("You win!")
                money *= 2
                await interaction.followup.send("Your money is now {}".format(money))
            else:
                await interaction.followup.send("You lose.")
            break
        else:
            await interaction.followup.send("Please enter 'hit' or 'stand' or 'quit'.")


@bot.tree.command(name="get_top_sales",
                  description="Check out the top games on sale on steam")
async def get_top_sales(interaction: discord.Interaction, limit: int = 5):
    """Get the top games on sale from Steam. Shows 5 by default"""
    url = "https://store.steampowered.com/search/?specials=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select(".search_result_row")
    print(f"Top {limit} games on sale:\n")

    await interaction.response.send_message(f"Top {limit} games on sale:")

    for result in results[:limit]:
        if result.select_one(".title") is None:
            print("Skipping invalid result")
            continue
        title = result.select_one(".title").text.strip()
        discount = result.select_one(".search_discount span")
        price = result.select_one(".search_price_discount_combined")
        link = result["href"]

        discount_text = discount.text.strip() if discount else "No discount"
        price_text = price.text.strip().replace("\n", " ") if price else "N/A"

        await interaction.followup.send(
            f"{title}  Discount: {discount_text}  Price: {price_text}\n  Link: {link}\n"
        )


@bot.tree.command(name="truth_or_dare",
                  description="I tried to keep it family friendly i promise")
async def truth_or_dare(interaction: discord.Interaction):
    truths = [
        "What's the weirdest thing you've ever eaten?",
        "What's your least favorite anime",
        "What's your favorite song?",
        "Have you ever lied to get out of trouble?",
        "What's something you've never told anyone?"
        "What's the most embarrassing thing that has happened to you?",
        "If you were stranded on an island whats the first thing you'd do?",
        "What is the bordest you've ever been?",
        "What is your opinion on the current president?",
        "What is the dumbest / most cringy thing you've ever said?",
        "If you could only eat one food for the rest of your life what would it be?",
        "Do you prefer hot or cold showers?",
        "What is the worst movie you have ever seen?",
    ]
    dares = [
        "Tell a joke. NOW!",
        "Sing the intro to through the fire and flames",
        "Lick peanut butter off your elbow",
        "DM a random person and talk in brainrot",
        "Play clone hero at 200% speed blindfolded",
        "Play minecraft with your feet for 10 minutes",
        "take a drink every time carney jared says something crazy on his latest stream",
        "Do pushups and say david every time you do one",
        "take a shot of a carbonated drink",
        "sing the national anthem",
        "sing the alphabet backwards",
        "do your best omni man impression"
        "pick a random person and say their name in a french accent",
    ]
    await interaction.response.send_message("Truth or Dare?")
    response = await bot.wait_for(
        'message', check=lambda message: message.author == interaction.user)
    if response.content.lower() == 'truth':
        await interaction.followup.send(random.choice(truths))
        return
    elif response.content.lower() == 'dare':
        await interaction.followup.send(random.choice(dares))
        return




@bot.tree.command(name="tic_tac_toe_h",
                  description="Play tic tac toe with a friend")
async def tic_tac_toe_h(interaction: discord.Interaction, player2: discord.Member):
    turn = 0
    board = [
        ":white_large_square:", ":white_large_square:", ":white_large_square:",
        ":white_large_square:", ":white_large_square:", ":white_large_square:",
        ":white_large_square:", ":white_large_square:", ":white_large_square:"
    ]
    await interaction.response.send_message(f"{player2} Do you accept to play tic tac toe? Y/N")
    response = await bot.wait_for(
        'message', check=lambda message: message.author == player2)
    if response.content.lower() == 'y':
        await interaction.followup.send("Player 1 is X and Player 2 is O")
        await interaction.followup.send(f"Player {turn+1}'s turn")
        await interaction.followup.send(board[0] + board[1] + board[2] + "\n" + board[3] +
                       board[4] + board[5] + "\n" + board[6] + board[7] +
                       board[8])
        while turn != 2:
            response = await bot.wait_for(
                'message',
                check=lambda message: message.author == interaction.user or message.
                author == player2)
            if type(int(response.content)) is int:
                board[int(response.content)] = ":x:" if turn == 0 else ":o:"
                turn = 1 if turn == 0 else 0
                await interaction.followup.send(f"Player {turn+1}'s turn")
                await interaction.followup.send(board[0] + board[1] + board[2] + "\n" +
                               board[3] + board[4] + board[5] + "\n" +
                               board[6] + board[7] + board[8])
            elif response.content.lower() == 'quit':
                await interaction.followup.send("Game ended")
                turn = 2
                break
            else:
                await interaction.followup.send("Please enter a number between 0 and 8")
                continue

    else:
        return
    return


@bot.tree.command(name="hangman", description="Play hangman with questionable words")
async def hangman(interaction: discord.Interaction):
    if not interaction.channel:
        return
    if interaction.channel.id in games:
        await interaction.followup.send("A game is already running in this channel!")
        return
    await interaction.response.send_message("Starting hangman. Use /guess <letter> to guess a letter.")
    word = random.choice(WORDS)
    display = ["_"] * len(word)
    guesses = []
    attempts = 6

    games[interaction.channel.id] = {
        "word": word,
        "display": display,
        "guesses": guesses,
        "attempts": attempts
    }

    await interaction.followup.send(
        f"Hangman started. Word: `{' '.join(display)}`\n"
        f"Guess a letter using `!guess <letter>`"
    )
@bot.command()
async def guess(ctx, letter: str):
    game = games.get(ctx.channel.id)
    if not game:
        await ctx.send("No hangman game is running. Start one with `/hangman`.")
        return
    letter = letter.lower()
    if letter in game["guesses"]:
        await ctx.send(f"You already guessed `{letter}`!")
        return
    game["guesses"].append(letter)
    if letter in game["word"]:
        for i, l in enumerate(game["word"]):
            if l == letter:
                game["display"][i] = letter
        await ctx.send(f"✅ Correct. `{' '.join(game['display'])}`")
    else:
        game["attempts"] -= 1
        await ctx.send(f"❌  `{letter}` isn't in the word. Attempts left: {game['attempts']}")
    if "_" not in game["display"]:
        await ctx.send(f":check: Correct. The word was `{game['word']}`.")
        del games[ctx.channel.id]
    elif game["attempts"] <= 0:
        await ctx.send(f" Game over. The word was `{game['word']}`.")
        del games[ctx.channel.id]


@bot.tree.command(name="dad_joke", description="Get a shitty deplorable joke")
async def dad_joke(interaction: discord.Interaction):
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    joke = response.json()["joke"]
    await interaction.response.send_message(joke)

@bot.tree.command(name="elon_musk_twitter", description="See the crazy ravings of elon musk. I'm not responsible for your sanity")
async def elon_musk_twitter(interaction: discord.Interaction):
    await interaction.response.send_message("https://twitter.com/elonmusk")

@bot.tree.command(name="goon", description="don't enter this command. PLEASE")
async def goon(interaction: discord.Interaction):
    await interaction.response.send_message("FREAK AHH WHY WOULD YOU ENTER THIS COMMAND")
    await interaction.followup.send("https://tenor.com/view/benjammins-gooner-goon-what-a-gooner-simp-gif-6065693207482219935")  
    
# === GeoGuess ===
# rarley do i comment code but this is hard to read
def get_random_coordinate():
    lat = round(random.uniform(-60, 85), 6)
    lon = round(random.uniform(-180, 180), 6)
    return lat, lon

def is_land(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 10,
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "GeoBotDiscord/1.0 (foo@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("address"), data.get("display_name")
        else:
            print("Error:", response.status_code)
            return None, None
    except Exception as e:
        print("Error:", e)
        return None, None
        
def get_osm_map_url(lat, lon, zoom=15, size="800x600"):
    return f"https://staticmap.openstreetmap.de/staticmap.php?center={lat},{lon}&zoom={zoom}&size={size}"


@bot.tree.command(name="geoguesser", description="Guess the location from an image")
async def geoguesser(interaction: discord.Interaction):
    await interaction.response.send_message("Looking for a random location on land. This may take a moment because the api makes me wait.")

    lat, lon = None, None
    address, display_name = None, None

    # Loop until a land location is found. sleep bc api sucks
    while True:
        lat, lon = get_random_coordinate()
        address, display_name = is_land(lat, lon)
        if address: # break when we find a valid location
            break
        await asyncio.sleep(1)  # Rate limit for Nominatim API

    map_url = get_osm_map_url(lat, lon)

    embed = discord.Embed(title="🌍 Guess the location", description="Reply with your guess here in chat within 60 seconds.")
    embed.set_image(url=map_url)
    await interaction.followup.send(embed=embed)

    def check(m):
        return m.channel == interaction.channel and m.author == interaction.user

    try:
        # check if the user's guess is correct
        guess_msg = await bot.wait_for('message', timeout=60.0, check=check)
        country = address.get("country", "").lower()
        state = address.get("state", "").lower()

        guess_content = guess_msg.content.lower()
        if country in guess_content or state in guess_content:
            await interaction.followup.send(f"✅ Correct... wow you are a real nerd The location was: **{display_name}**")
        else:
            await interaction.followup.send(f"❌ Wrong mate. The correct answer was: **{display_name}**")
    except asyncio.TimeoutError:
        await interaction.followup.send(f"⏱️ Too slow. The correct answer was: **{display_name}**")


@bot.tree.command(name="meme", description="Get a random meme from reddit, May or may not be cringe or nsfw")
async def meme(interaction: discord.Interaction):
    url = "https://meme-api.com/gimme"
    response = requests.get(url)
    data = response.json()
    await interaction.response.send_message(data["url"])
    await interaction.followup.send(data["title"] + "" + (data["author"]))


@bot.tree.command(name="bible", description="Let the goon preach to you. Get a random Bible verse.")
async def bible(interaction: discord.Interaction):
    chance = random.randint(1, 100)
    if chance == 1:
        await interaction.response.send_message("Christianity is just a beleif system gooners. there is no evidence for or against it. We dont know if it is true or not or what lies outside of our universe and our lives. We can have faith in a god but we can also have faith in a toaster. Its all up to the human mind that you posess to decide what you beleive in and what happens when we die.")
        return
    chance2 = random.randint(1, 200)
    if chance2 == 1:
        await interaction.response.send_message("Goon 10:23 ling gan guli guli ling wa")
    verse = random.choice(verses)
    url = f"https://bible-api.com/{verse.replace(' ', '%20')}"

    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                message = f"**{data['reference']}**\n{data['text']}"
                await interaction.followup.send(message.replace("Yahweh","God"))
            else:
                await interaction.followup.send("Failed to fetch the verse. Try again later.")


@bot.tree.command(name="flag", description="Get a random flag from the world")
async def flag(interaction: discord.Interaction):
    url = "https://restcountries.com/v3.1/all?fields=name,capital,region,flags"
    response = requests.get(url)
    data = response.json()
    print(data)
    country = random.choice(data)
    try:
        await interaction.response.send_message(country["flags"]["png"])
        await interaction.followup.send(country["name"]["common"])
        await interaction.followup.send(country["capital"][0])
    except Exception as e:
        print(e)


@bot.tree.command(name="join", description="Bot joins your current voice channel.")
async def join(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("This command can only be used in a server.")
        return
    member = interaction.guild.get_member(interaction.user.id)
    if not member or not member.voice:
        await interaction.response.send_message("You are not in a voice channel!", ephemeral=True)
        return

    channel = member.voice.channel
    await channel.connect()
    await interaction.response.send_message(f"Connected to {channel.name}")


@bot.tree.command(name="degoon", description="deletes the last n messages in the channel sent by the goon")
async def degoon(interaction: discord.Interaction, amount: int):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command can only be used in a text channel.")
        return

    await interaction.response.defer()
    deleted = await interaction.channel.purge(limit=amount, check=lambda m: m.author == bot.user)
    await interaction.followup.send(f"Deleted {len(deleted)} messages.")


@bot.tree.command(name="trivia", description="Play a trivia game with a random question")
async def trivia(interaction: discord.Interaction):
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()


@bot.tree.command(name="answer", description="Answer a trivia question")
async def answer(interaction: discord.Interaction, answer: str):
    if not interaction.channel:
        return

@bot.tree.command(name="shrimp", description="Is that shit real man")
async def shrimp(interaction: discord.Interaction):
    await interaction.response.send_message("https://img.ifunny.co/images/9c52b138d1ebf767b59aba505dd66e1d0790a5146b306e63ca4e0a5b5f85cb84_1.jpg")

@bot.tree.command(name="wallet", description="See how many goon points you have")
async def wallet(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    server_id = str(interaction.guild.id)
    user_id = str(interaction.user.id)

    points = read_points(server_id)

    # If user not in points, initialize them
    if user_id not in points:
        points[user_id] = 0
        write_points(server_id, points)
        await interaction.response.send_message("You have 0 goon points. Some day these will replace the dollar trust me")
        return

    user_points = points[user_id]
    await interaction.response.send_message(f"You have {user_points} goon points.")

@bot.tree.command(name="give", description="Give goon points to someone. Admins only")
@app_commands.checks.has_permissions(administrator=True)
async def give(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return
    write_points(str(interaction.guild.id), {str(user.id), amount})
    await interaction.response.send_message("Gave goon points to user")
    
@bot.tree.command(name="suprise", description="Ba da ba ba ba david")
async def suprise(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.youtube.com/watch?v=TtdR-qo910k")

@bot.tree.command(name="omni", description="We can be bees!")
async def omni(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/omni-gyatt-gif-17689339150837030890")

@bot.tree.command(name="cat", description="random cat gif from tenor")
async def cat(interaction: discord.Interaction):
    cats = ["https://tenor.com/view/cat-gif-16258174987336597266", "https://tenor.com/view/cat-cat-with-tongue-cat-smiling-gif-11949735780193730026", "https://tenor.com/view/silly-reaction-meme-stan-twitter-funny-stressed-gif-7713976294327515532"]
    await interaction.response.send_message(random.choice(cats))

@bot.tree.command(name="info", description="Actual info trust me bro")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(f"=== THE GOON ===\n\n a discord bot made by Inexplicable768 (alex). \n version: {version}\nI didnt know i had to put that there")

# === Errors ===

@give.error
async def give_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
@gpurge.error
async def give_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
        
# === Start Bot ===
if __name__ == "__main__":
    try:
        token = os.getenv("TOKEN") or ""
        if not token:
            raise ValueError("Missing TOKEN environment variable.")
        bot.run(token)
    except Exception as e:
        print("Bot failed to start:", e)
