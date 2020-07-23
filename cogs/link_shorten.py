import discord
from discord.ext import tasks,commands
import requests #for PUT Requests to short.st link shortener
import json
def setup(bot):
    API_KEY='api-key-shorte.st' #api key from shorte.st
    bot.add_cog(link_maker(bot,API_KEY)) #add cog to bot


class link_maker(commands.Cog):
    def __init__(self,bot,apikey): #init cog values
        self.bot=bot
        self.apikey=apikey

    def cog_unload(self):
        print('unloaded link')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')
    
    def json_upd(self,lnk,g_id): #add created link to list of links in json

        with open('links.json','r') as f:
            link_json=json.load(f)
            
        if str(g_id) not in link_json.keys():
            link_json[f'{g_id}']=[]
            
        if lnk not in link_json[f'{g_id}']:
            link_json[f'{g_id}'].append(lnk)

        with open('links.json','w') as f:
            json.dump(link_json,f,indent=4)
        

    @commands.command()
    async def short(self,ctx,long_link):
        '''
        short.st api uses curl for api usage

        curl -H "public-api-token: key" -X PUT -d 
        "urlToShorten=url" https://api.shorte.st/v1/data/url
        
        Alternatively PUT Requests can be used
        
        '''
        response = requests.put("https://api.shorte.st/v1/data/url",{"urlToShorten":long_link}, headers={"public-api-token": self.apikey})
        '''
        Response Content Format
        {"status":"ok","shortenedUrl":"http:\/\/sh.st\/XXXX"}
        '''
        if response.status_code==200: #success
            short_link=response.json() #convert response to json
            
            #using embed for bot message
            embed_ln=discord.Embed(
                title=short_link['shortenedUrl'],
                color=discord.Color.dark_red(),
                url=short_link['shortenedUrl']
            )

            embed_ln.set_author(name=ctx.message.author)
            await ctx.message.delete() #delete original message from user
            await ctx.send(embed=embed_ln)
            self.json_upd(short_link['shortenedUrl'],ctx.message.guild.id)

        else:
            await ctx.send('Invalid Link') 
    
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def get_guild_links(self,ctx):
        '''
        Get Links Created In Guild
        '''
        with open('links.json','r') as f:
            link_json=json.load(f)
        
        guild_links=link_json[f'{ctx.message.guild.id}']

        embed_ln=discord.Embed(
                title=ctx.message.guild.name,
                color=discord.Color.dark_teal()
            )
        
        embed_ln.set_footer(text=f'Number Of Links : {len(guild_links)}')
        i=0
        for lnk in guild_links:
            embed_ln.add_field(name=f'{lnk}',value=f'{i}',inline=False)
            i+=1
        await ctx.send(embed=embed_ln)