import re
import glob

# Ensure all HTML files have data-hero
hero_mappings = {
    'coffee': 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=2000&auto=format&fit=crop',
    'community': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=2000&auto=format&fit=crop',
    'film': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=2000&auto=format&fit=crop',
    'history': 'https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=2000&auto=format&fit=crop',
    'learning': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=2000&auto=format&fit=crop',
    'literature': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2000&auto=format&fit=crop',
    'newness': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=2000&auto=format&fit=crop',
    'philosophy': 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=2000&auto=format&fit=crop',
    'photography': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=2000&auto=format&fit=crop',
    'running': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?q=80&w=2000&auto=format&fit=crop',
    'spanish': 'https://images.unsplash.com/photo-1543783207-ec64e4d95325?q=80&w=2000&auto=format&fit=crop'
}

html_files = glob.glob('beyond/*/index.html')

for path in html_files:
    # get slug from path (beyond/slug/index.html)
    slug = path.split('/')[1]
    url = hero_mappings.get(slug)
    if url:
        with open(path, 'r') as f:
            content = f.read()
        
        # If it doesn't have data-hero, inject it after data-slug
        if 'data-hero=' not in content:
            content = re.sub(f'data-slug="{slug}"', f'data-slug="{slug}" data-hero="{url}"', content)
            print(f"Injected data-hero for {slug}")
        else:
            # Replace existing just in case
            content = re.sub(r'data-hero="[^"]+"', f'data-hero="{url}"', content)
            
        with open(path, 'w') as f:
            f.write(content)
