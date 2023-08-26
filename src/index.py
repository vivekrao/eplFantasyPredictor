import requests
import pandas as pd
import numpy as np
import time

from src import predict

DESIRED_WIDTH = 320

pd.set_option('display.width', DESIRED_WIDTH)
np.set_printoptions(linewidth=DESIRED_WIDTH)
pd.set_option('display.max_columns', 10)

FANTASY_BASE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

max_value_season = 0.000
max_minutes = 0.000
max_bps = 0.000
max_selected = 0.000

value_weightage = 5
bps_weightage = 4
minutes_weightage = 2
selected_weightage = 1
team_weightage = 3


import requests
import json


def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from the API. Status code: {response.status_code}")


def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    data = fetch_data_from_api(FANTASY_BASE_URL)

    if data:
        filename = "premier_league_data.json"
        save_data_to_file(data, filename)
        print(f"Data has been successfully saved to {filename}.")


def get_base_data():
    req = requests.get(FANTASY_BASE_URL)
    json = req.json()

    print(json.keys())
    return json


def build_basic_dataframe(json):
    elements_df = pd.DataFrame(json['elements'])
    elements_types_df = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])

    # print(elements_df.head())
    # print(elements_df.columns)
    # print(elements_types_df.head())
    # print(elements_types_df.columns)
    # print(teams_df.head())
    # print(teams_df.columns)

    slim_elements_df = elements_df[
        ['id', 'element_type', 'points_per_game', 'selected_by_percent', 'team_code', 'team', 'status', 'transfers_in',
         'transfers_out', 'value_form', 'value_season', 'minutes', 'goals_scored', 'assists', 'clean_sheets',
         'goals_conceded', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps',
         'expected_goals_conceded', 'expected_goals_per_90', 'saves_per_90', 'expected_assists_per_90',
         'expected_goal_involvements_per_90', 'expected_goals_conceded_per_90', 'goals_conceded_per_90', 'now_cost',
         'first_name', 'second_name', 'total_points']]
    slim_elements_df.set_index(['id'])

    print(slim_elements_df.head())

    return elements_df, elements_types_df, teams_df, slim_elements_df


def refine_input_data(base_data):
    players_df, players_types_df, teams_details_df, slim_players_df = build_basic_dataframe(base_data)

    final_players_df = slim_players_df.copy()
    final_players_df['position'] = slim_players_df.element_type.map(players_types_df.set_index('id').singular_name)
    final_players_df['position_short'] = slim_players_df.element_type.map(
        players_types_df.set_index('id').singular_name_short)

    final_players_df['team_name'] = slim_players_df.team.map(teams_details_df.set_index('id').name)

    final_players_df['value_season'] = slim_players_df.value_season.astype(float)
    final_players_df['minutes'] = slim_players_df.minutes.astype(float)
    final_players_df['bps'] = slim_players_df.bps.astype(float)
    final_players_df['selected_by_percent'] = slim_players_df.selected_by_percent.astype(float)

    # print(final_players_df.head())
    return final_players_df.sort_values('value_season', ascending=False)


def pivot_input_data(refined_data):
    refined_data = refined_data.loc[refined_data.value > 0]
    refined_data.pivot_table(index='position', values='value', aggfunc=np.mean).reset_index()
    pivot = refined_data.pivot_table(index='position', values='value', aggfunc=np.mean).reset_index()
    return pivot.sort_values('value', ascending=False)


def team_pivot_input_data(refined_data):
    team_pivot = refined_data.pivot_table(index='team_name', values='value', aggfunc=np.mean).reset_index()
    return team_pivot.sort_values('value',ascending=False)


def get_histogram_data(refined_data):
    fwd_df = refined_data.loc[refined_data.position == 'Forward']

    mid_df = refined_data.loc[refined_data.position == 'Midfielder']

    def_df = refined_data.loc[refined_data.position == 'Defender']

    goal_df = refined_data.loc[refined_data.position == 'Goalkeeper']

    print(goal_df.head(20))
    print(def_df.head(20))
    print(mid_df.head(20))
    print(fwd_df.head(20))

    return fwd_df, mid_df, def_df, goal_df


def copy_data_to_csv(all_data, fwd_data, mid_data, def_data, gk_data):
    all_data.to_csv('~/home/epl_fantasy_data/all_data.csv')
    fwd_data.to_csv('~/home/epl_fantasy_data/fwd_data.csv')
    mid_data.to_csv('~/home/epl_fantasy_data/mid_data.csv')
    def_data.to_csv('~/home/epl_fantasy_data/def_data.csv')
    gk_data.to_csv('~/home/epl_fantasy_data/gk_data.csv')


def get_common_attributes():
    return ['element_type', 'points_per_game', 'selected_by_percent', 'team_code', 'team', 'status', 'total_points',
            'transfers_in', 'transfers_out', 'value_form', 'value_season', 'minutes', 'goals_scored', 'assists',
            'yellow_cards', 'red_cards', 'bonus', 'bps', 'now_cost']


def get_def_attributes():
    return ['clean_sheets', 'goals_conceded', 'penalties_saved', 'penalties_missed', 'saves_per_90',
            'expected_goals_conceded', 'expected_goals_conceded_per_90', 'goals_conceded_per_90']


def get_mid_attributes():
    return ['clean_sheets', 'penalties_missed', 'expected_goals_per_90', 'expected_assists_per_90',
            'expected_goal_involvements_per_90']


def get_gk_attributes():
    return ['clean_sheets', 'goals_conceded', 'penalties_saved', 'penalties_missed', 'saves_per_90',
            'expected_goals_conceded', 'expected_goals_conceded_per_90', 'goals_conceded_per_90']


def get_fwd_attributes():
    return ['penalties_missed', 'expected_goals_per_90', 'expected_assists_per_90', 'expected_goal_involvements_per_90']


def set_max_attributes(refined_data):
    max_values = refined_data.max()
    global max_value_season, max_minutes, max_bps, max_selected

    max_value_season = max_values['value_season']
    max_minutes = max_values['minutes']
    max_bps = max_values['bps']
    max_selected = max_values['selected_by_percent']

    print(max_value_season, max_minutes, max_bps, max_selected)


def get_team_value(player):

    return 0


def get_value_for_element(player):
    # First find out what kind of player it is
    player_type = player['position_short']

    value = (player['value_season'] / max_value_season) * value_weightage + (
                player['minutes'] / max_minutes) * minutes_weightage + (player['bps'] / max_bps) * bps_weightage + (
                        player['selected_by_percent'] / max_selected) * selected_weightage


    # Potentially here we can add more criteria for specific positions

    return value


def create_selection_criteria_value(refined_data):

    selection_criteria_values = []
    for index, row in refined_data.iterrows():
        selection_criteria_values.append(get_value_for_element(row))

    refined_data['selection_criteria_value'] = selection_criteria_values


'''
    Prediction process that we follow
    Assign a max amount for each section: GK - 10, DEF - 28, MID - 35, FWD - 27
    Pick cheapest FWD, cheapest GK, cheapest DEF and cheapest MID 
    then choose best gk
    then choose 3 defenders
    then 2 midfielders
    then 1 forward
    After that choose the next 
'''


# Returns true if this type of player can be added
def is_valid_player(player, def_count, gk_count, mid_count, fwd_count):
    if player['position_short'] == 'DEF':
        return def_count < 5
    elif player['position_short'] == 'GK':
        return gk_count < 2
    elif player['position_short'] == 'MID':
        return mid_count < 5
    return fwd_count < 3


def main():
    base_data = get_base_data()
    refined_data = refine_input_data(base_data)
    set_max_attributes(refined_data)
    # pivot_data = pivot_input_data(refined_data)
    # print(pivot_data)
    # team_pivot_data = team_pivot_input_data(refined_data)
    # print(team_pivot_data)

    # Use the data above to add a new column of selection_criteria_value
    create_selection_criteria_value(refined_data)

    refined_data = refined_data.sort_values('selection_criteria_value', ascending=False)
    print('refined data: ', refined_data.head(1).index)

    # histogram
    fwd_refined_data, mid_refined_data, def_refined_data, gk_refined_data = get_histogram_data(refined_data)

    # Copy it to csv
    # copy_data_to_csv(refined_data, fwd_refined_data, mid_refined_data, def_refined_data, gk_refined_data)

    # Predict all 15 players with standard restrictions
    predicted_players = predict.predict_full_team(refined_data, fwd_refined_data, mid_refined_data, def_refined_data,
                                          gk_refined_data)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
