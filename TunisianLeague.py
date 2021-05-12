from bs4 import BeautifulSoup
import os
import requests


class Team:
    def __init__(self, pos, team_name, matches_played, wins, draws,
                 losses, goals_for, goals_against, goal_diff, pts, last_five):
        self.pos = pos
        self.team_name = team_name
        self.matches_played = matches_played
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goal_diff = goal_diff
        self.pts = pts
        self.last_five = last_five


# gets a lists and adds spaces to all elements to make them equal in len
def list_formatter(content):
    # convert the list elements to string
    for list_index in range(len(content)):
        content[list_index] = str(content[list_index])

    max_str = len(content[0])
    # find the longest str in the list
    for list_index in range(1, len(content)):
        if len(content[list_index]) > max_str:
            max_str = len(content[list_index])

    # add spaces to all the list elements to make them all equal in len
    for list_index in range(0, len(content)):
        if len(content[list_index]) < max_str:
            content[list_index] += ' ' * (max_str - len(content[list_index]))


def main():
    os.system('cls')

    link = 'https://www.lequipe.fr/Football/championnat-de' \
           '-tunisie/page-classement-equipes/general'

    page = requests.get(link)

    source = page.content

    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('tbody')

    tr = table.find_all('tr')

    standings = []

    for info in tr:
        standings.append(info.find_all('td', class_='table__col'))

    for i in range(len(standings)):
        for x in range(len(standings[i]) - 1):
            standings[i][x] = standings[i][x].text.strip()

    for i in range(len(standings)):
        div = standings[i][-1].find_all('div')
        res = ''
        for x in div:
            content = str(x)
            if content.find('red') != -1:
                res += 'L'
            elif content.find('green') != -1:
                res += 'W'
            else:
                res += 'D'
            del standings[i][-1]
            standings[i].append(res)

    for ind in range(len(standings)):
        del standings[ind][2]

    print(standings)

    info = ['#', 'Pts', 'Pl', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Team', 'Last 6']
    pos = []
    team_name = []
    matches_played = []
    wins = []
    draws = []
    losses = []
    goals_for = []
    goals_against = []
    goal_diff = []
    pts = []
    last_five = []

    # converting the 'standings' list to multiple lists
    for index in standings:
        pos.append(index[0])
        team_name.append(index[1])
        matches_played.append(index[2])
        wins.append(index[3])
        draws.append(index[4])
        losses.append(index[5])
        goals_for.append(index[6])
        goals_against.append(index[7])
        goal_diff.append(index[8])
        pts.append(index[9])
        last_five.append(index[10])

    list_formatter(info)
    list_formatter(pos)
    list_formatter(team_name)
    list_formatter(matches_played)
    list_formatter(wins)
    list_formatter(draws)
    list_formatter(losses)
    list_formatter(goals_for)
    list_formatter(goals_against)
    list_formatter(goal_diff)
    list_formatter(pts)

    print(*info, sep='/')

    final_output = ''
    output_len = 0  # init made to avoid pycharm warning
    for ind in range(len(pos)):
        output = f"|  {pos[ind]} ) {team_name[ind]} | {matches_played[ind]} | {wins[ind]} | {draws[ind]} | " \
                 f"{losses[ind]} | {goals_for[ind]} | {goals_against[ind]} | {goal_diff[ind]} | {pts[ind]}" \
                 f" | {last_five[ind]} |"

        output_len = len(output)
        final_output += '\n' + ('-' * output_len)
        final_output += '\n' + output
    final_output += '\n' + ('-' * output_len)

    print(final_output)

    # storing the data in a class to manipulate them easier in case we needed them in the future
    data = []
    ind = 0
    for index in standings:
        team = Team(index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8],
                    index[9], index[10])
        data.append(team)
        ind += 1

    # print(data[8].team_name)

main()