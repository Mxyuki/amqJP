import json
import glob

merged_data = []

for file_num in range(1, 10):
    file_name = f"processed_anime_data_{file_num}.json"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            merged_data.extend(data)
            print(f"Successfully loaded {file_name}")
    except FileNotFoundError:
        print(f"File {file_name} not found, skipping.")
    except json.JSONDecodeError:
        print(f"File {file_name} is not a valid JSON, skipping.")

with open("nameList.json", "w", encoding="utf-8") as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print("Merging complete. The data has been saved to nameList.json.")
