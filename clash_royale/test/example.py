from clash_royale.src.clan_info import get_decks_used_per_member

number_of_weeks = 3 # number of past clan war weeks to check
clan_tag = "#90YCLJRJ"
print(get_decks_used_per_member(clan_tag, number_of_weeks))