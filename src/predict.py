import pandas as pd

team_counts = {}
total_count = 0

total_cost = 0

def_count = 0
gk_count = 0
mid_count = 0
fwd_count = 0


def update_player_count(player_type, count):
    global def_count, gk_count, mid_count, fwd_count, total_count, total_cost, team_counts
    if player_type == 'DEF':
        if count > 0 and def_count >= 5:
            return False
        def_count = def_count + count
    elif player_type == 'GKP':
        if count > 0 and gk_count >= 2:
            return False
        gk_count = gk_count + count
    elif player_type == 'MID':
        if count > 0 and mid_count >= 5:
            return False
        mid_count = mid_count + count
    else:
        if count > 0 and fwd_count >= 3:
            return False
        fwd_count = fwd_count + count

    total_count = total_count + count
    return True


def edit_team(all_remaining_players, result_players, num_players_to_edit):
    # Remove players from the list and replace them with the highest ranked player who fits the budget
    # first remove the number of players to edit
    removed_players = []
    removed_player_types = []
    global def_count, gk_count, mid_count, fwd_count, total_count, total_cost

    for i in range(num_players_to_edit):
        temp = all_remaining_players.pop()
        player_type = temp['position_short']
        removed_players.append(temp)
        removed_player_types.append(player_type)
        update_player_count(player_type, -1)
        total_cost = total_cost - temp['now_cost']

    # if cost is still over 100 exit early
    if total_cost > 100:
        # add all the players back

        return False





def add_players(all_remaining_players, result_players, result_ids):

    global def_count, gk_count, mid_count, fwd_count, total_count, total_cost, team_counts
    for index, player in all_remaining_players.iterrows():
        if player['id'] in result_ids:
            continue
        player_type = player['position_short']
        player_team = player['team_name']

        # Check for team limits
        if not team_counts.get(player_team):
            team_counts[player_team] = 0
        elif team_counts[player_team] == 3:
            continue

        # Update the player count - if unable to then skip
        if not update_player_count(player_type, 1):
            continue

        team_counts[player_team] += 1

        # Now add the player to the list
        result_players.append(player)
        result_ids.add(player['id'])
        total_cost += player['now_cost']

        total_count = total_count + 1
        if total_count == 15:
            break

    res_df = pd.DataFrame(result_players)
    print(res_df)
    print(total_cost)


def predict_full_team(all_data, fwd_data, mid_data, def_data, gk_data):
    all_remaining_players = all_data.copy()
    max_values_row = all_remaining_players.max()
    min_values_row = all_remaining_players.min()

    # We can potentially get this from the user as well
    result_players = []
    result_ids = set()

    global def_count, gk_count, mid_count, fwd_count, total_count, total_cost, team_counts

    add_players(all_remaining_players, result_players, result_ids)

    num_players_to_edit = 1
    final_players = []
    # while total_cost > 100 or num_players_to_edit > 10:
    #     final_players, total_cost = edit_team(all_remaining_players, result_players, num_players_to_edit)
    #     num_players_to_edit += 1

    res_df = pd.DataFrame(final_players)
    return result_players
