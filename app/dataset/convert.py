import json
import csv

# Load your JSON data (Assuming your file is named gita.json)
with open('updated_file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# File prefixes
yt_prefix = "https://www.youtube.com/watch?v="
pdf_prefix = "/static/gita_portal_data/pdfs/"

with open('gita_collection.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write Header
    writer.writerow(['chapter', 'verse', 'speaker', 'sanskrit', 'translation', 'youtube_link', 'download_link'])

    for entry in data:
        chap_num = entry['chapter']
        shlokas = entry['Shloka']
        
        # Sort verses numerically
        sorted_verses = sorted(shlokas.keys(), key=lambda x: int(x.split('-')[0]) if '-' in x else int(x))
        
        for v_num in sorted_verses:
            row_data = shlokas[v_num]
            
            # Extract fields based on your JSON structure
            sanskrit = row_data[0]
            translation = row_data[1]
            speaker = row_data[2] # Index 2 is empty string in your JSON
            yt_link = yt_prefix + row_data[3]
            pdf_link = pdf_prefix + row_data[4]
            
            writer.writerow([chap_num, v_num, speaker, sanskrit, translation, yt_link, pdf_link])

print("🎉 Success! 'gita_collection.csv' has been created with all verses.")
