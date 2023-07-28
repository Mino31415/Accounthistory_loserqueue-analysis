import requests, json, urllib3, time

urllib3.disable_warnings()

#get player uuid
def uuid(apikey, summonerName):
    print("Retrieving Player UUID")
    data = requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+apikey, verify=False).text
    data = json.loads(data)
    try:
        return data['puuid'], data['id']
    except:
        return None

#get matchhistory
def matchids(apikey, puuid, numgames="30"):
    print("Retrieving Matchhistory")
    data = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count="+numgames+"&api_key="+ apikey, verify=False).text
    data = json.loads(data)
    return data

#get matchinfo
def matchinfo(apikey, matchid):
    print("Retrieving Matchinfo")
    data = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/"+matchid+"?api_key="+apikey, verify=False).text
    data = json.loads(data)
    return data


#get winrate
def winrate(apikey, encryptedID):
    print("Collecting Rank Data")
    data = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+encryptedID+"?api_key="+apikey, verify=False).text
    data = json.loads(data)
    try:
        return data[0]['wins'] / (data[0]['wins'] + data[0]['losses'])
    except:
        return None


#analysis
def analysis(apikey, match, puuid, sleeper=3):
    returndata = []
    #go through matches
    matchdata = matchinfo(apikey, match)
    if matchdata['info']['queueId'] == 420:  #only check ranked matches
        print("\nRanked Match Found")
        #exclude self and opponent
        players = [0,1,2,3,4,5,6,7,8,9]
        for x in range(10):
            if matchdata['metadata']['participants'][x] == puuid:
                players.remove(x)
                if x < 5:
                    team1 = True
                    players.remove(x+5)

                else:
                    team1 = False
                    players.remove(x-5)

        #for each ally (4)
        print("Getting Matchdata")
        for x in range(4):
            print("Sleep timer to avoid rate limit")
            time.sleep(sleeper) #sleep timer to avoid rate limit
            #get winrate
            t1name =  matchdata['info']['participants'][players[x]]['summonerName']
            t2name = matchdata['info']['participants'][players[x]+5]['summonerName']
            try:
                t1encryID = uuid(apikey, summonerName=t1name)[1]
                t2encryID = uuid(apikey, summonerName=t2name)[1]
                t1wr = winrate(apikey, t1encryID)
                t2wr = winrate(apikey, t2encryID)
                if t1wr != None and t2wr != None:
                    if team1 == True:
                        wrdiff = round(100*(t1wr-t2wr), 1)
                    else:
                        wrdiff = round(100*(t2wr-t1wr), 1)
                else:
                    wrdiff = None
            except:
                print("Error collecting winrate")
                wrdiff = None
            print("Done collecting winrate")

            #get damage to champions
            t1dmg = matchdata['info']['participants'][players[x]]['totalDamageDealtToChampions']
            t2dmg = matchdata['info']['participants'][players[x]+5]['totalDamageDealtToChampions']
            if t1dmg != 0 and t2dmg != 0:
                if team1 == True:
                    dmgdiff = round(100*((t1dmg / t2dmg) - 1), 1)
                else:
                    dmgdiff = round(100*((t2dmg / t1dmg) - 1), 1)
            else:
                dmgdiff = None
            print("Done collecting damage dealt")

            #get damage to turrets
            t1dmg = matchdata['info']['participants'][players[x]]['damageDealtToTurrets']
            t2dmg = matchdata['info']['participants'][players[x]+5]['damageDealtToTurrets']
            if t1dmg != 0 and t2dmg != 0:
                if team1 == True:
                    turretdmgdiff = round(100*((t1dmg / t2dmg) - 1), 1)
                else:
                    turretdmgdiff = round(100*((t2dmg / t1dmg) - 1), 1)
            else:
                turretdmgdiff = None
            print("Done collecting damage to objectives")
            
            #get gold
            t1gold = matchdata['info']['participants'][players[x]]['goldEarned']
            t2gold = matchdata['info']['participants'][players[x]+5]['goldEarned']
            if team1 == True:
                golddiff = round(100*((t1gold / t2gold) - 1), 1)
            else:
                golddiff = round(100*((t2gold / t1gold) - 1), 1)
            print("Done collecting gold")

            #get kda
            if matchdata['info']['participants'][players[x]]['deaths'] != 0 and matchdata['info']['participants'][players[x]+5]['deaths'] != 0:
                t1kda = round(matchdata['info']['participants'][players[x]]['kills'] + matchdata['info']['participants'][players[x]]['assists'] / matchdata['info']['participants'][players[x]]['deaths'], 1)
                t2kda = round(matchdata['info']['participants'][players[x]+5]['kills'] + matchdata['info']['participants'][players[x]+5]['assists'] / matchdata['info']['participants'][players[x]+5]['deaths'], 1)
                if team1 == True:
                    kdadiff = round(t1kda  - t2kda, 1)
                else:
                    kdadiff = round(t2kda - t1kda, 1)
            else:
                kdadiff = None
            print("Done collecting stats")
            
            
            returndata.append([wrdiff, dmgdiff, turretdmgdiff, golddiff, kdadiff])
            

        return returndata
    else:
        return None
