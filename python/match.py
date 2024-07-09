import json
from difflib import SequenceMatcher
import re

def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def normalize_string(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

amq_names = load_json('amqNames.json')
anime_list_clean = load_json('animeListClean.json')

matches = []

normalized_amq_names = {normalize_string(name): name for name in amq_names}

def find_best_match(title, normalized_names, threshold):
    best_match = None
    best_ratio = 0
    normalized_title = normalize_string(title)
    for normalized_name, original_name in normalized_names.items():
        ratio = similarity(normalized_title, normalized_name)
        if ratio > best_ratio and ratio >= threshold:
            best_match = original_name
            best_ratio = ratio
    return best_match, best_ratio

print("Finding matches...")
for idx, anime in enumerate(anime_list_clean):
    normalized_main_title = normalize_string(anime['main_title'])
    normalized_english_title = normalize_string(anime['english_title'])
    best_match = None

    if normalized_main_title in normalized_amq_names:
        best_match = normalized_amq_names[normalized_main_title]
    elif normalized_english_title in normalized_amq_names:
        best_match = normalized_amq_names[normalized_english_title]
    else:
        for threshold in [0.90, 0.80]:
            best_match, best_ratio = find_best_match(anime['main_title'], normalized_amq_names, threshold)
            if best_ratio >= threshold:
                break
        
        if best_ratio < 0.80:
            for threshold in [0.90, 0.80]:
                best_match, best_ratio = find_best_match(anime['english_title'], normalized_amq_names, threshold)
                if best_ratio >= threshold:
                    break
    
    if best_match:
        matches.append({
            "id": anime['id'],
            "main_title": best_match,
            "japanese_title": anime['japanese_title']
        })

    if (idx + 1) % 10 == 0:
        print(f"Processed {idx + 1} titles...")

save_json(matches, 'dropDown.json')

print(f"Total matches: {len(matches)}")
