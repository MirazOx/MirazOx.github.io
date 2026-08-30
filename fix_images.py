import json

data = None
with open('content/beyond.json', 'r') as f:
    data = json.load(f)

# Hardcode some relevant unsplash IDs or Wikimedia URLs for relevance
# literature: books, library
lit_images = [
    "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=800&auto=format&fit=crop", # books
    "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=800&auto=format&fit=crop", # study
]
lit_mem = "https://images.unsplash.com/photo-1476275466078-4007374efbfc?q=80&w=800&auto=format&fit=crop" # poetry/marginalia

# film: film camera, cinema screen
film_images = [
    "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=800&auto=format&fit=crop", # movie reels
    "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?q=80&w=800&auto=format&fit=crop", # film camera
]
film_mem = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=800&auto=format&fit=crop" # cinema

# coffee:
coffee_images = [
    "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=800&auto=format&fit=crop"
]
coffee_mem = "https://images.unsplash.com/photo-1495474472204-51ea056bac14?q=80&w=800&auto=format&fit=crop"

# running:
running_images = [
    "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=800&auto=format&fit=crop"
]
running_mem = "https://images.unsplash.com/photo-1502224562085-639556652f33?q=80&w=800&auto=format&fit=crop"

# photography:
photo_images = [
    "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502982720700-baf97d4251a6?q=80&w=800&auto=format&fit=crop"
]
photo_mem = "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?q=80&w=800&auto=format&fit=crop"

# history:
history_images = [
    "https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=800&auto=format&fit=crop", # old map
    "https://images.unsplash.com/photo-1599930113854-d6d7fd521f10?q=80&w=800&auto=format&fit=crop"  # ruins
]
history_mem = "https://images.unsplash.com/photo-1524580131499-1bd125191de7?q=80&w=800&auto=format&fit=crop"

# philosophy:
phil_images = [
    "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1505664194779-8beaceb93744?q=80&w=800&auto=format&fit=crop"
]
phil_mem = "https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=800&auto=format&fit=crop"

# newness:
new_images = [
    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=800&auto=format&fit=crop"
]
new_mem = "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=800&auto=format&fit=crop"

# learning:
learn_images = [
    "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1513258496099-48168024aec0?q=80&w=800&auto=format&fit=crop"
]
learn_mem = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=800&auto=format&fit=crop"

mappings = {
    'literature': (lit_images, lit_mem),
    'film': (film_images, film_mem),
    'coffee': (coffee_images, coffee_mem),
    'running': (running_images, running_mem),
    'photography': (photo_images, photo_mem),
    'history': (history_images, history_mem),
    'philosophy': (phil_images, phil_mem),
    'community': (new_images, new_mem),
    'newness': (new_images, new_mem),
    'learning': (learn_images, learn_mem)
}

for key, entry in data.items():
    if key in mappings:
        imgs, mem_img = mappings[key]
        sections = entry.get('sections', [])
        
        # update photo grid
        for s in sections:
            if s.get('kind') == 'photo-grid':
                s['items'] = imgs
            
            if s.get('kind') == 'memory':
                s['image'] = mem_img

with open('content/beyond.json', 'w') as f:
    json.dump(data, f, indent=2)

