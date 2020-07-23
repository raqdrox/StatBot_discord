import discord
from discord.ext import commands, tasks
import json
import random
import time
import os
import logging

#settig up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#setting up bot
bot_token='TOKEN'
bot = commands.Bot(command_prefix = 'sb!')
bot.remove_command('help')


'''-----------Bot Functions------------'''
@bot.event
async def on_ready():
    print('Logging in...')
    print('Ready')
    cog_loader() #load cogs at start
    

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def stat_init(ctx,rolename='bot'): 
    '''
    This Function Sets Up Channels And Ids For Server_stats.py cog module
    Provide Bot role name if Custom
    '''
    bot.unload_extension(f'cogs.server_stats') #unload the cog before changes
    
    guild=ctx.message.guild
    
    with open('stats.json','r') as f:
        stat_json=json.load(f)
    
    if str(guild.id) not in stat_json["guilds_stats"].keys(): #check to avoid repetition if oommand used twice
        print(guild)
        #find BOT role
        for role in guild.roles:
            if role.name.lower()=='bots' or role.name.lower() ==rolename.lower():
                break
        
        #create channels
        stats1=await guild.create_voice_channel('stat1')
        stats2=await guild.create_voice_channel('stat2')
        stats3=await guild.create_voice_channel('stat3')
        await ctx.send("Channels Created")
        
        #adjust channel permissions
        
        overwrite_perm=discord.PermissionOverwrite()
        overwrite_perm.connect=False
        overwrite_perm.view_channel=True

        await stats1.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)
        await stats2.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)
        await stats3.set_permissions(ctx.guild.default_role,overwrite=overwrite_perm)

        #collect and format Guild and Channel IDs
        guild_stats={}
        guild_stats["bot_role"]=role.id
        guild_stats["mem_tot_id"]=stats1.id
        guild_stats["mem_onl_id"]=stats2.id
        guild_stats["bot_id"]=stats3.id
        guild_stats["mem_tot_count"]=69
        guild_stats["mem_onl_count"]=42
        guild_stats["bot_count"]=0

        stat_json["guilds_stats"][f'{guild.id}']=guild_stats
        
        #Dump IDs to JSON
        with open('stats.json','w') as f:
            json.dump(stat_json,f,indent=4)
        print('Data Updated')
        
        bot.load_extension('cogs.server_stats')    #reload server_stats Cog
    
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def stat_remove(ctx):
    '''
    This Function Deletes Stuff Initialized By stat_init Function
    '''
    
    bot.unload_extension(f'cogs.server_stats') #unload the cog before changes
    guild=ctx.message.guild
    
    with open('stats.json','r') as f: #get IDs
        stat_json=json.load(f)
    
    #get Channel Objects
    if str(guild.id) in stat_json["guilds_stats"].keys():
        mem_tot_channel=bot.get_channel(stat_json["guilds_stats"][f'{guild.id}']["mem_tot_id"])
        print(mem_tot_channel)
        mem_onl_channel=bot.get_channel(stat_json["guilds_stats"][f'{guild.id}']["mem_onl_id"])
        print(mem_onl_channel)
        bot_channel=bot.get_channel(stat_json["guilds_stats"][f'{guild.id}']["bot_id"])
        print(bot_channel)
        
        del stat_json["guilds_stats"][f'{guild.id}'] #delete Guild entries form JSON data
        with open('stats.json','w') as f:
            json.dump(stat_json,f,indent=4)
            
        #delete channels
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
        
        bot.load_extension('cogs.server_stats')#reload server_stats Cog

@bot.command()
@commands.is_owner()
async def load(ctx,extension):
    '''
    function for loading cogs
    provide cog name as argument
    '''
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} loaded')

@bot.command()
async def invite(ctx):
    '''
    Bot Invite Link
    '''
    inv_link="INV LINK"
    embed_inv=discord.Embed(
        title='Click To Invite',
        color=discord.Color.blue(),
        url=inv_link
        )
    embed_inv.set_author(name='Invite StatBot To Your Server')
    await ctx.send(embed=embed_inv)

@bot.command(aliases=['latency','speed'])
async def ping(ctx):
    '''
    Ping Bot
    '''
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
    '''
    function for unloading cogs
    provide cog name as argument
    '''
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} unloaded')

@bot.command()
@commands.is_owner()
async def reload(ctx,extension):
    '''
    function for unloading then loading cogs
    usefull for refresh
    provide cog name as argument
    '''
    bot.unload_extension(f'cogs.{extension}')
    print('reloading...')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension {extension} Reloaded')

def cog_loader():
    '''
    Load All Cogs To Bot
    Used At Bot Start
    '''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(aliases=['8ball'])
async def _8ball(ctx,*,question):
    '''
    Fun 8ball Command
    provide statement as argument
    '''
    responses=['It is certain.','It is decidedly so.','Without a doubt.','Yes – definitely.','You may rely on it.','As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer:{random.choice(responses)}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount):
    '''
    purge messages from chat
    provide number of messages as argument
    '''
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Deleted {amount} Messages')
    time.sleep(2)
    await ctx.channel.purge(limit=1) #remove bot message

#basic mod commands
@bot.command()
@commands.is_owner()
async def kick(ctx , member : discord.Member, * , reason=None):
    await member.kick(reason=reason)

@bot.command()
@commands.is_owner()
async def ban(ctx , member : discord.Member, * , reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned : {member.mention}')

@bot.command()
@commands.is_owner()
async def unban(ctx,*,member):
    '''
    Provide member discord tag as argument
    '''
    banned_users= await ctx.guild.bans()
    member_name,member_discriminator=member.split('#')

    for ban_entry in banned_users:
        user =ban_entry.user
        if(user.name,user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')

'''--------------------------------------'''

bot.run(bot_token)#run the bot