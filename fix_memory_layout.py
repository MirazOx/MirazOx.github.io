with open('assets/js/beyond.js', 'r') as f:
    js = f.read()

# Remove the inline style from section markup in JS to handle it via CSS
js = js.replace('<section class="beyond-memory reveal" style="display: grid; grid-template-columns: 1fr; gap: 1.5rem;">',
                '<section class="beyond-memory reveal">')

js = js.replace('style="width:100%; border-radius:12px; height: 260px; object-fit: cover;"',
                'class="beyond-memory-img"')

# Bump cache again
js = js.replace('v=4', 'v=5')

with open('assets/js/beyond.js', 'w') as f:
    f.write(js)
