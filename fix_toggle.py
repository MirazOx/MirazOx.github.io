with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# Fix HTML button text
html = html.replace('<button id="btn-mode">Mode: Word First</button>', '<button id="btn-mode">Switch to Context Mode</button>')
html = html.replace('<button id="btn-mode">Mode: Context First</button>', '<button id="btn-mode">Switch to Context Mode</button>')

# Fix JS toggle logic
old_js = '''el('btn-mode').textContent = studyMode === 'word' ? 'Mode: Word First' : 'Mode: Context First';'''
new_js = '''el('btn-mode').textContent = studyMode === 'word' ? 'Switch to Context Mode' : 'Switch to Word Mode';'''
html = html.replace(old_js, new_js)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied fix.")
