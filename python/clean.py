import json
from typing import Dict, List, Set
from collections import defaultdict

def loadTitles(filePath: str) -> Dict:
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)

def saveTitles(filePath: str, data: Dict) -> None:
    with open(filePath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def findCommonPrefix(strings: List[str]) -> str:
    if not strings:
        return ""
    
    minStr = min(strings)
    maxStr = max(strings)
    
    for i, char in enumerate(minStr):
        if char != maxStr[i]:
            return minStr[:i].strip()
    
    return minStr.strip()

def findCommonSuffix(strings: List[str]) -> str:
    if not strings:
        return ""
    
    reversedStrings = [s[::-1] for s in strings]
    commonPrefix = findCommonPrefix(reversedStrings)
    
    return commonPrefix[::-1].strip()

def extractUniquePart(romaji: str, commonPrefix: str, commonSuffix: str) -> str:
    uniquePart = romaji
    
    if commonPrefix and romaji.startswith(commonPrefix):
        uniquePart = romaji[len(commonPrefix):].strip()
    
    if commonSuffix and uniquePart.endswith(commonSuffix):
        uniquePart = uniquePart[:-len(commonSuffix)].strip()
    
    return uniquePart.strip(": -")

def removeDuplicates(titles: Dict) -> Dict:
    seen = {}
    toRemove = set()
    
    for animeId, data in titles.items():
        key = (data['romaji'], data['japanese'])
        
        if key in seen:
            if int(animeId) < int(seen[key]):
                toRemove.add(seen[key])
                seen[key] = animeId
            else:
                toRemove.add(animeId)
        else:
            seen[key] = animeId
    
    return {k: v for k, v in titles.items() if k not in toRemove}

def processDuplicateJapanese(titles: Dict) -> Dict:
    japaneseGroups = defaultdict(list)
    
    for animeId, data in titles.items():
        japaneseGroups[data['japanese']].append((animeId, data['romaji']))
    
    result = {}
    
    for japanese, entries in japaneseGroups.items():
        if len(entries) == 1:
            animeId, romaji = entries[0]
            result[animeId] = {
                'romaji': romaji,
                'japanese': japanese
            }
        else:
            romajiList = [romaji for _, romaji in entries]
            
            commonPrefix = findCommonPrefix(romajiList)
            commonSuffix = findCommonSuffix(romajiList)
            
            for animeId, romaji in entries:
                uniquePart = extractUniquePart(romaji, commonPrefix, commonSuffix)
                
                if uniquePart:
                    newJapanese = f"{japanese} {uniquePart}"
                else:
                    newJapanese = japanese
                
                result[animeId] = {
                    'romaji': romaji,
                    'japanese': newJapanese
                }
    
    return result

def reorderByIds(titles: Dict) -> Dict:
    sortedIds = sorted(titles.keys(), key=lambda x: int(x))
    return {animeId: titles[animeId] for animeId in sortedIds}

def main():
    inputFile = 'allTitles.json'
    outputFile = 'newDropDown.json'
    
    print(f"Loading titles from {inputFile}...")
    titles = loadTitles(inputFile)
    print(f"Loaded {len(titles)} titles")
    
    print("Removing exact duplicates (same romaji and japanese)...")
    titles = removeDuplicates(titles)
    print(f"After removing duplicates: {len(titles)} titles")
    
    print("Processing titles with duplicate Japanese names...")
    titles = processDuplicateJapanese(titles)
    
    print("Reordering titles by ID...")
    titles = reorderByIds(titles)
    
    print(f"Saving cleaned titles to {outputFile}...")
    saveTitles(outputFile, titles)
    print("Done!")

if __name__ == "__main__":
    main()
