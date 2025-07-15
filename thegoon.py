import os
import random

import discord
import requests
import yt_dlp
from bs4 import BeautifulSoup
from discord.ext import commands

# setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# constants
permissions_integer = 586005375540800
version = "v1.2.0"
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


async def list_members(guild: discord.Guild):
    return [member async for member in guild.fetch_members(limit=50)]


# === events ===
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

@bot.event
async def on_member_join(member):
    channels = ['main', 'general', 'welcome', 'home', 'hello']
    for n in channels:
        channel = discord.utils.get(member.guild.text_channels, name=n)
        if channel:
            await channel.send(f"Hello im, {member.mention} {version}")
            await channel.send(
                "https://tenor.com/view/it's-been-awhile-its-been-a-while-omni-man-omni-man-meme-invincible-gif-17023911097105463424"
            )
            break
        else:
            print("Channel not found :(")


# === commands ===


@bot.tree.command(name="about", description="A totally normal about message")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(about_i))


@bot.tree.command(name="ping_me", description="Ping the bot to see latency")
async def ping_me(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Ping Latency: {latency} ms")


@bot.tree.command(name="roll_die", description="Roll an n sided die")
async def roll_die(interaction: discord.Interaction, sides: int):
    choice = random.randint(1, sides)
    await interaction.response.send_message(f"You rolled a: {choice}")


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


@bot.tree.command(name="marry_boff_kill",
                  description="A totally family friendly game.")
async def marry_boff_kill(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return 
    members = await list_members(interaction.guild)
    selected = random.sample(members, 3)
    await interaction.response.send_message(f"MBK: {', '.join(m.display_name for m in selected)}")


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
    await interaction.response.send_message("https://www.youtube.com/watch?v=0jgrCKhxE1s")


@bot.tree.command(name="join", description="add the bot to your voice channel")
async def join(interaction: discord.Interaction):
    """Joins your voice channel"""
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    member = interaction.guild.get_member(interaction.user.id)
    if member and member.voice and member.voice.channel:
        try:
            await member.voice.channel.connect()
            await interaction.response.send_message("Joined your voice channel!")
        except Exception as e:
            await interaction.response.send_message(f"Failed to join voice channel: {str(e)}")
    else:
        await interaction.response.send_message("You need to be in a voice channel first.")


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


@bot.tree.command(name="leave",
                  description="Remove the bot from your voice channel")
async def leave(interaction: discord.Interaction):
    """Leaves your voice channel"""
    if interaction.guild and interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect(force=True)
        await interaction.response.send_message("Left the voice channel.")
    else:
        await interaction.response.send_message("Not currently in a voice channel.")


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
@bot.tree.command(name="guess", description="guess a letter in hangman")
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

@bot.tree.command(name="geoguessr", description="Play geoguessr with an image randomly selected from the internet")
async def geoguessr(interaction: discord.Interaction):
    await interaction.response.send_message("Not implemented yet I was too busy eating cheetos")

@bot.tree.command(name="meme", description="Get a random meme from reddit, May or may not be cringe or nsfw")
async def meme(interaction: discord.Interaction):
    url = "https://meme-api.com/gimme"
    response = requests.get(url)
    data = response.json()
    await interaction.response.send_message(data["url"])
    await interaction.followup.send(data["title"])
    await interaction.followup.send(data["postLink"])
    await interaction.followup.send(data["author"])

@bot.tree.command(name="bible", description="Get a random verse from the Bible.")
async def bible(interaction: discord.Interaction):
    url = "https://labs.bible.org/api/?passage=random&type=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        verse = data[0] 
        message = f"**{verse['bookname']} {verse['chapter']}:{verse['verse']}**\n"
        message += f"{verse['text']}\n"
        message += f"(*{verse.get('translation_name', 'Translation Unknown')}*)"

        await interaction.response.send_message(message)
    else:
        await interaction.response.send_message("Failed to fetch verse. Please try again later.")

@bot.tree.command(name="flag", description="Get a random flag from the world")
async def flag(interaction: discord.Interaction):
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    data = response.json()
    country = random.choice(data)
    await interaction.response.send_message(country["flags"]["png"])
    await interaction.followup.send(country["name"]["common"])
    await interaction.followup.send(country["capital"][0])


@bot.tree.command(name="playaudio", description="takes a youtube url and plays the audio in the voice channel")
async def playaudio(ctx, url: str):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        if info is None:
            await ctx.send("Failed to retrieve audio URL.")
            return
        audio_url = info['url']

    ctx.voice_client.stop()
    source = await discord.FFmpegOpusAudio.from_probe(audio_url)
    ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send(f"Now playing: {info['title']}")
    
@bot.tree.command(name="clear", description="deletes the last n messages in the channel sent by the goon")
async def clear(interaction: discord.Interaction, amount: int):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command can only be used in a text channel.")
        return
    
    await interaction.response.defer()
    deleted = await interaction.channel.purge(limit=amount, check=lambda m: m.author == bot.user)
    await interaction.followup.send(f"Deleted {len(deleted)} messages.")
# === Start Bot ===
if __name__ == "__main__":
    try:
        token = os.getenv("TOKEN") or ""
        if not token:
            raise ValueError("Missing TOKEN environment variable.")
        bot.run(token)
    except Exception as e:
        print("Bot failed to start:", e)
