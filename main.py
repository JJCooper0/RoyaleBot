import json
from cr_api_handler import CR_Api_Handler

def _store_to_file(filename, data):
     with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

number_of_weeks = 3 # number of past clan war weeks to check
clan_tag = "#90YCLJRJ"

riverracelog = CR_Api_Handler().get_clan_riverracelog(clan_tag, number_of_weeks)

_store_to_file("racelog", riverracelog)

clan_results = []
participants_stats = {}

for week in riverracelog["items"]:
    for standing in week["standings"]:
        if standing["clan"]["tag"] == clan_tag:
            clan_results.append(standing["clan"])

for c in clan_results:
    for p in c["participants"]:
        if p["tag"] in participants_stats:
            participants_stats[p["tag"]] += p["decksUsed"]
        else:
            participants_stats[p["tag"]] = p["decksUsed"]

_store_to_file("output", participants_stats)
print(participants_stats)
