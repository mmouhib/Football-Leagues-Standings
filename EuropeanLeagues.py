from bs4 import BeautifulSoup
import os
import requests

os.system('cls')


class Team:
    def __init__(self, pos, team_name, matches_played, wins, draws,
                 losses, goals_for, goals_against, goal_diff, pts, last_five, last_five_details):
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
        self.last_five_details = last_five_details


def table_formatter(content):
    temp_content = ''
    max_len = content[0][1]
    for ctx in content:
        if len(ctx[1]) > len(max_len):
            max_len = ctx[1]

    for ctx in content:
        for sub_data in ctx:
            temp_content += sub_data
            for _ in range(len(max_len)):
                temp_content += ' '
        temp_content += '\n'
    return temp_content


def url_def(country):
    if country == 'spain':
        return 'https://www.skysports.com/la-liga-table'
    elif country == 'germany':
        return 'https://www.skysports.com/bundesliga-table'
    elif country == 'england':
        return 'https://www.skysports.com/premier-league-table'
    elif country == 'italy':
        return 'https://www.skysports.com/serie-a-table'
    elif country == 'france':
        return 'https://www.skysports.com/ligue-1-table'
    elif country == 'netherlands':
        return 'https://www.skysports.com/eredivisie-table'


def result_parser(result):
    pos_one = 0  # this init is just for the PEP warning in pycharm
    for position in range(len(result)):
        if result[position].isdigit():
            pos_one = position
            break
    team_one = result[:pos_one - 1]
    team_one_score = result[pos_one]
    team_two_score = result[pos_one + 2]
    team_two = result[pos_one + 4:]
    if team_one_score > team_two_score:
        return team_one
    elif team_one_score < team_two_score:
        return team_two
    return 'draw'


def last_six(content, club):
    match_res = ''
    for element in content:
        fn = result_parser(element)
        if fn == club:
            match_res += 'W'
        elif fn == 'draw':
            match_res += 'D'
        else:
            match_res += 'L'
    return match_res


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
    league = 'spain'

    link = url_def(league)

    page = requests.get(link)

    source = page.content

    soup = BeautifulSoup(source, 'lxml')

    # recover the one and only tbody in the page
    table = soup.find('table')

    # recover the one and only tbody in the page
    tbody = table.find('tbody')

    # recover all TRs
    tr = tbody.find_all('tr')

    last_six_record = []
    standings = []  # list that contains all stats
    spans = []  # contains the last six matches results

    # looping through every TR tag (every tr contains the infos about a team)
    for squad_info in tr:
        # storing all the data for each team (position, wins, draws..):
        td = squad_info.find_all('td')
        standings.append(td)
        # remove extra spaces and extra characters from the data:
        for i in range(len(td)):
            td[i] = td[i].text.strip()
        # storing the last 6 games data:
        spans.append(squad_info.find_all('span', class_='standing-table__form-cell'))

    for x in spans:
        span2 = []
        for i in x:
            span2.append(i['title'])
        last_six_record.append(span2)

    # deleting the last element from 'standings' list c=because it is empty
    for i in range(len(standings)):
        del standings[i][-1]

    # print(*last_six_record, sep='\n\n')

    ind = 0
    for stats in last_six_record:
        res = last_six(stats, standings[ind][1])
        res = res[::-1]
        standings[ind].append(res)
        ind += 1

    # adds extra space to the first element of each club list that is < 10 to make them all equal
    for index in range(len(standings)):
        if int(standings[index][0]) < 10:
            standings[index][0] += ' '

    info = ['#', 'Team', 'Pl', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', 'Last 6']
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

    # with open("res.txt", "w") as file:
    #     file.write(final_output)

    # storing the data in a class to manipulate them easier in case we needed them in the future
    data = []
    ind = 0
    for index in standings:
        team = Team(index[0], index[1], index[2], index[3], index[4], index[5], index[6],
                    index[7], index[8], index[9], index[10], last_six_record[ind])

        data.append(team)
        ind += 1

    # print(data[0].last_five_details)


main()
