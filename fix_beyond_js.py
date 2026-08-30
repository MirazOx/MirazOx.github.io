with open('assets/js/beyond.js', 'r') as f:
    js = f.read()

import re

# We want to replace the folder-entry-clean rendering logic.
# The original logic:
old_logic = """    const items = (section.items || []).map((item) => `
      <li class="folder-entry-clean">
        <span class="folder-entry-text">${item.text || ''}</span>
        ${item.meta ? `<span class="folder-entry-meta">${item.meta}</span>` : ''}
      </li>
    `).join('');"""

new_logic = """    const items = (section.items || []).map((item) => `
      <li class="folder-entry-clean ${item.cover ? 'has-cover' : ''}">
        <div style="display:flex; align-items:center; flex:1;">
          ${item.cover ? `<img src="${item.cover}" class="entry-cover-img" alt="">` : ''}
          <span class="folder-entry-text">${item.text || ''}</span>
        </div>
        ${item.meta ? `<span class="folder-entry-meta">${item.meta}</span>` : ''}
      </li>
    `).join('');"""

js = js.replace(old_logic, new_logic)

# Also bump cache buster to v=4
js = js.replace('v=3', 'v=4')

with open('assets/js/beyond.js', 'w') as f:
    f.write(js)
