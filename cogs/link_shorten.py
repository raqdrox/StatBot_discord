import discord
from discord.ext import tasks,commands
import requests #for PUT Requests to short.st link shortener

def setup(bot):
    API_KEY='api-key-short.st' #api key from short.st
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
            embed_inv=discord.Embed(
                title=short_link['shortenedUrl'],
                color=discord.Color.dark_red(),
                url=short_link['shortenedUrl']
            )

            embed_inv.set_author(name=ctx.message.author)
            await ctx.message.delete() #delete original message from user
            await ctx.send(embed=embed_inv)
        else:
            await ctx.send('Invalid Link')