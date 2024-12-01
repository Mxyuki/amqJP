import json

with open('newDropDown.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

updated_data = []

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        if data[i]['JA'] == data[j]['JA'] and data[i]['RO'] != data[j]['RO']:
            shorter_ro, longer_ro = (data[i]['RO'], data[j]['RO']) if len(data[i]['RO']) < len(data[j]['RO']) else (data[j]['RO'], data[i]['RO'])
            shorter_ja, longer_ja = (data[i]['JA'], data[j]['JA']) if len(data[i]['RO']) < len(data[j]['RO']) else (data[j]['JA'], data[i]['JA'])
            updated_ro = longer_ro.replace(shorter_ro, '').strip()
            updated_ja = longer_ja + " " + updated_ro
            
            if len(data[i]['RO']) < len(data[j]['RO']):
                old_ja = data[j]['JA']
                data[j]['JA'] = updated_ja
            else:
                old_ja = data[i]['JA']
                data[i]['JA'] = updated_ja

            updated_data.append({"oldJA": old_ja, "newJA": updated_ja})

with open('newDropDown.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

with open('updated.json', 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, ensure_ascii=False, indent=4)

print("File updated successfully.")
