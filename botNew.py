import json
from turtle import title
from unittest import result
from urllib import response
import requests
import discord
from discord.ext import commands
import responses
from discord import app_commands
import array
import urllib.request
import urllib3
from discord.interactions import Interaction
import datetime, time
import selenium
import csv
import asyncio

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.all()
    intents.members = True

    global startTime
    startTime = time.time()
    print(startTime)

    bot = commands.Bot(command_prefix='--', intents=intents) 
    TOKEN_Discord = ""
    TOKEN_Riot = ""


        #initializes the ugg scraper to rewrite the Tierlist.csv file (first part only, second part formats it in some way)

    #with open("loltierlist.py") as f:
        #exec(f.read())

    #with open('Tierlist.csv', mode='r') as csv_file:
            #csv_reader = csv.DictReader(csv_file)
            #line_count = 0
            #for row in csv_reader:
                #if line_count ==0:
                    #print(f'Column names are {", ".join(row)}')
                    #line_count += 1
                #print(f'\t{row["Champion Name"]} has a winrate of {row["Win Rate"]}, and has a ban rate of {row["Ban Rate"]}.')
                #line_count += 1
            #print(f'Processed {line_count} lines.')

    def clearNameSpaces(nameWithSpaces):
        result = ""
        for n in nameWithSpaces:
            result = result + " " + str(n)
        return result

    def getProfile(region, name):
        if region == "eune":
            API_Riot = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        if region == "na":
            API_Riot = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        if region == "kr":
            API_Riot = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        if region == "euw":
            API_Riot = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        if region == "br":
            API_Riot = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        response = requests.get(API_Riot)
        if response.status_code == 200:
            jsonDataSummoner = response.json()
            sEncryptedId = jsonDataSummoner['id']
            sName = jsonDataSummoner['name']
            sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
            sIcon = "http://ddragon.leagueoflegends.com/cdn/13.6.1/img/profileicon/" + str(jsonDataSummoner['profileIconId']) + ".png"
            print(response.status_code)
            return (sName, sLevel, sIcon, sEncryptedId)
        else:
            print("not found")
            return None
            
        
        #return (sName, sLevel, sIcon, sEncryptedId)
        

    def fetchMasteries(region, sEncryptedId):
        limit = "5" #shit
        champions = []
        arrids, arrlevels, arrpoints, arrname, arrimgs, arrtime = [], [], [], [], [], []
        championsURL = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"
        iconURL = "http://ddragon.leagueoflegends.com/cdn/12.18.1/img/champion/"

        if region == "eune":
            API_Riot = f"https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"
        if region == "euw":
            API_Riot = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"
        if region == "na":
            API_Riot = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"
        if region == "kr":
            API_Riot = f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"
        if region == "br":
            API_Riot = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"

        response = requests.get(API_Riot)
        playersChampions = response.json()
        for champion in playersChampions:
            arrids.append(champion['championId'])
            arrlevels.append(champion['championLevel'])
            arrpoints.append(champion['championPoints'])
            arrtime.append(champion['lastPlayTime'])
            #time = str(arrtime)
            
            
        
        champions_db = requests.get(championsURL).json()   

        
        [champions.append(champion) for champion in champions_db['data']]        

        for championId in arrids:
            for name in champions:
                wantedChampion = champions_db['data'][name]['key']             
                if int(wantedChampion) == int(championId):            
                    arrname.append(name)
                    arrimgs.append(iconURL + name + ".png")
                    #print(time)
        
        print(arrname)

        if arrname[0] == 'Shen':
            arrname[0] = 'Shen :goat:'
        elif arrname[1] == 'Shen':
            arrname[1] = 'Shen :goat:'
        elif arrname[2] == 'Shen':
            arrname[2] = 'Shen :goat:'
        elif arrname[3] == 'Shen':
            arrname[3] = 'Shen :goat:'
        elif arrname[4] == 'Shen':
            arrname[4] = 'Shen :goat:'
        
        return [arrname, arrpoints, arrlevels, arrimgs, arrtime]


    @bot.command()
    async def eune(ctx, *nameWithSpaces):
        region = "eune"
        name = clearNameSpaces(nameWithSpaces)
        summoner = getProfile(region, name)
        championsMastery = fetchMasteries(region, summoner[3])
        embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
        embed.set_thumbnail(url=summoner[2])
        await ctx.send(embed=embed)
        
        for i in range(len(championsMastery)+1):
            tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}"
            if championsMastery[2][i] == 7:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x0AC7C6)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 6:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xC51BC0)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 5:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xCB1E1E)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 4:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xD1CF0F)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x858585)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
    

    @bot.command()
    async def na(ctx, *nameWithSpaces):
        region = "na"
        name = clearNameSpaces(nameWithSpaces)
        summoner = getProfile(region, name)
        championsMastery = fetchMasteries(region, summoner[3])
        embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xC8C8C8)
        embed.set_thumbnail(url=summoner[2])
        await ctx.send(embed=embed)
        
        for i in range(len(championsMastery)+1):
            tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}"
            if championsMastery[2][i] == 7:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x0AC7C6)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 6:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xC51BC0)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 5:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xCB1E1E)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 4:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xD1CF0F)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x858585)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)

    @bot.command()
    async def kr(ctx, *nameWithSpaces):
        region = "kr"
        name = clearNameSpaces(nameWithSpaces)
        summoner = getProfile(region, name)
        championsMastery = fetchMasteries(region, summoner[3])
        embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
        embed.set_thumbnail(url=summoner[2])
        await ctx.send(embed=embed)
        
        for i in range(len(championsMastery)+1):
            tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}"
            if championsMastery[2][i] == 7:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x0AC7C6)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 6:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xC51BC0)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 5:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xCB1E1E)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 4:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xD1CF0F)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x858585)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)

    @bot.command()
    async def euw(ctx, *nameWithSpaces):
        region = "euw"
        name = clearNameSpaces(nameWithSpaces)
        summoner = getProfile(region, name)
        championsMastery = fetchMasteries(region, summoner[3])
        embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
        embed.set_thumbnail(url=summoner[2])
        await ctx.send(embed=embed)
        
        for i in range(len(championsMastery)+1):
            tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}"
            if championsMastery[2][i] == 7:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x0AC7C6)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 6:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xC51BC0)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 5:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xCB1E1E)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 4:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xD1CF0F)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x858585)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)

    @bot.command()
    async def br(ctx, *nameWithSpaces):
        region = "br"
        name = clearNameSpaces(nameWithSpaces)
        summoner = getProfile(region, name)
        championsMastery = fetchMasteries(region, summoner[3])
        embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
        embed.set_thumbnail(url=summoner[2])
        await ctx.send(embed=embed)
        
        for i in range(len(championsMastery)+1):
            tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}"
            if championsMastery[2][i] == 7:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x0AC7C6)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 6:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xC51BC0)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 5:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xCB1E1E)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            elif championsMastery[2][i] == 4:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xD1CF0F)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0x858585)
                embed.set_thumbnail(url=championsMastery[3][i])
                await ctx.send(embed=embed)


    @bot.event
    async def on_ready():
        print("Bot is running...")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
    
        botactivity = discord.Activity(type=discord.ActivityType.watching, name="twitch.tv/xpetu", large_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/1200px-LoL_icon.svg.png')
        await bot.change_presence(activity=botactivity, status=discord.Status.online)
    
    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}")
    
    @bot.tree.command(name="say")
    @app_commands.describe(arg = "What do you want to say?")
    async def say(interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(f"{arg} <:gdhappy:779864437443133460>")
    
    @bot.tree.command(name="goodshit")
    async def goodshit(interaction: discord.Interaction):
        await interaction.response.send_message(f"https://www.twitch.tv/xpetu")
    
    @bot.tree.command(name="help")
    async def help(interaction: discord.Interaction):
        await interaction.response.send_message(f"```--commands: \n\n --(region) (name) - shows summoner level + champion masteries \n \n Supported Regions: \n North America -> na \n Europe West -> euw \n Europe East -> eune \n Korea -> kr \n Brazil -> br \n\n\n Slash(/) Commands: \n\n /hello \n /say \n /goodshit \n /inspirobot - get inspired by ai \n /specmatch - insights on someone's current game (only for na server) (not done yet) \n /googlechamp - info on specific league champ ```")

    
    
    #SPECTATOR THING
    
    @bot.tree.command(name="specmatch", description="Shows the current match of the desired summoner.")
    @app_commands.describe(name="What is the summoner's name?")
    async def specmatch(ctx: commands.Context, name: str): #changed the interaction.discord thing. it seems to work 
        API_Riot = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        response = requests.get(API_Riot)
        jsonDataSummoner = response.json()
        encryptedSummonerId = jsonDataSummoner['id']
        print(encryptedSummonerId)
        sName = jsonDataSummoner['name']
        sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
        sIcon = "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/profileicon.json" + str(jsonDataSummoner['profileIconId']) + ".png"
        print(sName)
        print(sLevel)
        
        champions = []
        arrids, arrlevels, arrpoints, arrname, arrimgs = [], [], [], [], []
        championsURL = "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json"
        iconURL = "http://ddragon.leagueoflegends.com/cdn/12.18.1/img/champion/"

        API_Riot_Game = f"https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + encryptedSummonerId + "?api_key=" + TOKEN_Riot
        
        responseGame = requests.get(API_Riot_Game)
        CurrentGameParticipant = responseGame.json()
               
        

        gameMode = str(CurrentGameParticipant['gameMode'])
        participants = (CurrentGameParticipant['participants'])
        gameId = (CurrentGameParticipant['gameId'])
        print(participants) #work on making finishing spec match (maybe by doing something like porofessor)

        print(participants)
        for champion in participants:
            arrids.append(champion['championId'])     
        
        champions_db = requests.get(championsURL).json()
            
        [champions.append(champion) for champion in champions_db['data']]        

        for championId in arrids:
            for nameChamp in champions:
                wantedChampion = champions_db['data'][nameChamp]['key']             
                if int(wantedChampion) == int(championId):
                    arrname.append(nameChamp)
                    arrimgs.append(iconURL + nameChamp + ".png")
        #print(participants[0])
        #print(participants[1])

        
        
        
        #Match info (kills, etc)
        
        #API_Riot_Summoner = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
        #responseGameSummoner = requests.get(API_Riot_Summoner)
        #CurrentGameSummoner = responseGameSummoner.json()

        #puuid = (CurrentGameSummoner['puuid'])
        #print(puuid)
        #print("this the the thing")

        #API_Riot_Game_Match = f"https://na1.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        #responseGameMatch = requests.get(API_Riot_Game_Match)
        #summonerGameMatch = responseGameMatch.json()
        #print(summonerGameMatch)

        #API_Riot_Game_Info = f"https://na1.api.riotgames.com/lol/match/v5/matches/{gameId}" #need to use differnet puuid match api for it to work
        #responseGameInfo = requests.get(API_Riot_Game_Info)
        #CurrentGameInfo = responseGameInfo.json()

        #infoData =  (CurrentGameInfo['info'])
        #print(infoData)

        print(arrname)
        print(arrimgs)

        if gameMode == 'CLASSIC':
            gameMode = "Summoner's Rift"

        if name == participants[0]['summonerName']:
            print("it worked")
            print("1")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[0]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[0]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[0])
            await ctx.response.send_message(embed=embed)
        elif name == participants[1]['summonerName']:
            print("it worked")
            print("2")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[1]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[1]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[1])
            await ctx.response.send_message(embed=embed)
        elif name == participants[2]['summonerName']:
            print("it worked")
            print("3")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[2]}`.")
            embed = discord.Embed(title=name, ddescription=f"{gameMode} \n\n Currently playing {arrname[2]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[2])
            await ctx.response.send_message(embed=embed)
        elif name == participants[3]['summonerName']:
            print("it worked")
            print("4")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[3]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[3]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[3])
            await ctx.response.send_message(embed=embed)
        elif name == participants[4]['summonerName']:
            print("it worked")
            print("5")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[4]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[4]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[4])
            await ctx.response.send_message(embed=embed)
        elif name == participants[5]['summonerName']:
            print("it worked")
            print("6")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[5]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[5]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[5])
            await ctx.response.send_message(embed=embed)
        elif name == participants[6]['summonerName']:
            print("it worked")
            print("7")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[6]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[6]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[6])
            await ctx.response.send_message(embed=embed)
        elif name == participants[7]['summonerName']:
            print("it worked")
            print("8")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[7]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[7]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[7])
            await ctx.response.send_message(embed=embed)
        elif name == participants[8]['summonerName']:
            print("it worked")
            print("9")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[8]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[8]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[8])
            await ctx.response.send_message(embed=embed)
        elif name == participants[9]['summonerName']:
            print("it worked")
            print("10")
            #await ctx.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[9]}`.")
            embed = discord.Embed(title=name, description=f"{gameMode} \n\n Currently playing {arrname[9]}.", color=0xFFD500)
            embed.set_thumbnail(url=arrimgs[9])
            await ctx.response.send_message(embed=embed)
        else:
            print("you fucked up")

        #if encryptedSummonerId == (participant['summonerId']):
        #for champion in participants:
            #arrids.append(champion['championId'])
                    #arrlevels.append(champion['championLevel'])
                    #arrpoints.append(champion['championPoints'])
                    
        #champions_db = requests.get(championsURL).json()
                

        #[champions.append(champion) for champion in champions_db['data']]        

        #for championId in arrids:
            #for nameChamp in champions:
                #wantedChampion = champions_db['data'][nameChamp]['key']             
                #f int(wantedChampion) == int(championId):            
                    #arrname.append(nameChamp)
                    #arrimgs.append(iconURL + nameChamp + ".png")
                            

        #await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{nameChamp}`.")
        #print(nameChamp)
            #print(participant)
     

    

    

        
        
        
        #return (sName, sLevel, sIcon, sEncryptedId)

    @bot.tree.command(name="inspirobot")
    async def inspirobot(interaction: discord.Interaction):
        http =urllib3.PoolManager()
        response = http.request('GET','https://inspirobot.me/api?generate=true')
        image = response.data
        imageNew = image.decode('utf-8')
        print(imageNew)

        await interaction.response.send_message(f"{imageNew}")
    
    @bot.tree.command(name="uptime", description="View the uptime for the bot.")
    async def uptime(interaction: discord.Interaction):
        currentTime = time.time()
        print(currentTime)
        timeDifference = int(round(currentTime - startTime))
        convertTime = str(datetime.timedelta(seconds = timeDifference))
        print(f"The bot has been running for {timeDifference} seconds.")
        await interaction.response.send_message(f"The bot has been running for `{convertTime}` seconds.")

         
###############################################
    #SEARCH FOR SPECIFIC CHAMP'S INFO
###############################################
   
    @bot.tree.command(name="googlechamp", description="Google a champion from League of Legends")
    @app_commands.describe(name="What is the champion's name?")
    async def googlechamp(ctx: commands.Context, name: str): #consider changing interaction: discord.Interaction to ctx: commands.Context found in previous command. might fix embed issue
        nameCorrect = name.capitalize()
        if nameCorrect == "Aurelionsol":
            nameCorrect = "AurelionSol"
        elif nameCorrect == "Wukong":
            nameCorrect = "MonkeyKing"
        elif nameCorrect == "Monkeyking":
            nameCorrect = "MonkeyKing"
        
        print(nameCorrect)

        url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion/{nameCorrect}.json"
        global nameEdit
        nameEdit = nameCorrect
        global champBanner
        champBanner = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{nameCorrect}_0.jpg"

        response = requests.get(url)

        with open('Tierlist.csv') as file_obj:

            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                try:
                    if row[0] == nameCorrect:
                        global winr
                        global banr
                        global grade
                        winr = row[1]
                        banr = row[2]
                        grade = row[3]
                except:
                    continue
        print(winr)
        print(banr)
        print(grade)
        

        if response.status_code == 200:
            data = response.json()
            champions = data["data"]

            champion_name = nameCorrect
            if champion_name in champions:
                champion_data = champions[champion_name]
                #print("Champion Name:", champion_name)
                #print("Champion Title:", champion_data["title"])
                global title
                title = (champion_data["title"])
                #print("Champion Lore:", champion_data["blurb"])
                global blurb
                blurb = (champion_data["lore"])
                #print("Champion Stats:")
                #print("\tHealth Points:", champion_data["stats"]["hp"])
                #print("\tAttack Damage:", champion_data["stats"]["attackdamage"])
                #print("\tMagic Damage:", champion_data["stats"]["mpperlevel"])
                global baseHP
                global baseAD
                global baseAP
                global spells
                global abilities
                global ability
                global ability_message
                global difficulty
                baseHP = (champion_data["stats"]["hp"])
                baseAD = (champion_data["stats"]["attackdamage"])
                baseAP = (champion_data["stats"]["mpperlevel"])
                difficulty = (champion_data["info"]["difficulty"])
                image = (champion_data["image"])
                #print(image)
                #print("\n")
                spells = (champion_data["spells"])
                #print(spells)
                
                abilities = champion_data["spells"]
                ability_message = ""
                for ability in abilities:
                     ability_message += f"**{ability['name']}:**\n\t{ability['description']}\n\n"
                    
                #print(ability_message)

                global embColor

                if grade == "S+":
                    embColor = int(hex(0xFF9B00), 0)
                elif grade == "S":
                    embColor = int(hex(0x3273F4), 0)
                elif grade == "A":
                    embColor = int(hex(0x5A80D6), 0)
                elif grade == "B":
                    embColor = int(hex(0xFFFBF2), 0)
                elif grade == "C":
                    embColor = int(hex(0xFCB1AE), 0)
                elif grade == "D":
                    embColor = int(hex(0xFF4246), 0)

                print(embColor)

                #await ctx.response.send_message(f"```Champion Name: {name} \n\nChampion Title: {title} \n\nBio: {blurb} \n\nChampion Base Stats: \n\tHealth Points: {baseHP} \n\tAttack Damage: {baseAD} \n\tMagic Damage: {baseAP}\n\n\n Spells:\n\n{ability_message}``` \n{champBanner}")
                #embed = discord.Embed(title=f"__{nameCorrect}, {title}__", description=f"**{grade}**\n\n**Bio:** {blurb} \n\n **Difficulty:** {difficulty} / 10 \n\n **Winrate:** {winr}\n **Ban Rate:** {banr}", color=embColor)
                embed = discord.Embed(title=f"__{nameCorrect}, {title}__", description=f"**{grade}**\n\n**Difficulty:** {difficulty} / 10\n**Winrate:** {winr}\n**Ban Rate:** {banr}\n\n**Bio:**{blurb}", color=embColor)
                embed.set_image(url=champBanner)
                await ctx.response.send_message(embed=embed, view=MyViewMore())

                
            else:
                print(f"Champion `{nameCorrect}` not found.")
                await ctx.response.send_message(f"The Champion {nameCorrect} was not found.")
        else:
            print("Error:", response.status_code)
            await ctx.response.send_message(f"`Error {response.status_code}` : champion `{nameCorrect}` not found. Check spelling.")
    
    
    class MyViewMore(discord.ui.View):
        @discord.ui.button(label="More", style=discord.ButtonStyle.primary)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.button):

            embedEdit = discord.Embed(title=f"__{nameEdit}, {title}__", description=f"**{grade}**\n\n**Difficulty:** {difficulty} / 10\n**Winrate:** {winr}\n**Ban Rate:** {banr}\n\n**Bio:**{blurb}\n\n __Spells:__\n\n{ability_message}", color=embColor)
            embedEdit.set_image(url=champBanner)
            await interaction.message.edit(embed=embedEdit, view=MyViewLess())
            await interaction.response.defer()
    
    class MyViewLess(discord.ui.View):
        @discord.ui.button(label="Less", style=discord.ButtonStyle.primary)
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.button):

            embedEditLess = discord.Embed(title=f"__{nameEdit}, {title}__", description=f"**{grade}**\n\n**Difficulty:** {difficulty} / 10\n**Winrate:** {winr}\n**Ban Rate:** {banr}\n\n**Bio:**{blurb}", color=embColor)
            embedEditLess.set_image(url=champBanner)
            await interaction.message.edit(embed=embedEditLess, view=MyViewMore())
            await interaction.response.defer()
    
    #uses porofesor to get match info. Idk what to do with it

    @bot.tree.command(name="test", description="test")
    async def test(interaction: discord.Interaction):
        http =urllib3.PoolManager()
        response = http.request('GET','https://u.gg/lol/champions/aatrox/build/top')
        data = response.data
        print(data)


    
    bot.run(TOKEN_Discord)
