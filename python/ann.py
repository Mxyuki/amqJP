import requests
import json
import time
import xml.etree.ElementTree as ET
import math

def fetch_anime_titles(start_id, end_id):
    base_url = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime="
    titles = []
    
    for anime_id in range(start_id, end_id + 1):
        try:
            response = requests.get(base_url + str(anime_id))
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                anime = root.find('anime')
                if anime is not None:
                    main_title = anime.get('name')
                    japanese_title = None
                    
                    for info in anime.findall('info'):
                        if info.get('type') == 'Alternative title' and info.get('lang') == 'JA':
                            title_text = info.text.strip()
                            if contains_kana_or_kanji(title_text):
                                japanese_title = title_text
                                break
                    
                    if japanese_title is None:
                        japanese_title = main_title
                    
                    aired = False
                    for info in anime.findall('info'):
                        if info.get('type') == 'Vintage':
                            aired = True
                            break
                    
                    if aired:
                        titles.append({
                            "id": anime_id,
                            "main_title": main_title,
                            "japanese_title": japanese_title
                        })
                        print(f"Fetched ID {anime_id}: {main_title} / {japanese_title} (Aired)")
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
        save_titles_to_json(titles, f"animeList{math.ceil(end_id / 1000)}.json")

def contains_kana_or_kanji(text):
    return any('\u3040' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FFF' for char in text)

def save_titles_to_json(titles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    start_id = 1
    end_id = 33000
    fetch_anime_titles(start_id, end_id)
    print("All anime titles fetched and saved into multiple JSON files.")
