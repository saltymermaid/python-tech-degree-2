import copy
import constants

DISPLAY_WIDTH = 36

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


def pick_best_team(teams, experienced, max_players_per_team):
    """Pick one of the smallest teams"""
    # exclude teams that are full
    candidate_teams = [team for team in teams if team['size'] < max_players_per_team]
    # find the smallest team with the right experience
    if experienced:
        smallest_size = min(team['num_experienced'] for team in candidate_teams)
        smallest_team = [team for team in candidate_teams if team['num_experienced'] == smallest_size][0]
    else:
        smallest_size = min(team['num_inexperienced'] for team in candidate_teams)
        smallest_team = [team for team in candidate_teams if team['num_inexperienced'] == smallest_size][0]
    return smallest_team


def create_and_balance_teams(team_names, players):
    """Assign players to teams evenly"""
    teams = [{'name': name, 'size': 0, 'num_experienced': 0, 'num_inexperienced': 0, 'players': []} for name in team_names]
    max_players_per_team = len(players) / len(teams)
    for player in players:
        experienced = player['experience']
        selected_team = pick_best_team(teams, experienced, max_players_per_team)
        selected_team['players'].append(player)
        selected_team['size'] += 1
        # increment the experienced or inexperienced count
        if experienced:
            selected_team['num_experienced'] += 1
        else:
            selected_team['num_inexperienced'] += 1
    return teams


def player_display_name(player):
    """Display the player name with (exp) if they are experienced"""
    player_exp = player['experience']
    if player_exp == True:
        return player['name'] + " (exp)"
    else:
        return player['name']


def avg_height(team):
    """Calculate the average height of a team"""
    total_height = sum([player['height'] for player in team['players']])
    avg_height = total_height / team['size']
    avg_height = round(avg_height, 1)
    return avg_height


def print_header():
    """Print the header"""
    print()
    print("*" * DISPLAY_WIDTH)
    print("* " + "BASKETBALL TEAM STATS TOOL".center(DISPLAY_WIDTH - 4, ' ') + " *")


def print_menu():
    """Print the menu"""
    print("*" + ' ' * (DISPLAY_WIDTH - 2) + "*")
    print("* " + " MENU ".center(DISPLAY_WIDTH - 4, '-') + " *")
    print("*" + ' ' * (DISPLAY_WIDTH - 2) + "*")
    print("* (S) Display Team Stats" + ' ' * (DISPLAY_WIDTH - 25) + '*')
    print("* (X) Exit" + ' ' * (DISPLAY_WIDTH - 11) + '*')
    print("*" * DISPLAY_WIDTH)
    print()


def print_team_choice_menu(teams):
    print()
    print("*" * 36)
    print("* " + "DISPLAY STATS".center(DISPLAY_WIDTH - 4, ' ') + " *")
    print("*" + ' ' * (DISPLAY_WIDTH - 2) + "*")
    print("* " + " TEAMS ".center(DISPLAY_WIDTH - 4, '-') + " *")
    print("*" + ' ' * (DISPLAY_WIDTH - 2) + "*")
    for index, team in enumerate(teams, 1):
        team_name_prompt = "(" + str(index) + ") " + team['name']
        print("* " + team_name_prompt + ' ' * (DISPLAY_WIDTH - len(team_name_prompt) - 3) + "*")
    print("*" + ' ' * (DISPLAY_WIDTH - 2) + "*")
    print("*" * 36)
    print()


def print_team_stats(team):
    """Print the team stats"""
    print()
    team_head = "Team " + team['name'] + " Stats"
    print("-" * DISPLAY_WIDTH)
    print(team_head.center(DISPLAY_WIDTH, ' '))
    print("-" * DISPLAY_WIDTH)
    print(f"Total players:   {team['size']}")
    print(f"  Experienced:   {team['num_experienced']}")
    print(f"  Inexperienced: {team['num_inexperienced']}")
    print(f"Average Height:  {avg_height(team)} inches")
    players_list = [player_display_name(player) for player in team['players']]
    players_str = ", ".join(players_list)
    print(f"Players on Team: {players_str}")
    guardians_list = [guardian for player in team['players'] for guardian in player['guardians']]
    guardians_str = ", ".join(guardians_list)
    print(f"Guardians:       {guardians_str}")
    print("-" * DISPLAY_WIDTH)
    print()
    print("-" * DISPLAY_WIDTH)


def choose_team(teams):
    """Get team choice from user and validate"""
    print_team_choice_menu(teams)
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
        if user_choice.upper() == 'S':
            selected_team = choose_team(teams)
            print_team_stats(selected_team)
            print()
        elif user_choice.upper() == 'X':
            player_stats = False
        else:
            print("Please enter a valid option")
        print("*" * DISPLAY_WIDTH)


if __name__ == "__main__":
    players = clean_data()
    team_names = copy.deepcopy(constants.TEAMS)
    assigned_teams = create_and_balance_teams(team_names, players)
    print_header()
    menu(assigned_teams)
