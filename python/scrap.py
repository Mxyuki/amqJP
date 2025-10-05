import json
import requests
import re
import sys
import os

ANN_API_BASE_URL = "https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime="
OUTPUT_FILE = "allTitles.json"
INPUT_FILE = "titles.json"

def fetchJapaneseKana(annId):
    """
    Fetch Japanese kana title from Anime News Network API.
    Returns tuple: (japaneseTitle, apiSuccess)
    - japaneseTitle: The JA title if found, empty string if not found but API succeeded
    - apiSuccess: True if API request succeeded, False otherwise
    """
    try:
        response = requests.get(f"{ANN_API_BASE_URL}{annId}", timeout=10)
        if response.status_code == 200:
            xmlData = response.text
            allJaTitles = re.findall(r'<info[^>]*lang="JA"[^>]*>(.*?)</info>', xmlData)
            kanaTitles = [title for title in allJaTitles if re.search(r'[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', title)]
            japaneseTitle = kanaTitles[0] if kanaTitles else (allJaTitles[0] if allJaTitles else "")
            return japaneseTitle, True
    except Exception as e:
        print(f"Error fetching data for annId {annId}: {str(e)}")
    return "", False

def loadExistingData():
    """
    Load existing newDropDown.json if it exists, otherwise return empty dict.
    """
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            pass
    return {}

def saveData(data):
    """
    Save current data to newDropDown.json in sorted order by annId.
    Filters out entries with None values before saving.
    """
    filteredData = {k: v for k, v in data.items() if v is not None}
    sortedData = dict(sorted(filteredData.items(), key=lambda x: int(x[0])))
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        json.dump(sortedData, file, ensure_ascii=False, indent=2)

def findStartingAnnId(titleData, requestedStart):
    """
    Find the closest annId >= requestedStart.
    Returns the annId to start from.
    """
    annIds = sorted([int(annId) for annId in titleData.keys()])
    
    for annId in annIds:
        if annId >= requestedStart:
            return annId
    
    return annIds[-1] if annIds else 0

def parseArguments():
    """
    Parse command line arguments.
    Returns tuple: (startAnnId, updateMode)
    """
    startAnnId = 0
    updateMode = False
    
    for arg in sys.argv[1:]:
        if arg == '-u':
            updateMode = True
        else:
            try:
                startAnnId = int(arg)
            except ValueError:
                print(f"Warning: Invalid argument '{arg}' ignored")
    
    return startAnnId, updateMode

def getMissingAnnIds(titleData, existingData):
    """
    Get list of annIds that are in title.json but not in newDropDown.json.
    """
    titleIds = set(titleData.keys())
    existingIds = set(existingData.keys())
    missingIds = titleIds - existingIds
    return sorted([int(annId) for annId in missingIds])

def processTitle(annId, romajiTitle):
    """
    Process a single title entry and fetch Japanese kana.
    Returns None only if API request completely fails.
    Uses romaji as fallback if API succeeds but no Japanese title found.
    """
    japaneseKana, apiSuccess = fetchJapaneseKana(annId)
    
    if not apiSuccess:
        return None
    
    entry = {
        'romaji': romajiTitle,
        'japanese': japaneseKana if japaneseKana else romajiTitle
    }
    
    return entry

def main():
    startAnnId, updateMode = parseArguments()
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            titleData = json.load(file)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {INPUT_FILE}")
        return
    
    outputData = loadExistingData() if updateMode else {}
    
    if updateMode:
        print("Update mode enabled - processing only missing entries")
        missingAnnIds = getMissingAnnIds(titleData, outputData)
        filteredAnnIds = [annId for annId in missingAnnIds if annId >= startAnnId]
        if not filteredAnnIds:
            print("No missing entries found")
            return
    else:
        actualStartId = findStartingAnnId(titleData, startAnnId)
        print(f"Starting from annId: {actualStartId}")
        sortedAnnIds = sorted([int(annId) for annId in titleData.keys()])
        filteredAnnIds = [annId for annId in sortedAnnIds if annId >= actualStartId]
    
    totalCount = len(filteredAnnIds)
    processedCount = 0
    
    for annId in filteredAnnIds:
        romajiTitle = titleData[str(annId)]
        
        entry = processTitle(annId, romajiTitle)
        outputData[str(annId)] = entry
        
        saveData(outputData)
        
        processedCount += 1
        status = "Success" if entry is not None else "Skipped - API request failed"
        print(f"Processed annId {annId} - {status} - {processedCount}/{totalCount} ({processedCount / totalCount * 100:.2f}%) complete")
    
    print("Data processing complete.")

if __name__ == "__main__":
    main()
