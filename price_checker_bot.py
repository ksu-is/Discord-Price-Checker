#price checker bot
import os
import time
import discord
from discord import guild
from dotenv import load_dotenv
from discord.ext import commands
import sys
from webscrape import *
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
    steam_package= steam_grab(message)
    steam_titles=steam_package[0]
    steam_summary=steam_package[1]
    steam_url=steam_package[2]

    await ctx.send("Top result from steam "+message+" is "+steam_titles[0].title())
    await ctx.send(steam_summary)
    await ctx.send(steam_url)
    ebay_package=ebay_grab(message)
    await ctx.send("Searching ebay for "+message)
    ebay_titles=ebay_package[0]
    ebay_urls=ebay_package[1]
    await ctx.send("Top three results from ebay for "+message+":")
    await ctx.send(ebay_titles[0]+"\n"+ebay_titles[1]+"\n"+ebay_titles[2])


    

   

bot.run(TOKEN)