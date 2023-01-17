# import http.client
#
# conn = http.client.HTTPSConnection("api.sportradar.com")
#
# conn.request("GET", "/mlb/trial/v7/en/games/2023/01/16/boxscore.xml?api_key=6ujezamjxp3hfhdqxqefkygg")
#
# res = conn.getresponse()
# data = res.read()
#
# print(data.decode("utf-8"))

import requests
import json

# leagues = ["mlb", "nba", "nhl", "nba"];
# leagueapis = ["3ughsyzsev7zv77nbmmcae5q", "aahfrx7shknnmup4tkrbc5rk", "aahfrx7shknnmup4tkrbc5rk", "aahfrx7shknnmup4tkrbc5rk"]
resultdate = "2022/4/10"
leagues = ["mlb", "nba"];
leagueurl = ["https://api.sportradar.com/mlb/trial/v7/en/games/" + resultdate + "/boxscore.json?api_key=3ughsyzsev7zv77nbmmcae5q",
             "https://api.sportradar.com/nba/trial/v7/en/games/" + resultdate + "/schedule.json?api_key=vd86r5thtnug6e4zccvgwb4r"
]

result = 0
from pprint import pprint
currentgame = 0
gamecount = 0
leaguecount = len(leagues)
currentleague = 0
leagueacronym = 0

while currentleague < leaguecount:
    url = leagueurl[currentleague]
    currentleaguename = leagues[currentleague]
    # print(url)
    currentleague = currentleague + 1
    response = requests.get(url)
    # print(response.text)

    # res= response.text['league']['games']
    res = json.loads(response.text)
    if currentleaguename == "mlb":
        gamecount = len(res['league']['games'])
    elif currentleaguename == "nba":
        gamecount = len(res['games'])

    currentgame = 0
    # temp, hard-code variables for testing
    find = 'WAS'

    while currentgame < gamecount:

        if currentleaguename == "mlb":
            home = res['league']['games'][currentgame]['game']['home']['abbr']
            away = res['league']['games'][currentgame]['game']['away']['abbr']
            hometext = res['league']['games'][currentgame]['game']['home']['market'] + " " + res['league']['games'][currentgame]['game']['home']['name']
            awaytext = res['league']['games'][currentgame]['game']['away']['market'] + " " + res['league']['games'][currentgame]['game']['away']['name']
            homescore = res['league']['games'][currentgame]['game']['home']['runs']
            awayscore = res['league']['games'][currentgame]['game']['away']['runs']
        elif currentleaguename == "nba":
            home = res['games'][currentgame]['home']['alias']
            away = res['games'][currentgame]['away']['alias']
            hometext = res['games'][currentgame]['home']['name']
            awaytext = res['games'][currentgame]['away']['name']
            if res['games'][currentgame]['status'] != 'unnecessary':
                homescore = res['games'][currentgame]['home_points']
                awayscore = res['games'][currentgame]['away_points']

        if home == find:
            if homescore > awayscore:
                result = "and won " + str(homescore) + " to " + str(awayscore)
            else:
                result = "and lost " + str(awayscore) + " to " + str(homescore)
            print(hometext, "played", awaytext, result, "- home game")
        if away == find:
            if homescore > awayscore:
                result = "and lost " + str(homescore) + " to " + str(awayscore)
            else:
                result = "and won " + str(awayscore) + " to " + str(homescore)
            print(awaytext, "played", hometext, result, "- away game")
        currentgame = currentgame + 1
#print(res)