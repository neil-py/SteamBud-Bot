import discord
from dotenv import dotenv_values
from discord.ext import commands
from SteamBud import SearchAPI

config = dotenv_values(".env")
TOKEN = config['TOKEN']

backendAPI = SearchAPI()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with myself"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            embed=discord.Embed(
                title="⭕ Invalid Command ⭕", color=0xFF0000,
                description="Please Try again or Enter '!sbcmds' for more commands!"
            )
        )

@bot.command()
async def findDeals(ctx, game_id, amountSearch=None):
    await ctx.send(embed=discord.Embed(title=f"🔎 Searching.... 🔎", color= 10026752))
    amount_search = amountSearch if amountSearch is not None else 0
    try:
        game_list = backendAPI.finddeals(game_id=game_id, amount=int(amount_search))
        await ctx.channel.purge(limit=1)
        if game_list == []:
            await ctx.send(embed=discord.Embed(title="❌ No Deals Found! ❌", color= 16711680))
        else:
            await ctx.send(embed=discord.Embed(title=f"🏷️ {len(game_list['other_deals']) +1} Deals Found! 🏷️", color= 10026752))
        
        embed=discord.Embed(title=f"[CHEAPEST] {game_list['game_title']}", color= 7461119, url=game_list['deal_link'])
        embed.set_thumbnail(url=game_list['cheapest_store_banner'])
        embed.set_image(url=game_list['thumbnail'])
        embed.add_field(name="Cheapest Price", value=f"${game_list['cheapest_price']}", inline=False)
        embed.add_field(name="Store", value=game_list['cheapest_store'], inline=False)
        embed.add_field(name=f"Saved: {game_list['savings']}%", value="", inline=False)
        embed.set_footer(text=f"Searched By: {ctx.author.display_name}")
        await ctx.send(embed=embed)

        for game in game_list['other_deals']:
            embed=discord.Embed(title=game['store'], color= 7461119, url=game['deal_link'])
            embed.set_thumbnail(url=game['store_thumb'])
            embed.add_field(name="Price", value=f"${game['price']}", inline=False)
            embed.add_field(name=f"Saved: {game['savings']}%", value="", inline=False)
            await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Search Complete ✅", color= 10026752, 
                description="")
                )
    except Exception as e :
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(
                title=f"🚧 An Error Occured [{str(e)}] 🚧", color= 16711680, 
                description="Please Try again or Enter '!sbcmds' for more commands!")
                )

@bot.command()
async def searchgame(ctx, game_name:str, amountSearch=None):
    await ctx.send(embed=discord.Embed(title=f"🔎 Searching.... 🔎", color= 10026752))
    game_name= game_name.lower()
    amount_search = amountSearch if amountSearch is not None else 0
    try:
        game_list = backendAPI.generalSearch(game_name=game_name, amount=int(amount_search))
        await ctx.channel.purge(limit=1)
        if game_list == []:
            await ctx.send(embed=discord.Embed(title="❌ No Deals Found! ❌", color= 16711680))
        else:
            await ctx.send(embed=discord.Embed(title=f"🎮 {len(game_list)} Games Found! 🎮", color= 10026752))
        for game in game_list:
            embed=discord.Embed(title=f"Game ID: {game['gameID']} - {game['game_title']}", color= 7461119, url=game['deal_link'] )
            embed.set_image(url=game['thumbnail'])
            embed.add_field(name="Cheapest Price", value=f"${game['cheapset_price']}", inline=False)
            embed.add_field(name="Store", value=game['cheapest_store'], inline=False)
            embed.set_footer(text=f"Searched By: {ctx.author.display_name}")
            await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Search Complete ✅", color= 10026752, 
                description="")
                )
    except Exception as e :
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(
                title="🚧 An Error Occured 🚧", color= 16711680, 
                description="Please Try again or Enter '!sbcmds' for more commands!")
                )

@bot.command()
async def steamID(ctx, steamappid):
    await ctx.send(embed=discord.Embed(title=f"🔎 Searching.... 🔎", color= 10026752))
    try:
        game_list = backendAPI.steamID(steamappid)
        await ctx.channel.purge(limit=1)
        if  game_list == []:
            await ctx.send(embed=discord.Embed(title="❌ No Deals Found! ❌", color= 16711680))
        else:
            await ctx.send(embed=discord.Embed(title=f"🏷️ {len(game_list)} Deals Found! 🏷️", color= 10026752))
        for game in game_list:
            embed=discord.Embed(title=game['game_title'], color= 7461119, url=game['deal_link']  )
            embed.set_image(url=game['thumbnail'])
            embed.add_field(name="Cheapest Price", value=f"${game['cheapset_price']}", inline=False)
            embed.add_field(name="Store", value=game['cheapest_store'], inline=False)
            embed.set_footer(text=f"Searched By: {ctx.author.display_name}")
            await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Search Complete ✅", color= 10026752, 
                description="")
                )
    except Exception as e :
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(
                title="🚧 An Error Occured 🚧", color= 16711680, 
                description="Please Try again or Enter '!sbcmds' for more commands!")
                )

@bot.command()
async def steamLINK(ctx, steamLink):
    await ctx.send(embed=discord.Embed(title=f"🔎 Searching.... 🔎", color= 10026752))
    try:
        game_list = backendAPI.steamlink(steamLink)
        await ctx.channel.purge(limit=1)
        if  game_list == []:
            await ctx.send(embed=discord.Embed(title="❌ No Deals Found! ❌", color= 16711680))
        else:
            await ctx.send(embed=discord.Embed(title=f"🏷️ {len(game_list)} Deals Found! 🏷️", color= 10026752))
        for game in game_list:
            embed=discord.Embed(title=game['game_title'], color= 7461119, url=game['deal_link'])
            embed.set_image(url=game['thumbnail'])
            embed.add_field(name="Cheapest Price", value=f"${game['cheapset_price']}", inline=False)
            embed.add_field(name="Store", value=game['cheapest_store'], inline=False)
            embed.set_footer(text=f"Searched By: {ctx.author.display_name}")
            await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Search Complete ✅", color= 10026752, 
                description="")
                )
    except Exception as e :
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(
                title="🚧 An Error Occured 🚧", color= 16711680, 
                description="Please Try again or Enter '!sbcmds' for more commands!")
                )
        
@bot.command()
async def dealsLookUp(ctx, storeID, lowerPrice=None, upperPrice=None):
    await ctx.send(embed=discord.Embed(title=f"🔎 Searching.... 🔎", color= 10026752))
    try:
        deals_list = backendAPI.dealsLookUp(storeID=storeID, lowerPrice=lowerPrice, upperPrice=upperPrice)
        await ctx.channel.purge(limit=1)
        if  deals_list == []:
            await ctx.send(embed=discord.Embed(title="❌ No Deals Found! ❌", color= 16711680))
        else:
            await ctx.send(embed=discord.Embed(title=f"🏷️ {len(deals_list['deals'])} Deals Found! 🏷️", color= 10026752))
        await ctx.send(
            embed=discord.Embed(title=f"{deals_list['store_name']} Deals", color= 7461119).set_image(url=deals_list['store_banner'])
        )
        for game_deal in deals_list['deals']:
            embed=discord.Embed(title=game_deal['game_title'], color= 7461119, url=game_deal['deal_link'])
            embed.set_image(url=game_deal['thumb'])
            embed.add_field(name="Cheapest Price", value=f"${game_deal['sale_price']}", inline=False)
            embed.add_field(name=f"Saved: {game_deal['savings']}%", value="", inline=False)
            await ctx.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                title=f"✅ Search Complete ✅", color= 10026752, 
                description="")
                )
    except Exception as e:
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(
                title=f"🚧 An Error Occured 🚧", color= 16711680, 
                description="Please Try again or Enter '!sbcmds' for more commands!")
                )

@bot.command()
async def stores(ctx):
    store_list = backendAPI.available_stores()
    embed = discord.Embed(title="🖥️ Trusted Websites 🖥️", color= 16777215)
    for store in store_list:
        embed.add_field(name=f"[{store['storeID']}] {store['storeName']}", value="")
    await ctx.send(embed=embed)
        


##################################################################################################

@bot.command()
async def sbcmds(ctx):
    embed = discord.Embed(title="🤖 SteamBud Commands 🤖", color= 16777215)
    embed.add_field(name="🔗 | !info", value='Bot Info', inline=False)
    embed.add_field(name="🔗 | !sbcmds", value='SteamBud Commands', inline=False)
    embed.add_field(name="🔗 | !stores", value='Return Trusted Websites', inline=False)
    embed.add_field(name='🔗 | !searchgame "<game name>" <amount **optional **max=10>', value='Search Games and Respective Game ID', inline=False)
    embed.add_field(name="🔗 | !dealsLookUp <storeID> <lowerPrice **optional> <upperPrice **optional>", value='Return Top 10 Deals From Selected Store Based on Lower and Upper Price.', inline=False)
    embed.add_field(name='🔗 | !findDeals <appID>', value='Search Deals Based on appID', inline=False)
    embed.add_field(name='🔗 | !steamID <steamappid>', value='Search Deals Based on the SteamAppID', inline=False)
    embed.add_field(name='🔗 | !steamLINK <steamlink>', value='Search Deals Based on the Steam Link', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="🤖 SteamBud Info 🤖", description="SteamBud is an open source discord bot made for every game enthusiast. Check the github repository for more info", color= 16777215)
    embed.add_field(name=f"👨‍💻 Developer: @genua", value='', inline=False)
    embed.add_field(name="🔗 GitHubRepo: https://github.com/neil-py/SteamBud-Bot", value='', inline=False)
    await ctx.send(embed=embed)

def main(token):
    bot.run(token)

if __name__ == '__main__':
    main(TOKEN)

