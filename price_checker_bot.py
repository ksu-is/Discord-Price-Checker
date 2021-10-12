#price checker bot
import os
import time
import discord
from discord import guild
from discord.ext.commands.core import command
from dotenv import load_dotenv
from discord.ext import commands
from webscrape import *
from bs4 import BeautifulSoup


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


@bot.command(name="price", help="Pulls the price of the game title from several sites, to call send \"\\price\" and the title of the game.")
async def on_message(ctx,*,message):
    #await ctx.send("Where do you want to search (Steam, Ebay, or Epic)")
    await ctx.send("Searching steam for "+message)
    steam_package= steam_grab(message)
    if type(steam_package)==str:
        await ctx.send(steam_package+"on Steam")
    else:
        steam_titles=steam_package[0]
        steam_summary=steam_package[1]
        steam_url=steam_package[2]

        await ctx.send("Top result from steam "+message+" is "+steam_titles[0].title())
        await ctx.send(steam_summary)
        await ctx.send(steam_url)
        
    
    play_package=play_grab(message)
    await ctx.send("Searching playstation store for "+message)
    await ctx.send("Top results:")
    await ctx.send(play_package[0])
    await ctx.send(play_package[1])
    await ctx.send(play_package[2])    
    ebay_package=ebay_grab(message)
    await ctx.send("Searching ebay for "+message)
    ebay_titles=ebay_package[0]
    ebay_urls=ebay_package[1]
    await ctx.send("Top three results from ebay for "+message+":")
    await ctx.send(ebay_titles[0]+"\n"+ebay_titles[1]+"\n"+ebay_titles[2])
    epic_package=epic_grab(message)
    await ctx.send("Searching Epic Game Store for "+message)
    if type(epic_package) != str:
        print(epic_package)
        
        await ctx.send("Top 3 results for Epic Game Store for "+message+':')
        for games in epic_package:
            await ctx.send(games)
    else:
        print(epic_package)
        await ctx.send(epic_package)
    play_package=play_grab(message)
    await ctx.send("Searching playstation store for "+message)
    await ctx.send("Top results:")
    for game in range(0,3):
        await ctx.send(play_package[game])
@bot.command(name="store", help="enter name of \"store\" and the \"title\" in separate quotations.")
async def on_message(ctx,store : str,title : str):
    if store.lower()=="steam":
        await ctx.send("Searching steam for "+title)
        steam_package= steam_grab(title)
        if type(steam_package)==str:
            await ctx.send(steam_package+"on Steam")
        else:
            steam_titles=steam_package[0]
            steam_summary=steam_package[1]
            steam_url=steam_package[2]

            await ctx.send("Top result from steam "+title+" is "+steam_titles[0].title())
            await ctx.send(steam_summary)
            await ctx.send(steam_url)

    elif store.lower()=="play" or "playstation"or"play station":
        play_package=play_grab(title)
        await ctx.send("Searching playstation store for "+title)
        await ctx.send("Top results:")
        await ctx.send(play_package[0])
        await ctx.send(play_package[1])
        await ctx.send(play_package[2])


    elif store.lower()=="ebay":
        ebay_package=ebay_grab(title)
        await ctx.send("Searching ebay for "+title)
        ebay_titles=ebay_package[0]
        ebay_urls=ebay_package[1]
        await ctx.send("Top three results from ebay for "+title+":")
        await ctx.send(ebay_titles[0]+"\n"+ebay_titles[1]+"\n"+ebay_titles[2])
    elif store.lower()=="epic":
        epic_package=epic_grab(title)
        await ctx.send("Searching Epic Game Store for "+title)
        if type(epic_package) != str:
            print(epic_package)
            
            await ctx.send("Top 3 results for Epic Game Store for "+title+':')
            for games in epic_package:
                await ctx.send(games)
        else:
            print(epic_package)
            await ctx.send(epic_package)
    else:
        await ctx.send("Only three stores currently: Steam, eBay, Epic")
    

bot.run(TOKEN)


