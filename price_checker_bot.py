#price checker bot
import os
import time
import discord
from discord import guild
from dotenv import load_dotenv
from discord.ext import commands
import sys
from webscrape import steam_grab
from bs4 import BeautifulSoup
import requests

load_dotenv()
#The token is a special code that connects the bot to the correct server with the guild being the name of the server and is used
#to verify that it connected to the correct server.
#The token and guild name are stored in a seperate .env file that the user can change for their specific guild and enhances security
#by not being hard coded in
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')
#this is the command character that tells the bot the message is a command it must start with this character to be seen as one
bot = commands.Bot(command_prefix="\\")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            #print("the guilds are the same")
            #Was used to check that the guild/server it connected was the one in the .env file
            break

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #Loops through the member list and prints the members to the console
    members='\n'.join([member.name for member in guild.members])
    print(f'Guild Members:\n {members}')


@bot.command(name="price", help="Will pull the price of the game title from several sites, to call send \"\\price\" and the title of the game.")
async def on_message(ctx,*,message):
    await ctx.send("Searching steam for "+message)
    package= steam_grab(message)
    titles=package[0]
    summary=package[1]
    url=package[2]

    await ctx.send("Top result from steam "+message+" is "+titles[0].title())
    await ctx.send(summary)
    await ctx.send(url)
    

   

bot.run(TOKEN)