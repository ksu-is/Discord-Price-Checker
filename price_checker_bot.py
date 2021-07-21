#price checke bot.py
import os
import discord
from discord import guild
from dotenv import load_dotenv


load_dotenv()
#The token is a special code that connects the bot to the correct server with the guild being the name of the server and is used
#to verify that it connected to the correct server.
#The token and guild name are stored in a seperate .env file that the user can change for their specific guild and enhances security
#by not being hard coded in
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')

client=discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            #print("the guilds are the same")
            #Was used to check that the guild/server it connected was the one in the .env file
            break

    print(
        f'{client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #Loops through the member list and prints the members to the console
    members='\n'.join([member.name for member in guild.members])
    print(f'Guild Members:\n {members}')
client.run(TOKEN)