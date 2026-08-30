import json

with open('content/beyond.json', 'r') as f:
    data = json.load(f)

for key in data.keys():
    entry = data[key]
    sections = entry.get('sections', [])
    
    # Check if a photo-grid exists
    has_photo = any(s.get('kind') == 'photo-grid' for s in sections)
    
    if not has_photo:
        # Add a photo grid as the second item, or first if empty
        photo_sec = {
            "kind": "photo-grid",
            "title": "Visual fragments",
            "items": [
                f"https://picsum.photos/seed/{key}1/800/600",
                f"https://picsum.photos/seed/{key}2/800/600"
            ]
        }
        if len(sections) > 0:
            sections.insert(1, photo_sec)
        else:
            sections.append(photo_sec)
            
    # Make sure memory sections have images
    for s in sections:
        if s.get('kind') == 'memory' and 'image' not in s:
            s['image'] = f"https://picsum.photos/seed/{key}-mem/800/400"

with open('content/beyond.json', 'w') as f:
    json.dump(data, f, indent=2)
