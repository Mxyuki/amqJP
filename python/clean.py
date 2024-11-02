import json

with open('nameList.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

unique_anime = {}

for item in data:
    annId = item["annId"]
    ro_title = item["RO"]
    ja_title = item["JA"]

    key = (ro_title, ja_title)

    if key not in unique_anime or annId < unique_anime[key]["annId"]:
        unique_anime[key] = item

filtered_data = list(unique_anime.values())

with open('newDropDown.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print("Filtered data has been saved to newDropDown.json")
