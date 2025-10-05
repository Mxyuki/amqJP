import json

def extractLongestTitle(names):
    """
    Extract the longest title from names array.
    Priority: JA language first, then EN if no JA exists.
    """
    jaNames = [entry['name'] for entry in names if entry.get('language') == 'JA']
    enNames = [entry['name'] for entry in names if entry.get('language') == 'EN']
    
    if jaNames:
        return max(jaNames, key=len)
    elif enNames:
        return max(enNames, key=len)
    
    return None

def processAmqMaster(inputFile, outputFile):
    """
    Read AMQ Master JSON and extract longest titles for each anime entry.
    Creates a simplified JSON with annId and selected title.
    """
    try:
        with open(inputFile, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        animeMap = data.get('animeMap', {})
        titleData = {}
        
        for annId, animeInfo in animeMap.items():
            names = animeInfo.get('names', [])
            longestTitle = extractLongestTitle(names)
            
            if longestTitle:
                titleData[annId] = longestTitle
            else:
                print(f"Warning: No valid title found for annId {annId}")
        
        with open(outputFile, 'w', encoding='utf-8') as file:
            json.dump(titleData, file, ensure_ascii=False, indent=2)
        
        print(f"Successfully processed {len(titleData)} entries")
        print(f"Output saved to {outputFile}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {inputFile}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {inputFile}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    processAmqMaster('amqMaster.json', 'titles.json')
