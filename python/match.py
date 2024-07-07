import json
from difflib import SequenceMatcher

def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

amq_names = load_json('amqNames.json')
anime_list_clean = load_json('animeListClean.json')

perfect_match = []
unperfect_match = []

print("Finding perfect matches...")
for idx, anime in enumerate(anime_list_clean):
    if anime['main_title'] in amq_names:
        perfect_match.append(anime)
    if (idx + 1) % 10 == 0:
        print(f"Processed {idx + 1} titles for perfect matches...")

print("Finding unperfect matches...")
for idx, anime in enumerate(anime_list_clean):
    if anime not in perfect_match:
        best_match = None
        best_ratio = 0
        for name in amq_names:
            ratio = similarity(anime['main_title'], name)
            if ratio > best_ratio:
                best_match = name
                best_ratio = ratio
        
        if best_ratio >= 0.98:
            anime['main_title'] = best_match
            unperfect_match.append(anime)
    if (idx + 1) % 10 == 0:
        print(f"Processed {idx + 1} titles for unperfect matches...")

save_json(perfect_match, 'perfectMatch.json')
save_json(unperfect_match, 'unperfectMatch.json')

print(f"Perfect matches: {len(perfect_match)}")
print(f"Unperfect matches: {len(unperfect_match)}")