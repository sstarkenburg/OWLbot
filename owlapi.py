#!/env/bin/python3
import sys
import json
import pprint
from datetime import datetime

import discord
import requests
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import asyncio

# hmmm, I get this from teams() as well, but I use this also to compare to
# /shrug
owl_teams = {
    'Dallas Fuel':            4523,
    'Philadelphia Fusion':    4524,
    'Houston Outlaws':        4525,
    'Boston Uprising':        4402,
    'New York Excelsior':     4403,
    'San Francisco Shock':    4404,
    'Los Angeles Valiant':    4405,
    'Los Angeles Gladiators': 4406,
    'Florida Mayhem':         4407,
    'Shanghai Dragons':       4408,
    'Seoul Dynasty':          4409,
    'London Spitfire':        4410
}

owl_baseurl = "https://api.overwatchleague.com"


def fetch(thing):
    response = requests.get(owl_baseurl + thing)
    if response.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET {} {}'.format(thing, response.status_code))
        return None
    return json.loads(response.content.decode('utf-8'))


def teams():
    teamsJSON = fetch("/teams")

    if teamsJSON is not None:
        #print(teamsJSON)
        print("Here's the OWL teams: ")
        for k in teamsJSON['competitors']:
            print('{0}'.format(k['competitor']['name']))
    else:
        print('[!] Request Failed')


def getTeam(t_input):
    teamsJSON = fetch("/teams")

    if teamsJSON is not None:
        winrar = process.extractOne(t_input, owl_teams.keys(), scorer= fuzz.ratio)
        return winrar
    else:
        print('[!] Request Failed')


# from /matches
# i don't think this shows all the actual matches, will use something else
def getMatches():
    matchesJSON = fetch("/matches")

    if matchesJSON is not None:
        for i in matchesJSON['content']:
            if i['state'] == "PENDING":
                print('Upcoming (in progress?) match: {0} vs {1}'.format(
                      i['competitors'][0]['name'],
                      i['competitors'][1]['name']))
                print('Starts at {0}'.format(
                      datetime.fromtimestamp(int(i['startDate']/1000)).
                      strftime('%H:%M:%S %m-%d')))
            if i['state'] == "CONCLUDED":
                print('Previous match from {0}: {1} vs {2}'.format(
                      datetime.fromtimestamp(int(i['startDate']/1000)).
                      strftime('%m-%d'),
                      i['competitors'][0]['name'],
                      i['competitors'][1]['name']))
                print(' - {0} won'.format(i['winner']['name']))
    else:
        return('[!] Request Failed')


def getLiveMatch():
    matchJSON = fetch("/live-match")
    embed = discord.Embed(title="Live Overwatch League Match",
                          colour=discord.Colour(0xfaa02e),
                          url="https://overwatchleague.com/en-us/schedule")
    embed.set_thumbnail(url="https://bnetcmsus-a.akamaihd.net/cms/page_media/JEUWQ6CN33BR1507857496436.svg")
    embed.set_footer(text="work in progress")

    if matchJSON is not None:
        # print(matchJSON['data']['liveMatch'])
        if matchJSON['data']['liveMatch']['liveStatus'] == "UPCOMING":
            embed.add_field(name='No live match right now.',
                            value='The next, upcoming match is:')
            embed.add_field(name='{0} vs {1}'.format(
                                matchJSON['data']['liveMatch']['competitors'][0]['name'],
                                matchJSON['data']['liveMatch']['competitors'][1]['name']),
                           value='Starts on {0}'.format(datetime.fromtimestamp(
                                int(matchJSON['data']['liveMatch']['startDateTS']/1000)).
                                strftime('%H:%M on %m-%d')))
        elif matchJSON['data']['liveMatch']['liveStatus'] == "PENDING":
            pass
    else:
        print('[!] Request Failed')
    return embed


def getUpcomingMatches():
    matchJSON = fetch("/schedule")
    embed = discord.Embed(title="Upcoming Overwatch League Matches",
                          colour=discord.Colour(0xfaa02e),
                          url="https://overwatchleague.com/en-us/schedule")
    embed.set_thumbnail(url="https://bnetcmsus-a.akamaihd.net/cms/page_media/JEUWQ6CN33BR1507857496436.svg")
    embed.set_footer(text="work in progress")

    if matchJSON is not None:
        uc = 0  # upcoming count
        done = False
        for stage in matchJSON['data']['stages']:
            for match in stage['matches']:
                if (match['state'] != "CONCLUDED") and (uc < 3):
                    comp0 = fetch('/teams/{0}'.format(match['competitors'][0]['id']))
                    comp1 = fetch('/teams/{0}'.format(match['competitors'][1]['id']))

                    embed.add_field(name=datetime.fromtimestamp(int(
                                        match['startDateTS']/1000)).
                                        strftime('__At %H:%M on %m-%d__'),
                                    value="We have:",
                                    inline=False)
                    embed.add_field(name='{0} vs {1}'.format(
                                         match['competitors'][0]['name'],
                                         match['competitors'][1]['name']),
                                    value='W:{0}/L:{1}/D:{2} -- W:{3}/L:{4}/D:{5}'.format(
                                          comp0['ranking']['matchWin'],
                                          comp0['ranking']['matchLoss'],
                                          comp0['ranking']['matchDraw'],
                                          comp1['ranking']['matchWin'],
                                          comp1['ranking']['matchLoss'],
                                          comp1['ranking']['matchDraw']))
                    uc += 1
                if uc >= 3:
                    done = True
                    break
            if done == True:
                break

    else:
        print('[!] Request Failed')
    return embed
















