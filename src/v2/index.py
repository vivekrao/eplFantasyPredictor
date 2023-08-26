import requests
import json


def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def save_players_data(players_data):
    with open('data/players_data.json', 'w') as f:
        json.dump(players_data, f)


def save_teams_data(teams_data):
    with open('data/teams_data.json', 'w') as f:
        json.dump(teams_data, f)


def add_useful_fields(players_data, teams_data, players_type_data):
    # print(players_type_data['id'])
    for player in players_data:
        # player['position'] = players_type_data[player['id']]['singular_name_short']
        res = [obj for obj in players_type_data if players_type_data['id'] == int(player.get('element_type'))][0]
        print(res)


if __name__ == '__main__':
    api_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    # Fetch data from the URL
    data = get_data_from_url(api_url)

    if data:
        # Extract players' data
        players_data = data.get('elements', [])

        # Extract teams' data
        teams_data = data.get('teams', [])

        # Extract players' type data
        players_type_data = data.get('element_types', [])

        # Massage players data
        add_useful_fields(players_data, teams_data, players_type_data)

        # Save the data to JSON files
        save_players_data(players_data)
        save_teams_data(teams_data)

        print("Players' data and teams' data have been saved successfully.")
