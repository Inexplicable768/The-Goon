import os
import random

import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup

# setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
permissions_integer = 586005375540800
version = "v1.0.0"


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


async def list_members(guild: discord.Guild):
    return [member async for member in guild.fetch_members(limit=50)]


# === events ===
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_member_join(member):
    # Replace with your actual channel name or ID
    channel = discord.utils.get(member.guild.text_channels, name='general')

    if channel:
        await channel.send(f"👋 Hello im, {member.mention}! {version}")
        await channel.send(
            "https://tenor.com/view/it's-been-awhile-its-been-a-while-omni-man-omni-man-meme-invincible-gif-17023911097105463424"
        )
    else:
        print("Channel not found.")


# === commands ===
about_i = [
    "I am the goon *belches loudly*",
    "I have no idea why I exist why are you asking me nerd",
    "Tell me about you first", "We can be bees!", "Gaze upon my massive belly"
]

bird_images = [
    "https://upload.wikimedia.org/wikipedia/commons/3/32/House_sparrow04.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/12/Northern_Cardinal_Male-27527-2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/8/8e/Blue_Jay_in_Lincroft.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f3/American_Robin_2006.jpg",
    # Add more if needed
]

iris_songs = [
    "https://www.youtube.com/watch?v=nVSa9OJboIM",
    "https://www.youtube.com/watch?v=3HR52f-T7s8",
    "https://www.youtube.com/watch?v=U4ZspzDkm4Q",
    "https://www.youtube.com/watch?v=5y8AT2h04Q4",
    # Add more if needed
]


@bot.command()
async def about(ctx):
    await ctx.send(random.choice(about_i))


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Ping Latency: {latency} ms")


@bot.command()
async def roll_die(ctx, sides: int):
    choice = random.randint(1, sides)
    await ctx.send(f"You rolled a: {choice}")


@bot.command()
async def flip_coin(ctx):
    await ctx.send(f"Coin Flip: {random.choice(['Heads', 'Tails'])}")


@bot.command()
async def random_user(ctx):
    members = await list_members(ctx.guild)
    selected = random.choice(members)
    await ctx.send(f"Selected: {selected.display_name}")


@bot.command()
async def marry_boff_kill(ctx):
    members = await list_members(ctx.guild)
    selected = random.sample(members, 3)
    await ctx.send(f"MBK: {', '.join(m.display_name for m in selected)}")


@bot.command()
async def phasmo_item(ctx):
    items = [
        "Video Camera", "Photo Camera", "Tripod", "D.O.T.S", "UV Light",
        "Salt", "Sanity Pills", "Smudge & Matches", "Sound Recorder",
        "Sound Sensor", "Crucifix", "Para-mic", "EMF Reader", "Thermometer",
        "Candle", "Notepad", "Spirit Box", "Motion Sensor", "Headgear",
        "Flashlight"
    ]
    await ctx.send(f"Item Selected: {random.choice(items)}")


@bot.command()
async def phasmo_ghosts(ctx):
    ghosts = [
        "Spirit", "Wraith", "Phantom", "Poltergeist", "Banshee", "Jinn",
        "Mare", "Revenant", "Shade", "Demon", "Yurei", "Oni", "Yokai", "Hantu",
        "Goryo", "Myling", "Onryo", "The Twins", "Raiju", "Obake", "The Mimic",
        "Moroi", "Deogen", "Thaye"
    ]
    await ctx.send(f"Ghost Selected: {random.choice(ghosts)}")


@bot.command()
async def bird_picture(ctx):
    await ctx.send(random.choice(bird_images))


@bot.command()
async def weather(ctx, zipcode: int):
    lat, lon = get_coordinates_from_zip(zipcode)
    if lat is None:
        await ctx.send("Could not find location for that ZIP code.")
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
        await ctx.send(f"Weather at {zipcode}:")
        await ctx.send(
            f"Temperature: {weather['temperature']}°C / {far(float(weather['temperature'])):.1f}°F"
        )
        await ctx.send(f"Wind Speed: {weather['windspeed']} km/h")
        await ctx.send(
            f"Rain (next hour): {data['hourly']['precipitation'][0]} mm")

    except Exception as e:
        print("Weather error:", e)
        await ctx.send("Failed to fetch weather data.")


@bot.command()
async def random_list(ctx, *args):
    """Choose a random item from a user-given list"""
    if not args:
        await ctx.send("Please give me a list to pick from.")
        return
    await ctx.send(f"Selected: {random.choice(args)}")


@bot.command()
async def iris(ctx):
    await ctx.send(random.choice(iris_songs))


@bot.command()
async def dragonforce(ctx):
    await ctx.send("https://www.youtube.com/watch?v=0jgrCKhxE1s")


@bot.command()
async def join(ctx):
    """Joins your voice channel"""
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("Joined your voice channel!")
    else:
        await ctx.send("You need to be in a voice channel first.")


@bot.command()
async def roulette(ctx, color: str, num: str, money=100):
    """Play Roulette. Bet on a number or color. enter NONE for number to bet on color only"""
    color = color.strip().lower()
    number = random.randint(0, 36)
    if number == 0:
        winning_color = 'green'
    elif number % 2 == 0:
        winning_color = 'black'
    else:
        winning_color = 'red'
    await ctx.send("The ball landed on {} {}".format(winning_color, number))
    if color == winning_color and num == 'NONE' and winning_color != 'green':
        money *= 2
        await ctx.send(
            "You won with a payout of 2:1. Your money is now {}".format(money))
    elif color == 'NONE' and num == str(
            number) or winning_color == color and winning_color == 'green':
        money *= 36
        await ctx.send(
            "You won with a payout of 35:1. Your money is now {}".format(money)
        )
    await ctx.send("Play Again? Y/N")
    response = await bot.wait_for(
        'message', check=lambda message: message.author == ctx.author)
    if response.content.lower() == 'y':
        await roulette(ctx, color, num, money)
    else:
        await ctx.send("Ended with a total of {}".format(money))
        return 0


@bot.command()
async def get_top_sales(ctx, limit=15):
    """Get the top games on sale from Steam"""
    url = "https://store.steampowered.com/search/?specials=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select(".search_result_row")
    print(f"Top {limit} games on sale:\n")

    for result in results[:limit]:
        title = result.select_one(".title").text.strip()
        discount = result.select_one(".search_discount span")
        price = result.select_one(".search_price_discount_combined")
        link = result["href"]

        discount_text = discount.text.strip() if discount else "No discount"
        price_text = price.text.strip().replace("\n", " ") if price else "N/A"

        await ctx.send(
            f"{title}  Discount: {discount_text}  Price: {price_text}\n  Link: {link}\n"
        )


@bot.command()
async def truth_or_dare(ctx):
    truths = [
        "What’s the weirdest thing you’ve ever eaten?",
        "What's your least favorite anime",
        "What’s your favorite song?",
        "Have you ever lied to get out of trouble?",
        "What’s something you’ve never told anyone?"
        "What’s the most embarrassing thing that has happened to you?",
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
    await ctx.send("Truth or Dare?")
    response = await bot.wait_for(
        'message', check=lambda message: message.author == ctx.author)
    if response.content.lower() == 'truth':
        await ctx.send(random.choice(truths))
        return
    elif response.content.lower() == 'dare':
        await ctx.send(random.choice(dares))
        return


# === Start Bot ===
if __name__ == "__main__":
    try:
        token = os.getenv("TOKEN") or ""
        if not token:
            raise ValueError("Missing TOKEN environment variable.")
        bot.run(token)
    except Exception as e:
        print("Bot failed to start:", e)
