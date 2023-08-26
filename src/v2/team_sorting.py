import json


def load_teams_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def calculate_weighted_average(team, weights):
    total_weighted_sum = 0
    for attribute, weight in weights.items():
        total_weighted_sum += team.get(attribute, 0) * weight
    return total_weighted_sum


def sort_teams_by_weighted_average(teams_data, weights):
    sorted_teams = sorted(teams_data, key=lambda x: calculate_weighted_average(x, weights), reverse=True)
    return sorted_teams


if __name__ == '__main__':
    teams_data = load_teams_data('data/teams_data.json')

    if teams_data:
        weights = {
            'strength': 0.15,
            'strength_overall_home': 0.15,
            'strength_overall_away': 0.1,
            'strength_attack_home': 0.1,
            'strength_attack_away': 0.15,
            'strength_defence_home': 0.15,
            'strength_defence_away': 0.1,
        }

        sorted_teams = sort_teams_by_weighted_average(teams_data, weights)

        print("Teams sorted by Weighted Average:")
        for idx, team in enumerate(sorted_teams, 1):
            weighted_average = calculate_weighted_average(team, weights)
            print(f"{idx}. {team['name']} (Weighted Average: {weighted_average:.2f})")
