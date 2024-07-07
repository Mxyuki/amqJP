# AMQ Japanese Drop Down Script

The AMQ script can be accessed [here](https://raw.githubusercontent.com/Mxyuki/AMQ-Scripts/main/amqJapaneseDropDown.user.js). All Japanese names are sourced from [ANN](https://www.animenewsnetwork.com/).

Feel free to use anything here to create an improved version, and please credit me if you publish it elsewhere. I may update it occasionally if motivated, but I recommend updating `dropDown.json` periodically if you use this script regularly.

## AnimeList Folder

This folder contains anime names fetched using the ANN API.

- Files named **animeList(1-12).json** each contain up to 1000 anime names.
- **mergedAnimelist.json** is a combined `.json` file from `animeList(1-12)` files.
- **animeListClean.json** is derived from `mergedAnimelist.json` with duplicate names removed and characters like `ō` replaced as follows:
  - `ō` to `ou`
  - `Ō` to `Ou`
  - `ū` to `uu`

## Python Folder

This folder includes essential Python scripts used:

- **ann.py**: Retrieves all anime names from ANN. (Took 9 hours)
- **clean.py**: Cleans the complete list of names, removes duplicates, and replaces characters like `ō` and `ū`.
- **match.py**: Compares ANNID main titles to AMQ titles to ensure accuracy for AMQ.

### ANNID.json

This JSON file contains all ANNIDs for animes aired as of `7/7/2024`.

### perfectMatch.json

This file lists anime names exactly matching AMQ's main titles.

### unperfectMatch.json

This file includes anime names with a `98%` or greater resemblance to AMQ names, though not exact matches.

### dropDown.json

This file modifies the AMQ drop-down menu, merging `perfectMatch.json` and `unperfectMatch.json`.
