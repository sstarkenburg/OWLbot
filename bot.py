#!/env/bin/python3
import os
import asyncio
import configparser

import discord
from discord.ext import commands

import owlapi


# sets working directory to bot's folder
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# read config for token
config = configparser.ConfigParser()
config.read("config.ini")


## Some setup stuff

# create the discord client
bot = discord.Client()


## The meat of the bot

# different discord events

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '<@{0}> help'.format(config['Main']['bot_id']):
        await bot.send_message(message.channel, 'tell sam~ to fix this')
    elif message.content == '<@{0}> upcoming'.format(config['Main']['bot_id']):
        await bot.send_typing(message.channel)
        embed = owlapi.getUpcomingMatches()
        await bot.send_message(message.channel, embed=embed)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

print('Bot directory: ', dir_path)
bot.run(config['Main']['bot_token'])
