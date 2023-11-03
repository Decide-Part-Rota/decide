import os
import random
import discord
import requests
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
from typing import Union


### --- REST api Initialization --- ###

base_url = "http://127.0.0.1:8000/"

### --- Bot Initialization --- ###

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEV_MODE = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

### --- Functions --- ###

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise ValueError(f'Unhandled event: {event}')

@bot.event
async def on_command_error(ctx, error):
    message = ""

    if DEV_MODE:
        message += f'\n{error}'

    print(error)
    await ctx.send(message)

### --- Commands --- ###

@bot.event
async def on_member_join(member):
    await member.create_dm()
    # Important how to dm users
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name='commands', help='List all commands')
async def list_commands(ctx):
    embed = discord.Embed(title='List of all commands', color=discord.Color.random())

    # !list-votings
    value = 'Lists all votings following the format [VOTING_ID]: [VOTING_NAME].\nOnly shows public votings {NOT IMPLEMENTED YET}.'
    embed.add_field(name='!list-votings', value=value, inline=False)

    # !get-voting voting_id
    value = 'Gets a voting by its ID. Shows the voting name, options and the number for each option.'
    value += '\n\nThe ID can be found by using the !list-votings command.'
    value += '\nTo vote, select one of the provided reactions, corresponding to the desired option.'
    value += '\n WARNING: Only the first vote with be taken and you only have 60 seconds to vote.'
    value += '\n\nExample: !get-voting 1'
    embed.add_field(name='!get-voting [VOTING_ID]', value=value, inline=False)

    print(f"{ctx.author} requested the list of commands")
    await ctx.channel.send(embed=embed)

@bot.command(name='list-votings', help='Lists all votings')
async def list_votings(ctx):
    response = requests.get(base_url + "voting/")
    votings = response.json()

    embed = discord.Embed(title='Votings', color=discord.Color.random())

    for voting in votings:
        if voting["start_date"] is not None and voting["end_date"] is None and voting["public"]:
            embed.add_field(name=f'{voting["id"]}: {voting["name"]}', value=voting["question"]["desc"], inline=False)

    print(f"{ctx.author} requested the list of votings")
    await ctx.send(embed=embed)

# POST VOTE
def gen_data(voting, user_id, option_id):
    # Public key
    bigpk = {
        'p' : int(voting['pub_key']['p']),
        'g' : int(voting['pub_key']['g']),
        'y' : int(voting['pub_key']['y']),
    }

    # ElGamal bits
    bits = 256

    # Random number generation
    q = 2^bits - 1
    r = random.SystemRandom().randrange(1, q)

    # ElGamal encryption
    alpha = bigpk['g']^r % bigpk['p']
    beta = bigpk['y']^r * option_id % bigpk['p']

    data = {
        "voting": voting["id"],
        "voter": user_id,
        "a": alpha,
        "b": beta,
    }

    return data

async def post_voting(ctx, reaction, voting, option_id):
    people = requests.get(base_url + "authentication/persons/").json()
    user_id = 0
    user_found = False

    for person in people:
        if person["discord_account"] == str(ctx.author):
            user_found = True
            user_id = person["user"]["id"]

    if user_found:
        # ElGamal encryption
        #data = gen_data(voting, user_id, option_id)
        data = gen_data(voting, user_id, option_id)

        vote_response = requests.post(base_url + "store/bot/", data=data)

        if vote_response.status_code == 200:
            print(f"Vote for voting {voting['id']} created by {user_id} with option {option_id}")
            return await ctx.send(f"{ctx.author} answered option {str(reaction[0].emoji)}")
        else:
            return await ctx.send("There was an internal error. Please try again later.")

    else:
        title = 'This user account is not assigned to any existing Decide user.'
        description = "Please create an account or link your Discord account to an existing Decide user using these links:"

        embed = discord.Embed(title=title,description=description, color=discord.Color.random())

        embed.add_field(name="Signup", value="http://localhost:8000/authentication/accounts/login/?next=/", inline=False)
        embed.add_field(name="Profile", value="http://localhost:8000/profile/", inline=False)

        return await ctx.send(embed=embed)

async def post_voting_message(ctx, voting):
    # Creating question message
    embed = discord.Embed(title=f'{voting["name"]}', color=discord.Color.random())
    option_numbers = []
    
    def check(r: discord.Reaction, u: Union[discord.Member, discord.User]):
        return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and r.message.id == msg.id and \
               emotes.index(str(r.emoji)) - 1 in range(len(option_numbers))

    # Adding options
    counter = 1
    for option in voting["question"]["options"]:
        if counter < 11:
            embed.add_field(name=emotes[counter],
                            value=f'{option["option"]}',
                            inline=True)
            option_numbers.append(option["number"])
            counter += 1
        else:
            await ctx.send("Invalid option number")
            return
    # Sending message
    msg = await ctx.send(embed=embed)

    # Adding reactions
    for i in range(1,counter):
        await msg.add_reaction(emotes[i])

    # Waiting for reaction
    try:
        reaction = await bot.wait_for('reaction_add', check = check, timeout = 60.0)
    except asyncio.TimeoutError:
        # at this point, the check didn't become True.
        await ctx.send(f"**{ctx.author}**, you didnt react correctly with within 60 seconds.")
        return
    else:
        # at this point, the check has become True and the wait_for has done its work, now we can do ours.
        # here we are sending some text based on the reaction we detected.
        await post_voting(ctx, reaction, voting, option_numbers[emotes.index(reaction[0].emoji) - 1])
        return

# Reaction lookup table
emotes = ["0️⃣","1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

@bot.command(name='get-voting', help='Gets a voting from ID')
async def get_voting(ctx, voting_id: int):
    response = requests.get(base_url + "voting/")
    votings = response.json()

    # Extract the voting, send the message and add reactions
    for voting in votings:
        if voting["id"] == voting_id and voting["start_date"] is not None and voting["end_date"] is None and voting["public"]:
            print(f"{ctx.author} requested voting {voting_id}")
            return await post_voting_message(ctx, voting)
    return await ctx.send("Invalid voting ID or voting is not active")

bot.run(TOKEN)