import json
import pandas as pd

# JSONが記載されたファイルのパス
file_path = 'shogai_shi_anywhere.json'

# 結果を保持するリスト
records = []
unique_creators = []
# ファイルを開き、1行ずつ読み込む
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 各行を辞書に変換し、リストに追加
        record = json.loads(line)
        title_list = record.get('title')
        title_value = title_list[0].get('value') if title_list else ''
        creator_list = record.get('creator')
        creator_value = creator_list[0].get('name') if creator_list else ''
        unique_creators.append(creator_value)
        extent = record.get('extent')
        issued = record.get('issued')
        material_type = record.get('materialType')

        records.append({
            'title': title_value,
            'creator': creator_value,
            'extent': extent,
            'issued': issued,
            'material_type': material_type
        })
        print(record)

df = pd.DataFrame(records)
df.to_csv('shogai_shi_anywhere_simple.csv', index=False)

unique_creators = list(set(unique_creators))
print(unique_creators)
print(len(unique_creators))
