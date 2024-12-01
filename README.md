# AMQ Japanese Drop Down Script

The AMQ script can be accessed [here](https://raw.githubusercontent.com/Mxyuki/AMQ-Scripts/main/amqJapaneseDropDown.user.js). All Japanese names are sourced from [ANN](https://www.animenewsnetwork.com/).

Please note that this script may not comprehensively cover all Anime Names. Therefore, I do not recommend using it for anything beyond casual games. I may update it occasionally, but I recommend updating `newDropDown.json` periodically if you use this script regularly.

## Python Folder

The **Python** folder contains the essential scripts to prepare the Japanese name drop-down for AMQ.

To get started, you’ll need to download `libraryMasterList.json` from [AnimeMusicQuiz.com](https://animemusicquiz.com/) via the "Expand Library" feature.

*Here where to find `libraryMasterList.json`*

<img src="https://i.imgur.com/20owlDq.png" alt="How to find the libraryMasterList" width="400">

Once you have this file, follow these steps:

- **scrap.py**: This script extracts English and Romaji titles, along with their ANNID, from `libraryMasterList.json`. The ANNID is used to make API calls to get the Japanese names. The script saves a JSON file every 1000 ANNIDs to track progress.

- **merge.py**: After running `scrap.py`, you can use `merge.py` to combine all partial JSON files into a single file for easier management.

- **clean.py**: This script cleans up `newDropDown.json`, removing duplicate entries. For example, shows like *My Hero Academia*, which has multiple seasons with identical names and Japanese titles, are streamlined to avoid redundancy.

- **fix.py**: This script fix some entry in `newDropDown.json`, so that anime that share same "JA" but not same "RO" can be distinguished in the dropdown.

Feel free to take my scripts, update, or upgrade them as you wish. If you need help with anything related to the script, feel free to reach out to me on Discord: `.micookie`.

---
