# amqJP

A Tampermonkey script that replaces the anime dropdown on [AnimeMusicQuiz.com](https://animemusicquiz.com) with Japanese titles instead of Romaji.

## Quick Installation

If you just want to use the script:

1. Install [Tampermonkey](https://www.tampermonkey.net/) browser extension
2. Click this link to install the script: [amqJapaneseDropDown.user.js](https://github.com/Mxyuki/amqJP/raw/refs/heads/main/scripts/amqJapaneseDropDown.user.js)
3. Go to [animemusicquiz.com](https://animemusicquiz.com)
4. Reload the page and the dropdown should now display Japanese titles

## Updating the Dropdown Data

If you want to update the dropdown with the latest anime data, follow these steps:

### Step 1: Extract the Master List

1. Install [Tampermonkey](https://www.tampermonkey.net/)
2. Install the extraction script: [amqListExtract.user.js](https://github.com/Mxyuki/amqJP/raw/refs/heads/main/scripts/amqListExtract.user.js)
3. Go to [animemusicquiz.com](https://animemusicquiz.com)
4. Run the command `/getMaster` in the chat
5. This will download the `amqMaster.json` file

### Step 2: Process the Data

Create a folder and place the following files in it:
- `amqMaster.json` (from Step 1)
- `extract.py`
- `scrap.py`
- `clean.py`

#### Run extract.py

```bash
python extract.py
```

This will create `titles.json` with the format:

```json
{
  "1": "Seihou Tenshi Angel Links",
  "2": "Kakugo no Susume",
  "3": "Nasu: Andalusia no Natsu",
  "4": "Kagaku Ninja-tai Gatchaman"
}
```

#### Run scrap.py

```bash
python scrap.py
```

This script queries the [Anime News Network API](https://www.animenewsnetwork.com/) for each anime ID in `titles.json` to retrieve Japanese titles. It creates/updates `allTitles.json`.

**Advanced Usage:**

```bash
python scrap.py <starting_id> -u
```

- `<starting_id>`: Skip all anime IDs before this number (e.g., `1000` will start from ID 1000)
- `-u`: Update mode - only fetches missing IDs without overwriting existing data. Without this flag, the file will be completely recreated from scratch

**Example:**
```bash
python scrap.py 1000 -u
```

The resulting `allTitles.json` format:

```json
{
  "1": {
    "romaji": "Seihou Tenshi Angel Links",
    "japanese": "星方天使エンジェルリンクス"
  },
  "2": {
    "romaji": "Kakugo no Susume",
    "japanese": "覚悟のススメ"
  },
  "3": {
    "romaji": "Nasu: Andalusia no Natsu",
    "japanese": "茄子 アンダルシアの夏"
  }
}
```

#### Run clean.py

```bash
python clean.py
```

This creates `newDropDown.json` by:
- Removing duplicate entries (same Romaji and Japanese titles)
- For anime with identical Japanese titles but different Romaji names, it identifies the unique parts and appends them to the Japanese title for differentiation

### Step 3: Update the Script

1. Upload your `newDropDown.json` to your GitHub repository
2. Edit line 18 in `amqJapaneseDropDown.user.js`:

```javascript
const JSON_URL = 'https://raw.githubusercontent.com/YOUR_USERNAME/amqJP/main/newDropDown.json';
```

3. Reload your AMQ page to see the updated dropdown

## Repository Structure

```
amqJP/
├── newDropDown.json
├── python/
│   ├── clean.py
│   ├── extract.py
│   └── scrap.py
└── scripts/
    ├── amqJapaneseDropDown.user.js
    └── amqListExtract.user.js
```

## Contributing

Feel free to fork this repository, improve the scripts, or adapt them for your own use. Contributions and updates are welcome.
