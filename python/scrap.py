import json
import requests
import re

ANN_API_BASE_URL = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime="

# Set the starting annId here
start_id = 0

def fetch_japanese_title(ann_id):
    response = requests.get(f"{ANN_API_BASE_URL}{ann_id}")
    if response.status_code == 200:
        xml_data = response.text
        all_ja_titles = re.findall(r'<info[^>]*lang="JA"[^>]*>(.*?)</info>', xml_data)
        kana_titles = [title for title in all_ja_titles if re.search(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', title)]
        return kana_titles[0] if kana_titles else (all_ja_titles[0] if all_ja_titles else None)
    return None

with open("libraryMasterList.json", "r", encoding="utf-8") as file:
    data = json.load(file)

filtered_data = {anime_id: anime_info for anime_id, anime_info in data["animeMap"].items() if anime_info["annId"] >= start_id}
total_count = len(filtered_data)

output_data = []
processed_count = 0
file_count = 1

for anime_id, anime_info in filtered_data.items():
    ann_id = anime_info["annId"]

    main_names = anime_info["mainNames"]
    en_title = main_names.get("EN") or main_names.get("JA", "")
    ro_title = main_names.get("JA") or en_title
    ja_title = fetch_japanese_title(ann_id) or ro_title
    if not en_title:
        en_title = ro_title
    if not ro_title:
        ro_title = en_title
    if not ja_title:
        ja_title = ro_title
    output_data.append({
        "annId": ann_id,
        "RO": ro_title,
        "EN": en_title,
        "JA": ja_title
    })
    processed_count += 1

    print(f"Processing ANN ID {ann_id} - {processed_count}/{total_count} ({processed_count / total_count * 100:.2f}%) complete")

    if processed_count % 1000 == 0:
        with open(f"processed_anime_data_{file_count}.json", "w", encoding="utf-8") as outfile:
            json.dump(output_data, outfile, ensure_ascii=False, indent=4)
        output_data = []
        print(f"Saved processed_anime_data_{file_count}.json")
        file_count += 1

if output_data:
    with open(f"processed_anime_data_{file_count}.json", "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)

print("Data processing complete.")
