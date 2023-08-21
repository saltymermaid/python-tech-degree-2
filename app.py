import copy
import constants
import pdb

def clean_data():
    """Import a copy and clean the data"""
    dirty_data = copy.deepcopy(constants.PLAYERS)
    cd = []
    for player in dirty_data:
        player['height'] = convert_height(player['height'])
        player['experience'] = convert_experience(player['experience'])
        player['guardians'] = convert_guardians(player['guardians'])
        cd.append(player)
    return cd


def convert_height(height_str):
    """Convert the height to an integer"""
    height_in_inches = int(height_str.split()[0])
    return height_in_inches


def convert_experience(experience_str):
    """Convert the experience to a boolean"""
    if experience_str == 'YES':
        experience = True
    else:
        experience = False
    return experience


def convert_guardians(guardians_str):
    """Convert the guardians to a list"""
    guardians = guardians_str.split(' and ')
    return guardians


def pick_smallest_team(teams):
    """Pick one of the smallest teams"""
    team_dict = {team['name']: len(team['players']) for team in teams}
    smallest_size = min(team_dict.values())
    smallest_team_name = [key for (key, value) in team_dict.items() if value == smallest_size][0]
    smallest_team = [team for team in teams if team['name'] == smallest_team_name][0]
    return smallest_team


def balance_teams(team_names, players):
    """Assign players to teams evenly"""
    num_players_per_team = len(players) / len(team_names)
    teams = [{'name': name, 'size': 0, 'players': []} for name in team_names]
    for player in players:
        selected_team = pick_smallest_team(teams)
        selected_team['players'].append(player)
        selected_team['size'] += 1
    return teams


if __name__ == "__main__":
    players = clean_data()
    team_names = copy.deepcopy(constants.TEAMS)
    assigned_teams = balance_teams(team_names, players)
    player_stats = True
    print("BASKETBALL TEAM STATS TOOL\n")
    print("---- MENU ----\n")
    while player_stats:
        user_choice = input("Menu:\n A) Display Team Stats\n B) Quit\n\nEnter an option > ")
        if user_choice.upper() == 'A':
            for team in assigned_teams:
                print(team)
        elif user_choice.upper() == 'B':
            player_stats = False
        else:
            print("Please enter a valid option")
