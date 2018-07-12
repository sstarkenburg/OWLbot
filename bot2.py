#!/env/bin/python3
import os
import asyncio
import configparser

import discord
from discord.ext import commands

import owlapi


## Some setup stuff
# sets working directory to bot's folder
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# read config for token
config = configparser.ConfigParser()
config.read("config.ini")

# create the discord client
bot = commands.Bot(command_prefix='<@{0}> '.format(config['Main']['bot_id']))


## The meat of the bot

@bot.command()
async def about():
    """ 
    Description of the bot.

    Deletes itself after 20 seconds to try and keep the channel clean.
    """
    await bot.say('A Discord bot meant to provide information on the Overwatch\
                   League to a Discord server.\n\nCurrently a work in progress.\
                   \n\n(Message will self-destruct in 20 seconds)',
                  delete_after=20)

@bot.command()
async def upcoming():
    """
    Get upcoming OWL matches.
    """
    await bot.type()
    embed = owlapi.getUpcomingMatches()
    await bot.say(embed=embed)

@bot.command()
async def live():
    """
    Get the live OWL match.
    """
    await bot.type()
    embed = owlapi.getLiveMatch()
    await bot.say(embed=embed)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

print('Bot directory: ', dir_path)

bot.run(config['Main']['bot_token'])
