import aiohttp
import asyncio
from prettytable import PrettyTable
from fpl import FPL
from matplotlib import pyplot as plt
import operator


def most_val(number, players, games):
    top_performers = sorted(
        players, key=lambda x: float(x.points_per_game)  # (x.pp90-2)/(x.now_cost/10)
        if (x.minutes // 90 > games
            and x.status == "a")
        else 0.0,
        reverse=True)
    #  Outputs in Table form
    player_table = PrettyTable()
    player_table.field_names = ["Player", "£", "G", "A", "CS", "Pts per game", "VAPM", "Total Points", "Games played"]
    player_table.align["Player"] = "l"
    for player in top_performers[:number]:
        goals = player.goals_scored
        assists = player.assists

        #  PrettyTable formatting
        player_table.add_row([player.web_name, f"£{player.now_cost / 10}",
                              goals, assists, player.clean_sheets, player.points_per_game,
                              '{0:.2f}'.format((player.pp90 - 2) / (player.now_cost / 10)), player.total_points,
                              "{0:.2f}".format(player.minutes / 90)
                              ])
    print(player_table)


"""
Function to obtain players classified as midfielders in FPL

args:
    players: a list of player objects from FPL API

returns: 
    list of player objects with element type = 3 (midfielders)
"""


def getMID(players: list) -> list:
    mid = []
    for player in players:
        if player.element_type == 3:
            mid.append(player)
    return mid


"""
Function to obtain players classified as forwards in FPL

args:
    players: a list of player objects from FPL API

returns: 
    list of player objects with element type = 4 (forwards)
"""


def getFWD(players: list) -> list:
    fw = []
    for player in players:
        if player.element_type == 4:
            fw.append(player)
    return fw


"""
Function to obtain players classified as defenders in FPL

args:
    players: a list of player objects from FPL API

returns: 
    list of player objects with element type = 2 (defenders)
"""


def getDF(players: list) -> list:
    defs = []
    for player in players:
        if player.element_type == 2:
            defs.append(player)
    return defs


"""
Function to obtain players classified as goalkeepers in FPL

args:
    players: a list of player objects from FPL API

returns: 
    list of player objects with element type = 1 (goalkeepers)
"""


def getGK(players: list) -> list:
    gk = []
    for player in players:
        if player.element_type == 1:
            gk.append(player)
    return gk


"""
Function to find all teams in FPL

args:
    teams: a list of team objects from FPL API

returns: 
    a dict of all teams with team.id as the key and team name,
     team short name and team points as values
"""


def getAllTeams(teams: list) -> dict:
    TeamData = {}
    for team in teams:
        TeamData[team.id] = [team.name, team.short_name, team.strength]
    return TeamData


"""
Function to return the number of games played using minutes played divided by 90

args:
    player: a player object from FPL API

returns: 
    number of minutes played divided by 90
"""


def getGamesPlayed(player) -> float:
    return player.minutes / 90


"""
Function to group players by their respective EPL team

args:
    players: a list of player objects from FPL API
    teams: a list of team objects from FPL API

returns: 
    players grouped by teams in a dictionary whereby the team shortname
    is the key and a list of the grouped players are the values
"""


def getPlayersByTeam(players: list, teams: list) -> dict:
    AllTeams = getAllTeams(teams)  # retrieve shortened team info
    teamPlayers = {}  # dict to group players by team shortname

    # append player to a team list of team players if player team id is in list of team ids
    for player in players:
        if player.team in AllTeams:
            if AllTeams[player.team][1] not in teamPlayers:  # create empty list for all teams by team shortname
                teamPlayers[AllTeams[player.team][1]] = []
            teamPlayers[AllTeams[player.team][1]].append(player)
    return teamPlayers


"""
Function to sum cost of players grouped by team

args:
    players: a list of player objects from FPL API
    teams: a list of team objects from FPL API

returns: 
    a dict whose indices are team shortnames and whose values are the total FPL cost of 
    said team's players
"""


def getSquadCostbyTeam(players, teams) -> dict:
    playersByTeam = getPlayersByTeam(players, teams)
    teamCosts = {}

    for squad in playersByTeam:  # key in playersByTeam is team shortname
        # using list comprehension to sum player cost in a squad
        teamCosts[squad] = sum((player.now_cost/10) for player in playersByTeam[squad])  # player costs are in digits
        # to change to tens, remove the '/10'
    return teamCosts


"""
Function to sum points of players grouped by team

args:
    players: a list of player objects from FPL API
    teams: a list of team objects from FPL API

returns: 
    a dict whose indices are team shortnames and whose values are the total FPL points of 
    said team's players
"""


def getPlayerPtsPerTeam(players, team):
    playerPtsPerTeam = {}
    teams = getAllTeams(team)
    for player in players:
        if player.team in teams:
            if teams[player.team][1] not in playerPtsPerTeam:  # add player.team shortname as key to playerPtsPerTeam
                # if not yet added
                playerPtsPerTeam[teams[player.team][1]] = player.total_points
                continue
            playerPtsPerTeam[teams[player.team][1]] += player.total_points
    return playerPtsPerTeam


#  Graph total player fantasy points per team
def graphPlayerPointsPerTeam(players, teams):
    data = dict(sorted(getPlayerPtsPerTeam(players, teams).items(), key=operator.itemgetter(1), reverse=True))
    keys = list(data.keys())
    values = list(data.values())
    y = sum(list(data.values())) / 20  # Average total player fantasy points per team

    plt.bar(keys, values)
    plt.plot(keys, [y] * len(values), color='red', linestyle='dotted',
             label="Average fantasy points total per League Team")
    plt.legend()
    plt.show()


#  Graph total player costs per team
def graphTotalSquadCost(players, teams):
    TotalSquads = getSquadCostbyTeam(players, teams)
        # dict(sorted(getSquadCostbyTeam(players, teams).items(), key=lambda item: item[1], reverse=True))

    x = list(TotalSquads.keys())  # retrieving team shortnames as x values

    averageCost = sum(TotalSquads.values()) / 20  # Average total player fantasy points per team
    # TotalSquads = sorted(TotalSquads)
    str_ = "Average fantasy player cost per League Team ({0})".format(averageCost)
    plt.bar(x, TotalSquads.values(), label="Total Squad Cost", color="Orange", width=-0.3, align="edge")
    plt.plot(x, [averageCost] * len(x), color='orange', linestyle='dotted', label=str_)
    plt.legend()
    plt.show()


async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()
        teams = await fpl.get_teams()
        total = 0
        count = 0
        for player in getPlayersByTeam(players, teams)['MCI']:
            print(player.web_name, end=', ')
            print(player.now_cost/10)
            total += player.now_cost/10
            count += 1
        print(total, end=', ')
        print(count, end=', ')
        print(len(getPlayersByTeam(players, teams)['MCI']))


asyncio.run(main())
