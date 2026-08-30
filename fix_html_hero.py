import os
import re
import glob

html_files = glob.glob('beyond/*/index.html')

replacement = """      <div class="beyond-hero-copy">
        <a href="/beyond/" class="beyond-back-btn">← Beyond the work</a>
        <h1 class="page-title" id="b-title">Loading…</h1>
        <p class="page-subtitle" id="b-subtitle"></p>
      </div>"""

# Define regex to capture from <div class="beyond-hero-copy"> to </div>
regex = re.compile(r'<div class="beyond-hero-copy">.*?</div>', re.DOTALL)

for path in html_files:
    with open(path, 'r') as f:
        content = f.read()
    
    new_content = regex.sub(replacement, content)
    
    with open(path, 'w') as f:
        f.write(new_content)

print(f"Updated {len(html_files)} files.")
