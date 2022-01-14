import aiohttp
import asyncio
from prettytable import PrettyTable
from fpl import FPL
from matplotlib import pyplot as plt
import operator
#  Modified method to test FPL API
#  Sorts by best in position. element_type = 1=GK, 2=DEF, 3=MID, 4=FOR
#
def most_val(number, players):
    top_performers = sorted(
        players, key=lambda x: float(x.points_per_game)#(x.pp90-2)/(x.now_cost/10)
        if (x.minutes > 90 * 4 and
         x.element_type == 3
        and x.status == "a")
        #and x.total_points > 100)
        else 0.0,
        reverse=True)
    #  Outputs in Table form
    player_table = PrettyTable()
    player_table.field_names = ["Player", "£", "G", "A", "CS", "Pts per game", "VAPM","Total Points", "Games played"]
    player_table.align["Player"] = "l"
    for player in top_performers[:number]:
        goals = player.goals_scored
        assists = player.assists

        #  PrettyTable formatting
    player_table.add_row([player.web_name, f"£{player.now_cost / 10}",
                          goals, assists, player.clean_sheets, player.points_per_game,
                          '{0:.2f}'.format((player.pp90-2)/(player.now_cost/10)), player.total_points,
                          "{0:.2f}".format(player.minutes/90)
                          ])
    print(player_table)

def getMidfielders(players):
    mid = []
    for player in players:
        if player.element_type == 3:
            mid.append(player)
    return mid

def getForwards(players):
    fw = []
    for player in players:
        if player.element_type == 4:
            fw.append(player)
    return fw

def getDefenders(players):
    defs = []
    for player in players:
        if player.element_type == 2:
            defs.append(player)
    return defs

def getGoalies(players):
    gk = []
    for player in players:
        if player.element_type == 1:
            gk.append(player)
    return gk
#  Returns all League teams as Dict
def getAllTeams(teams):
    TeamData = {}
    for team in teams:
        TeamData[team.id] = [team.name, team.short_name,  team.points, team.id]

    return TeamData

#  Returns All players grouped by teams in a dict
#  Key = team's short name, Value = List of players
def getPlayersbyTeam(players, teams):
    AllTeams = getAllTeams(teams) 
    teamPlayers = {}
    # create empty list for all teams
    for team in AllTeams:
        teamPlayers[team] = []

    for player in players:
        if player.team == AllTeams[player.team][3]:
            teamPlayers[AllTeams[player.team][1]].append(player)
    return teamPlayers

#  Returns Total cost of players grouped by team as dict
#  Player costs are in tens instead of digits
#  To change to digits, teamCosts[AllTeams[player.team][1]] += player.now_cost/10
#  Key = team's short name, Value = List of players
def getSquadCostbyTeam(players, teams):
    AllTeams = getAllTeams(teams)
    teamCosts = {}

    for team in AllTeams:
        teamCosts[AllTeams[team][1]] = 0

    for player in players:
        if player.team == AllTeams[player.team][3]:
            teamCosts[AllTeams[player.team][1]] += player.now_cost
    return teamCosts

#  Returns total points accumulated by players per team as dict
#  Key = team's short name, Value = List of players
def getPlayerPtsPerTeam(players, team):
    playerPtsPerTeam = {}
    teams = getAllTeams(team)
    for player in players:
        if player.team == teams[player.team][3]:
            if teams[player.team][1] not in playerPtsPerTeam:
                playerPtsPerTeam[teams[player.team][1]] = player.total_points
            playerPtsPerTeam[teams[player.team][1]] += player.total_points
    return playerPtsPerTeam

#  Graph total player fantasy points per team
def graphPlayerPointsPerTeam(players, teams):
    data = dict(sorted(getPlayerPtsPerTeam(players, teams).items(), key=operator.itemgetter(1), reverse=True))
    lst = list(data.keys())
    keys = list(data.keys())
    values = list(data.values())
    y = sum(list(data.values()))/20  # Average total player fantasy points per team

    plt.bar(keys, values)
    plt.plot(keys, [y]*len(values), color='red', linestyle='dotted', label="Average fantasy points total per League Team")
    plt.legend()
    plt.show()

#  Graph total player costs per team
def graphTotalSquadCostvsTotalPoints(players, teams):
    TotalPoints = dict(sorted(getPlayerPtsPerTeam(players, teams).items(), key=operator.itemgetter(1), reverse=True))
    TotalSquads = getSquadCostbyTeam(players, teams)

    x = list(TotalPoints.keys())
    points = list(TotalPoints.values())
    reArranged = []
    i = 0
    # Loop rearranges sequence of totalSquads values to fit
    # TotalPoints sequence
    for cost in range(len(points)):
        if x[i] in list(TotalSquads.keys()):
            reArranged.append(TotalSquads[x[i]])
        i+=1

    averagePoints = sum(points)/20  # Average total player cost per team
    averageCost = sum(reArranged)/20  # Average total player fantasy points per team
    str1 = "Average fantasy points total per League Team ({0})".format(averagePoints)
    str2 = "Average fantasy cost per League Team ({0})".format(averageCost)
    plt.bar(x, points, label="Total Fantasy Points per Team", color="blue", width=0.3, align="edge")
    plt.bar(x, reArranged, label="Total Squad Cost", color="Orange", width=-0.3, align="edge")
    plt.plot(x, [averagePoints] * len(x), color='blue', linestyle='dotted', label=str1)
    plt.plot(x, [averageCost] * len(x),  color='orange', linestyle='dotted', label=str2)
    plt.legend()
    plt.show()

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()
        teams = await fpl.get_teams()
        graphTotalSquadCostvsTotalPoints(players, teams)




asyncio.run(main())