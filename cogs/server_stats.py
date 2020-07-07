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

    def cog_unload(self):
        print('unloaded Stats')
        self.change_stats.stop()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')

    @commands.Cog.listener()
    async def on_member_join(self):
        self.change_stats()

    @commands.Cog.listener()
    async def on_member_remove(self):
        self.change_stats()


    @tasks.loop(seconds=10)
    async def change_stats(self):
        online=0
        for member in self.guild.members:
            if (str(member.status)=='online' or str(member.status)=='idle') and member not in self.roles.members:
                online+=1

        print('Got Members')

        if self.mem_tot_count!=((self.guild.member_count)-(len(self.roles.members))):
            self.mem_tot_count=(self.guild.member_count)-(len(self.roles.members))
            await self.mem_tot_channel.edit(name=f'Total Members: {self.mem_tot_count}')
            print('Edited Total')

        
        if self.mem_onl_count!=online:
            self.mem_onl_count=online
            await self.mem_onl_channel.edit(name=f'Members Online: {self.mem_onl_count}')
            print('Edited Online')

        
        if self.bot_count!=len(self.roles.members):
            self.bot_count=len(self.roles.members)
            await self.bot_channel.edit(name=f'Total Bots: {self.bot_count}')
            print('Edited Bots')

        print('DONE')
        
    @change_stats.before_loop
    async def before_stats(self):
        print('Starting...')
        await self.bot.wait_until_ready()

        self.guild=self.bot.get_guild(id=690205011497582702)
        self.roles=self.guild.get_role(role_id=690269298685771797)
        
        with open("stats.json",'r') as f:
            ch_id=json.load(f)
        print(f'IDs LOADED :{ch_id}')

        self.mem_tot_channel=self.bot.get_channel(int(ch_id["mem_tot_id"]))
        self.mem_onl_channel=self.bot.get_channel(int(ch_id["mem_onl_id"]))
        self.bot_channel=self.bot.get_channel(int(ch_id["bot_id"]))

        self.mem_tot_count=0
        self.mem_onl_count=0
        self.bot_count=0
        print('Bot is Online')