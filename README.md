# AMQ Japanese Drop Down Script

The AMQ script can be accessed [here](https://raw.githubusercontent.com/Mxyuki/AMQ-Scripts/main/amqJapaneseDropDown.user.js). All Japanese names are sourced from [ANN](https://www.animenewsnetwork.com/).

Please note that this script may not comprehensively cover all Anime Names. Therefore, I do not recommend using it for anything else than casual games. If you have suggestions for improvement or wish to enhance its functionality, your contributions are welcome and encouraged.

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

- **ann.py**: Retrieves all anime names from ANN.
- **clean.py**: Cleans the complete list of names, removes duplicates, and replaces characters like `ō` and `ū`.
- **match.py**: Compares ANNID main titles / japanese title / alt english title to AMQ titles to ensure accuracy for AMQ.

### ANNID.json

This JSON file contains all ANNIDs for animes aired as of `7/7/2024`.

### dropDown.json

This is the file used for the modified AMQ drop-down.

## Script Showcase

https://github.com/Mxyuki/amqJP/assets/86327219/a3801216-dabd-4605-91bf-614d3a04e998

