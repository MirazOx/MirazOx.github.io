with open('assets/css/style.css', 'r') as f:
    content = f.read()

# Fix opacity in .hero-fullbleed-portrait
content = content.replace('opacity: 0.86;', 'opacity: 0.98;')

# Fix light mode filter
content = content.replace('filter: grayscale(10%) contrast(1.08) brightness(0.72) saturate(0.85);', 
                          'filter: grayscale(5%) contrast(1.05) brightness(0.98) saturate(0.95);')

# Fix dark mode filter (assuming the brightness(0.66) one is dark mode)
content = content.replace('filter: grayscale(36%) contrast(1.05) brightness(0.66) saturate(0.72);', 
                          'filter: grayscale(15%) contrast(1.05) brightness(0.92) saturate(0.85);')

with open('assets/css/style.css', 'w') as f:
    f.write(content)
