import discord
from discord.ext import tasks,commands
from discord.utils import get
import json
def setup(bot):
        bot.add_cog(Stats_Cog(bot))

class Stats_Cog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.change_stats.start()
        self.ch_id={}

    def cog_unload(self):
        print('unloaded Stats')
        self.change_stats.stop()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')

    async def refresh_stats(self,g_id):
        guild=self.bot.get_guild(id=int(g_id))
        print(guild)
        roles=guild.get_role(role_id=self.ch_id["guilds"][f'{g_id}']["bot_role"])
        mem_tot_channel=self.bot.get_channel(self.ch_id["guilds"][f'{g_id}']["mem_tot_id"])
        mem_onl_channel=self.bot.get_channel(self.ch_id["guilds"][f'{g_id}']["mem_onl_id"])
        bot_channel=self.bot.get_channel(self.ch_id["guilds"][f'{g_id}']["bot_id"])

        online=0
        for member in guild.members:
            if (str(member.status)=='online' or str(member.status)=='idle') and member not in roles.members:
                online+=1

        print('Got Members')

        if self.ch_id["guilds"][f'{g_id}']["mem_tot_count"]!=((guild.member_count)-(len(roles.members))):
            mem_tot_count=(guild.member_count)-(len(roles.members))
            self.ch_id["guilds"][f'{g_id}']["mem_tot_count"]=mem_tot_count
            await mem_tot_channel.edit(name=f'Total Members: {mem_tot_count}')
            print('Edited Total')

        if self.ch_id["guilds"][f'{g_id}']["mem_onl_count"]!=online:
            mem_onl_count=online
            self.ch_id["guilds"][f'{g_id}']["mem_onl_count"]=mem_onl_count
            await mem_onl_channel.edit(name=f'Members Online: {mem_onl_count}')
            print('Edited Online')

        if  self.ch_id["guilds"][f'{g_id}']["bot_count"]!=len(roles.members):
            bot_count=len(roles.members)
            self.ch_id["guilds"][f'{g_id}']["bot_count"]=bot_count
            await bot_channel.edit(name=f'Total Bots: {bot_count}')
            print('Edited Bots')

        print('DONE')

    @tasks.loop(seconds=10)
    async def change_stats(self):
        print('Bot is Online')
        with open("stats.json",'r') as f:
            self.ch_id=json.load(f)
        print(f'IDs LOADED :{self.ch_id}')     
        for guild_ids in self.ch_id["guilds"].keys():
            print(guild_ids)
            await self.refresh_stats(guild_ids)

        with open("stats.json",'w') as f:
            json.dump(self.ch_id,f,indent=4)
            
    @change_stats.before_loop
    async def before_stats(self):
        print('Starting...')
        await self.bot.wait_until_ready()
        
