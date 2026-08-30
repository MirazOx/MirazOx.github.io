import json

with open('content/beyond.json', 'r') as f:
    data = json.load(f)

# Literature reading now
lit_items = data.get('literature', {}).get('sections', [])[0].get('items', [])
if len(lit_items) >= 3:
    lit_items[0]['cover'] = "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=150&auto=format&fit=crop" # Generic blue book
    lit_items[1]['cover'] = "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=150&auto=format&fit=crop" # Red/orange book
    lit_items[2]['cover'] = "https://images.unsplash.com/photo-1621360841013-c76831f12258?q=80&w=150&auto=format&fit=crop" # Vintage book

# Film recent watches
film_items = data.get('film', {}).get('sections', [])[0].get('items', [])
if len(film_items) >= 3:
    film_items[0]['cover'] = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=150&auto=format&fit=crop" # cinema/film
    film_items[1]['cover'] = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=150&auto=format&fit=crop"
    film_items[2]['cover'] = "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?q=80&w=150&auto=format&fit=crop"

with open('content/beyond.json', 'w') as f:
    json.dump(data, f, indent=2)

