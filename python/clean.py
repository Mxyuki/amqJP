import json

with open('mergedAnimeList.json', 'r', encoding='utf-8') as input_file:
    merged_data = json.load(input_file)

seen_japanese_names = set()

filtered_data = []
for anime in merged_data:
    japanese_title = anime.get('japanese_title')
    if japanese_title not in seen_japanese_names:
        seen_japanese_names.add(japanese_title)
        filtered_data.append(anime)

filtered_json_str = json.dumps(filtered_data, ensure_ascii=False, indent=4)

cleaned_json_str = (
    filtered_json_str
    .replace('ō', 'ou')
    .replace('Ō', 'Ou')
    .replace('ū', 'uu')
)

cleaned_data = json.loads(cleaned_json_str)

with open('animeListClean.json', 'w', encoding='utf-8') as output_file:
    json.dump(cleaned_data, output_file, ensure_ascii=False, indent=4)

print("JSON file cleaned and saved successfully as animeListClean.json")
