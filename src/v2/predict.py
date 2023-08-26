import json


def load_players_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def calculate_combined_score(player, value_weight=0.4, team_weight=0.3, bps_weight=0.2, selected_weight=0.1):
    value_score = float(player.get('value_season', 0)) * value_weight
    # team_score = player.get('team', 0) * team_weight
    bps_score = float(player.get('bps', 0.0)) * bps_weight
    selected_score = float(player.get('selected_by_percent', 0)) * selected_weight

    return value_score + bps_score + selected_score


def predict_best_players(players_data, num_players=15):
    sorted_players = sorted(players_data, key=lambda x: calculate_combined_score(x), reverse=True)
    return sorted_players[:num_players]


if __name__ == '__main__':
    players_data = load_players_data('data/players_data.json')

    if players_data:
        best_players = predict_best_players(players_data, num_players=15)

        print("Predicted Best 15 Players:")
        for idx, player in enumerate(best_players, 1):
            print(f"{idx}. {player['web_name']} (Team: {player['team']}, Combined Score: {calculate_combined_score(player)})")
