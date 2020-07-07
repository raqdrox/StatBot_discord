import discord
from discord.ext import commands, tasks
import random
import time
import os
bot_token=''
bot = commands.Bot(command_prefix = 'd:')
@bot.event
async def on_ready():
    print('Logging in...')
    cog_loader()
    print('Ready')
    await bot.change_presence(activity=discord.Game("Under Construction"))

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} loaded')

@bot.command(aliases=['latency','speed'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} unloaded')

@bot.command()
async def reload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    print('reloading...')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} Reloaded')

def cog_loader():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(bot_token)