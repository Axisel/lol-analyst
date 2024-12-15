import sys

import context
from context import *

exit = False

ANSI_RED = "\033[1;31m"
ANSI_BLUE = "\033[1;34m"
ANSI_RESET = "\033[0;0m"

while(not exit):
    if(context.location == "home"):
        prompt(" select where you want to go : ")
        print("■━■━■━■━■━■━■━■━■━■━■")
        print("Summoner : connect to your summoner account and see plenty informations about your account")
        print("︵‿︵‿︵‿︵︵‿︵‿︵‿︵")
        print("Free champions : see the free champions of the week")
        print("︵‿︵‿︵‿︵︵‿︵‿︵‿︵")
        print("Exit : exit the program")
        print("■━■━■━■━■━■━■━■━■━■━■")
        context.location = input("->")

    match context.location:
        case "home":
            context.location = "home"


        case "summoner":
            context.location = "summoner"
            if(context.name == "rito"):
                prompt("Enter your summoner name : ")
                context.name = input("->")
                SummonerByNameResponse = getSummonerByName()

                if(SummonerByNameResponse.status_code != 200):
                    print("Error : " + errors[str(SummonerByNameResponse.status_code)])

                JSONSummonerByNameResponse = SummonerByNameResponse.json()

                context.id = JSONSummonerByNameResponse['id']
                context.summonnerLevel = JSONSummonerByNameResponse['summonerLevel']
                context.puuid = JSONSummonerByNameResponse['puuid']
                print("Summoner Level : " + str(context.summonnerLevel))
                print("Account ID : " + context.id)
                print("puuid : " + JSONSummonerByNameResponse['puuid'])

            prompt("Select a option :")
            print("1. Get matchlist (50 game max)")
            print("2. Get overall stats (on the last 20 games)")
            print("3. exit")

            choice = input("->")
            match choice:
                case "1":
                    MatchList = getMatchlist(50)
                    print(len(MatchList.json()))
                    print("Date                | Game duration | Champion     | KDA")

                    for matchId in MatchList.json():
                        matchinfos = getMatchInfo(matchId)
                        if( matchinfos['win']):
                            print(str(unixToDate(matchinfos['date'])) + " | " + str(
                                secondInMinutes(matchinfos['gameDuration'])) + "         | " + formatChampionName(
                                matchinfos['ChampionName']) + " | " + KDASpacing(str(matchinfos['kills']) + "/" + str(
                                matchinfos['deaths']) + "/" + str(matchinfos['assists'])) + " | " + ANSI_BLUE + "(W)" + ANSI_RESET)
                        else:
                            print(str(unixToDate(matchinfos['date'])) + " | " + str(
                                secondInMinutes(matchinfos['gameDuration'])) + "         | " + formatChampionName(
                                matchinfos['ChampionName']) + " | " + KDASpacing(str(matchinfos['kills']) + "/" + str(
                                matchinfos['deaths']) + "/" + str(matchinfos['assists'])) + " | " + ANSI_RED + "(L)" + ANSI_RESET)

                case "2":
                    MatchList = getMatchlist(20)
                    games = []
                    for matchid in MatchList.json():
                        matchinfos = getMatchInfo(matchid)
                        games.append(matchinfos)
                    wins = 0
                    kills = 0
                    deaths = 0
                    assists = 0
                    champions = {}
                    for game in games:
                        if(game['win']):
                            wins += 1
                        kills += game['kills']
                        deaths += game['deaths']
                        assists += game['assists']
                        champions[game['ChampionName']] = champions.get(game['ChampionName'], 0) + 1
                    MostPlayedChampions = get_top_three_keys(champions)
                    print("Overall stats :")
                    print("Average KDA : " + str(kills/20) + "/" + str(deaths/20) + "/" + str(assists/20))
                    print("Winrate : " + str(wins/20 * 100) + "%" + " (" + str(wins) + ANSI_BLUE + "W" + ANSI_RESET + "/" + str(20 - wins) + ANSI_RED + "L " + ANSI_RESET + ")")
                    print("Most played champions :")
                    for i in range (len(MostPlayedChampions)):
                        print(str(i+1) + ". " + MostPlayedChampions[i] + " : " + str(champions[MostPlayedChampions[i]]))



                case "3":
                    context.location = "home"

        case "freechampions":
            freechampions = getfreechampions()
            length = len(freechampions)
            for i in range(length):
                if(freechampions[i] == None):
                    continue
                if (i % 5 == 0):
                    print()
                if(i == length - 1):
                    sys.stdout.write(freechampions[i])
                    break
                sys.stdout.write(freechampions[i] + " - ")

            break



        case "exit":
            print("Exiting...")
            break


