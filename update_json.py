import json

with open('content/beyond.json', 'r') as f:
    data = json.load(f)

# Update learning
if 'learning' in data:
    data['learning']['sections'].insert(1, {
        "kind": "photo-grid",
        "title": "Visual fragments",
        "items": [
            "https://picsum.photos/seed/learn1/600/400",
            "https://picsum.photos/seed/learn2/600/400",
            "https://picsum.photos/seed/learn3/600/400"
        ]
    })
    # Add an image to the memory block
    for s in data['learning']['sections']:
        if s['kind'] == 'memory':
            s['image'] = 'https://picsum.photos/seed/learn-mem/800/400'

# Update literature
if 'literature' in data:
    data['literature']['sections'].insert(1, {
        "kind": "photo-grid",
        "title": "Books & Marginalia",
        "items": [
            "https://picsum.photos/seed/lit1/600/400",
            "https://picsum.photos/seed/lit2/600/400"
        ]
    })
    for s in data['literature']['sections']:
        if s['kind'] == 'memory':
            s['image'] = 'https://picsum.photos/seed/lit-mem/800/400'

# Update photography
if 'photography' in data:
    data['photography']['sections'].insert(1, {
        "kind": "photo-grid",
        "title": "Recent studies",
        "items": [
            "https://picsum.photos/seed/photo1/600/400",
            "https://picsum.photos/seed/photo2/600/400",
            "https://picsum.photos/seed/photo3/600/400",
            "https://picsum.photos/seed/photo4/600/400"
        ]
    })

# Make sure all subpages look less sloppy. 
# They all just use the renderer.

with open('content/beyond.json', 'w') as f:
    json.dump(data, f, indent=2)

