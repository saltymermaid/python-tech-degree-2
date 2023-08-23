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
    smallest_size = min(team['size'] for team in teams)
    smallest_team = [team for team in teams if team['size'] == smallest_size][0]
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


def print_team_stats(team):
    """Print the team stats"""
    print()
    team_head = "Team " + team['name'] + " Stats"
    print("-" * len(team_head))
    print(team_head)
    print("-" * len(team_head))
    print(f"Total players: {team['size']}")
    print(f"Average height: {avg_height(team)} inches\n")
    print("Players on Team:")
    players_list = [player['name'] for player in team['players']]
    players_str = ", ".join(players_list)
    print(players_str)
    print()
    print("Guardians:")
    guardians_list = [guardian for player in team['players'] for guardian in player['guardians']]
    guardians_str = ", ".join(guardians_list)
    print(guardians_str)


def avg_height(team):
    """Calculate the average height of a team"""
    total_height = sum([player['height'] for player in team['players']])
    avg_height = total_height / team['size']
    avg_height = round(avg_height, 1)
    return avg_height


def print_header():
    """Print the header"""
    print()
    print("*" * 30)
    print("BASKETBALL TEAM STATS TOOL\n")


def print_menu():
    """Print the menu"""
    print()
    print("---- MENU ----\n")
    print("A) Display Team Stats")
    print("B) Quit\n")


def choose_team(teams):
    for index, team in enumerate(teams, 1):
        print(f"{index}) Display Team {team['name']} Stats")
    choice = input("Pick a team > ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(teams):
            raise ValueError
    except ValueError:
        print("Please enter a valid option")
        return choose_team(teams)
    else:
        return teams[choice - 1]


def menu(teams):
    """Run the menu"""
    player_stats = True
    while player_stats:
        print_menu()
        user_choice = input("Enter an option > ")
        if user_choice.upper() == 'A':
            selected_team = choose_team(teams)
            print_team_stats(selected_team)
            print()
            print("*" * 30)
        elif user_choice.upper() == 'B':
            player_stats = False
        else:
            print("Please enter a valid option")


if __name__ == "__main__":
    players = clean_data()
    team_names = copy.deepcopy(constants.TEAMS)
    assigned_teams = balance_teams(team_names, players)
    print_header()
    menu(assigned_teams)
