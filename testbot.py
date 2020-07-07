import discord
from discord.ext import commands, tasks
import json
import random
import time
import os
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot_token=''
bot = commands.Bot(command_prefix = 'd:')
@bot.event
async def on_ready():
    print('Logging in...')
    print('Ready')
    cog_loader()
    await bot.change_presence(activity=discord.Game("Kalm"))

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def stat_init(ctx):
    bot.unload_extension(f'cogs.server_stats')
    guild=ctx.message.guild
    with open('stats.json','r') as f:
        stat_json=json.load(f)
    if str(guild.id) not in stat_json["guilds"].keys():
        print(guild)
        for role in guild.roles:
            if role.name.lower()=='bots' or role.name.lower()=='bot':
                break
        stats1=await guild.create_voice_channel('stat1')
        stats2=await guild.create_voice_channel('stat2')
        stats3=await guild.create_voice_channel('stat3')
        await ctx.send("Channels Created")
        overwrite_perm=discord.PermissionOverwrite()
        overwrite_perm.connect=False
        overwrite_perm.view_channel=True
        await stats1.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)
        await stats2.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)
        await stats3.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)
        guild_stats={}
        guild_stats["bot_role"]=role.id
        guild_stats["mem_tot_id"]=stats1.id
        guild_stats["mem_onl_id"]=stats2.id
        guild_stats["bot_id"]=stats3.id
        guild_stats["mem_tot_count"]=69
        guild_stats["mem_onl_count"]=42
        guild_stats["bot_count"]=0

        stat_json["guilds"][f'{guild.id}']=guild_stats

        with open('stats.json','w') as f:
            json.dump(stat_json,f,indent=4)
        print('Data Updated')
        bot.load_extension('cogs.server_stats')    
    
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def stat_remove(ctx):
    bot.unload_extension(f'cogs.server_stats')
    guild=ctx.message.guild
    with open('stats.json','r') as f:
        stat_json=json.load(f)
    if str(guild.id) in stat_json["guilds"].keys():
        mem_tot_channel=bot.get_channel(stat_json["guilds"][f'{guild.id}']["mem_tot_id"])
        print(mem_tot_channel)
        mem_onl_channel=bot.get_channel(stat_json["guilds"][f'{guild.id}']["mem_onl_id"])
        print(mem_onl_channel)
        bot_channel=bot.get_channel(stat_json["guilds"][f'{guild.id}']["bot_id"])
        print(bot_channel)

        del stat_json["guilds"][f'{guild.id}']
        with open('stats.json','w') as f:
            json.dump(stat_json,f,indent=4)

        try:
            await mem_onl_channel.delete()
            print('onl')
        except:
            pass
        try:
            await mem_tot_channel.delete()
            print('tot')
        except:
            pass
        try:
            await bot_channel.delete()
            print('bot')
        except:
            pass
        print('Deleted')
        await ctx.send("Channels Deleted")
        bot.load_extension('cogs.server_stats')

@bot.command()
@commands.is_owner()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} loaded')

@bot.command()
async def invite(ctx):
    inv_link="Invite Stonks To Your Server \n https://discord.com/api/oauth2/authorize?client_id=728878804491304980&permissions=8&scope=bot"
    await ctx.send(inv_link)

@bot.command(aliases=['latency','speed'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} unloaded')

@bot.command()
@commands.is_owner()
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
