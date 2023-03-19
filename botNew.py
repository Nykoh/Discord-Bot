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

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.all()
    intents.members = True

    bot = commands.Bot(command_prefix='--', intents=intents) 
    TOKEN_Discord = "MTA3NTI5NjU2NjI5MTczMDQ2Mg.G5qDEL.uvsLNP7GXYjB57aZ61hyYL0Y426C0V0NagqihQ"
    TOKEN_Riot = "RGAPI-2977359e-84b1-4db9-9240-d63a780837bc"

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
        jsonDataSummoner = response.json()
        sEncryptedId = jsonDataSummoner['id']
        sName = jsonDataSummoner['name']
        sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
        sIcon = "http://ddragon.leagueoflegends.com/cdn/13.4.1/img/profileicon/" + str(jsonDataSummoner['profileIconId']) + ".png"
        return (sName, sLevel, sIcon, sEncryptedId)


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

    
    
    #SPECTATOR THING
    
    @bot.tree.command(name="specmatch", description="Shows the current match of the desired summoner.")
    @app_commands.describe(name="What is the summoner's name?")
    async def specmatch(interaction: discord.Interaction, name: str):
        API_Riot = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
        response = requests.get(API_Riot)
        jsonDataSummoner = response.json()
        encryptedSummonerId = jsonDataSummoner['id']
        print(encryptedSummonerId)
        sName = jsonDataSummoner['name']
        sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
        sIcon = "http://ddragon.leagueoflegends.com/cdn/13.4.1/img/profileicon/" + str(jsonDataSummoner['profileIconId']) + ".png"
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
        #print(participant[0]) #limits the scope to just the summoner searched. (actually idk if it works) (it doesnt)

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

        if name == participants[0]['summonerName']:
            print("it worked")
            print("1")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[0]}`.")
            #embed = discord.Embed(title=name[0], description=gameMode[1], color=0xFFD500)
            #embed.set_thumbnail(url=arrname[0])
            #await discord.Interaction(embed=embed)
        elif name == participants[1]['summonerName']:
            print("it worked")
            print("2")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[1]}`.")
        elif name == participants[2]['summonerName']:
            print("it worked")
            print("3")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[2]}`.")
        elif name == participants[3]['summonerName']:
            print("it worked")
            print("4")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[3]}`.")
        elif name == participants[4]['summonerName']:
            print("it worked")
            print("5")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[4]}`.")
        elif name == participants[5]['summonerName']:
            print("it worked")
            print("6")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[5]}`.")
        elif name == participants[6]['summonerName']:
            print("it worked")
            print("7")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[6]}`.")
        elif name == participants[7]['summonerName']:
            print("it worked")
            print("8")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[7]}`.")
        elif name == participants[8]['summonerName']:
            print("it worked")
            print("9")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[8]}`.")
        elif name == participants[9]['summonerName']:
            print("it worked")
            print("10")
            await interaction.response.send_message(f"The summoner `{name}` is currently playing the `{gameMode}` gamemode. \n They are playing `{arrname[9]}`.")
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

    
    
    
    bot.run(TOKEN_Discord)