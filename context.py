# This file is for general infos

#puuid de MrGhastien
# L7MN_B_7iqnXxB3aY6H_eePfmKsEYVNlXm06F_69K339LPo87msHCilSzdf6QTGrJVpvAjyon89r3w

#puuid de Erwann
#

errors = { '200' : 'Request accepted', '400' : 'Bad request', '401' : 'Unauthorized', '403' : 'Forbidden'
          ,'404' : 'Not found', '405' : 'Method not allowed','415' : 'Unsupported media type','429' : 'Rate limit exceeded'
          ,'500' : 'Internal server error', '502' : 'Bad gateway','503' : 'Service unavailable', '504' : 'Gateway timeout' }

api_key = "RGAPI-d028b644-6f44-4580-b9b2-052d074b075c"
location = "home"
name = "rito"
region = "euw1"
prompt = "<|" + location + "|>"

puuid = ""
id = ""
summonnerLevel = 0

import requests, json


def getChampionNameById(id):
    urlChampionNameById = "http://ddragon.leagueoflegends.com/cdn/10.2.1/data/en_US/champion.json"
    ChampionNameByIdResponse = requests.get(urlChampionNameById)
    JSONChampionNameByIdResponse = ChampionNameByIdResponse.json()
    for champion in JSONChampionNameByIdResponse['data']:
        if(JSONChampionNameByIdResponse['data'][champion]['key'] == str(id)):
            return champion

def getfreechampions():
    urlFreeChampionIds = "https://" + region + ".api.riotgames.com/lol/platform/v3/champion-rotations?api_key=" + api_key
    FreeChampionIds = requests.get(urlFreeChampionIds)
    JSONfreechampionsid = FreeChampionIds.json()['freeChampionIds']
    rotafreechampions = []
    for id in JSONfreechampionsid:
        rotafreechampions.append(getChampionNameById(id))
    return rotafreechampions


def getSummonerByName():
    urlSummonerByName = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + api_key
    SummonerByNameResponse = requests.get(urlSummonerByName)
    return SummonerByNameResponse

def getMatchlist(gamesNb):
    if gamesNb > 50:
        raise "gamesNb must be less than 50"
    urlMatchlist = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=" + str(gamesNb) +"&api_key=" + api_key
    MatchlistResponse = requests.get(urlMatchlist)
    if(MatchlistResponse.status_code != 200):
        print("Error: " + str(MatchlistResponse.status_code) + " " + errors[str(MatchlistResponse.status_code)])
    return MatchlistResponse

def getMatchById(id):
    urlMatchById = "https://europe.api.riotgames.com/lol/match/v5/matches/" + id + "?api_key=" + api_key
    MatchByIdResponse = requests.get(urlMatchById)
    return MatchByIdResponse

def getMatchInfo(id):
    MatchByIdResponse = getMatchById(id)
    #if(MatchByIdResponse.status_code != 200):
     #   print("Error: " + str(MatchByIdResponse.status_code) + " " + errors[str(MatchByIdResponse.status_code)])
    JSONMatchByIdResponse = MatchByIdResponse.json()
    participantId = -1
    for i in range (10):
        if(JSONMatchByIdResponse['info']['participants'][i]['summonerName'] == name):
            participantId = i

    matchinfos = {
        "date" : JSONMatchByIdResponse['info']['gameCreation'],
        "gameDuration" : JSONMatchByIdResponse['info']['gameDuration'],
        "ChampionName" : JSONMatchByIdResponse['info']['participants'][participantId]['championName'],
        "kills" : JSONMatchByIdResponse['info']['participants'][participantId]['kills'],
        "deaths" : JSONMatchByIdResponse['info']['participants'][participantId]['deaths'],
        "assists" : JSONMatchByIdResponse['info']['participants'][participantId]['assists'],
        "win" : JSONMatchByIdResponse['info']['participants'][participantId]['win'],
    }
    return matchinfos

def prompt(message):
    if(location == "summoner" and name != "rito"):
        print("<|" + location + "|" + name + "|>" + message)
    else:
        print("<|" + location + "|>" + message)

def secondInMinutes(seconds):
    sec = seconds % 60
    min = int(seconds / 60)

    if sec < 10:
        sec = "0" + str(sec)
    if min < 10:
        min = "0" + str(min)

    return str(min) + ":" + str(sec)

def unixToDate(unix):
    import datetime
    return datetime.datetime.fromtimestamp(unix/1000).strftime('%Y-%m-%d %H:%M:%S')

def formatChampionName(name):
    length = len(name)
    return name + " " * (12 - length)

def KDASpacing(kda):
    length = len(kda)
    return kda + " " * (8 - length)

def get_top_three_keys(d):
    # Get a list of (key, value) tuples from the dictionary
    items = list(d.items())
    # Sort the list of tuples by value in descending order
    items.sort(key=lambda x: x[1], reverse=True)
    # Get the keys of the first three items in the sorted list
    top_keys = [item[0] for item in items[:3]]
    # Return the top three keys
    return top_keys