import json


def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def calculate_weighted_average(player, teams_data, weights):
    total_weighted_sum = 0
    for attribute, weight in weights.items():
        total_weighted_sum += float(player.get(attribute, 0)) * weight
    team_id = player.get('team', 0)
    team_strengths = next((team['strength'], team['strength_overall_home'], team['strength_overall_away'], team[
        'strength_attack_home'], team['strength_attack_away'], team['strength_defence_home'], team[
        'strength_defence_away'] for team in teams_data if team['id'] == team_id), 0)

    team_strength = team_strengths[0]
    if player.get('position') == 'DEF' or player.get('position') == 'GKP':
        team_strength = team_strengths[0] + (team_strengths[5] + team_strengths[6]) / 2
    elif player.get('position') == 'FWD':
        team_strength = team_strengths[0] + (team_strengths[3] + team_strengths[4]) / 2
    else:
        team_strength = team_strengths[0] + (team_strengths[1] + team_strengths[2]) / 2
    total_weighted_sum += team_strength * weights.get('team_strength', 0)
    return total_weighted_sum


def sort_best_players(players_data, teams_data, weights):
    sorted_players = sorted(players_data, key=lambda x: calculate_weighted_average(x, teams_data, weights), reverse=True)
    return sorted_players


if __name__ == '__main__':
    players_data = load_data('data/players_data.json')
    teams_data = load_data('data/teams_data.json')

    if players_data and teams_data:
        weights = {
            'value': 0.4,
            'bps': 0.3,
            'selected_by_percent': 0.3,
            'team_strength': 0.2,  # Additional weight for team strength (Optional)
        }

        sorted_players = sort_best_players(players_data, teams_data, weights)

        print("Best Players sorted by Weighted Average:")
        for idx, player in enumerate(sorted_players, 1):
            weighted_average = calculate_weighted_average(player, teams_data, weights)
            team_name = next((team['name'] for team in teams_data if team['id'] == player['team']), "")
            print(f"{idx}. {player['web_name']} (Team: {team_name}, Weighted Average: {weighted_average:.2f})")
