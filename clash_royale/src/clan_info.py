from cr_api_handler import CR_Api_Handler
from utils.file_handler import store_to_file

def get_decks_used_per_member(clan_tag: str, number_of_weeks: int) -> list[dict[str, int]]:
    """
    Returns the number of decks each clan member used in the specified number of weeks.
    """
    cr_api_handler = CR_Api_Handler()
    riverracelog = cr_api_handler.get_clan_riverracelog(clan_tag, number_of_weeks)

    store_to_file("racelog", riverracelog)

    clan_results = []

    for week in riverracelog["items"]:
        for standing in week["standings"]:
            if standing["clan"]["tag"] == clan_tag:
                clan_results.append(standing["clan"])

    participants_decks_used = []
    for c in clan_results:
        participants_decks_used_week = {}
        for p in c["participants"]:
            participants_decks_used_week[p["tag"]] = p["decksUsed"]
            cr_api_handler.buffer_name(p["tag"], p["name"])
        participants_decks_used.append(participants_decks_used_week)

    store_to_file("output", participants_decks_used)
    return participants_decks_used

#print(CR_Api_Handler().get_player_name("#2YCQ8PUJ"))