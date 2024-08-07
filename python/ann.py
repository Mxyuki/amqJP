import requests
import json
import time
import xml.etree.ElementTree as ET
import math

def fetch_anime_titles(anime_ids):
    base_url = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime="
    titles = []
    
    for anime_id in anime_ids:
        try:
            response = requests.get(base_url + str(anime_id))
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                anime = root.find('anime')
                if anime is not None:
                    main_title = anime.get('name')
                    japanese_title = None
                    english_title = None
                    romaji_title = None
                    
                    for info in anime.findall('info'):
                        title_type = info.get('type')
                        lang = info.get('lang')
                        title_text = info.text.strip() if info.text else None

                        if title_type == 'Alternative title' and lang == 'JA':
                            if title_text and contains_kana_or_kanji(title_text):
                                japanese_title = title_text
                            elif title_text and is_romaji(title_text):
                                romaji_title = title_text
                        elif title_type == 'Alternative title' and lang == 'EN':
                            english_title = title_text
                    
                    if japanese_title is None:
                        japanese_title = main_title
                    
                    if english_title is None:
                        english_title = main_title
                    
                    if romaji_title is None:
                        romaji_title = main_title
                    
                    aired = False
                    for info in anime.findall('info'):
                        if info.get('type') == 'Vintage':
                            aired = True
                            break
                    
                    if aired:
                        titles.append({
                            "id": anime_id,
                            "main_title": main_title,
                            "japanese_title": japanese_title,
                            "english_title": english_title,
                            "romaji_title": romaji_title
                        })
                        print(f"Fetched ID {anime_id}: {main_title} / {japanese_title} / {english_title} / {romaji_title} (Aired)")
                    else:
                        print(f"ID {anime_id}: {main_title} not aired.")
                else:
                    print(f"ID {anime_id} not found.")
            else:
                print(f"ID {anime_id} not found.")
            time.sleep(0.5)
        except Exception as e:
            print(f"An error occurred for ID {anime_id}: {str(e)}")
            time.sleep(1)
            
        if len(titles) == 1000:
            save_titles_to_json(titles, f"animeList{math.ceil(anime_id / 1000)}.json")
            titles = []
    
    if titles:
        save_titles_to_json(titles, f"animeList{math.ceil(anime_ids[-1] / 1000)}.json")

def contains_kana_or_kanji(text):
    return any('\u3040' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FFF' for char in text)

def is_romaji(text):
    return all('A' <= char <= 'Z' or 'a' <= char <= 'z' or char.isspace() or char in {'-', "'"} for char in text)

def save_titles_to_json(titles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    with open('ANNID.json', 'r', encoding='utf-8') as f:
        annid_data = json.load(f)
    
    anime_ids = annid_data['ANNID']
    
    start_id = 1
    end_id = 33000
    
    anime_ids_filtered = [anime_id for anime_id in anime_ids if start_id <= anime_id <= end_id]
    
    fetch_anime_titles(anime_ids_filtered)
    print("All anime titles fetched and saved into multiple JSON files.")
