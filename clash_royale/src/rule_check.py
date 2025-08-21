# Rules:
# 500 Donations => promote
# 7 days inactive => degrade / kick
# less than 4 decks used per week for at least 2 consecutive weeks => degrade / kick

from clan_info import get_decks_used_per_member
from cr_api_handler import CR_Api_Handler

def check_donations():
    pass

def check_inactivity():
    pass

def check_clanwar(clan_tag: str):
    decks_per_member = get_decks_used_per_member(clan_tag, 2) # list[dict], where each dict is one week
    underperformed_weeks = {} # player -> number of weeks where <4 decks were used
    print("ℹ️  Checking which players underperformed in which weeks")
    for week in decks_per_member:
        for member in week:
            if week[member] < 4:
                underperformed_weeks[member] = 1 if not member in underperformed_weeks else underperformed_weeks[member] + 1
    print("ℹ️  Checking which players to punish")
    kicklist = [] # list of players to be punished
    for player in underperformed_weeks:
        if underperformed_weeks[player] >= 2:
            kicklist.append(player)
    print("↪️  kicklist:", kicklist)
    names = _map_to_names(kicklist)
    return list(zip(kicklist, names))

def _map_to_names(player_tags: list[str]):
    return [CR_Api_Handler().get_player_name(pt) for pt in player_tags]

print(check_clanwar("#90YCLJRJ"))