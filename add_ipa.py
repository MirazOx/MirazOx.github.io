import re
import json
import eng_to_ipa as ipa

with open('projects/gre-500/index.html', 'r') as f:
    content = f.read()

# 1. Extract the JSON
match = re.search(r'const _D=(\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find _D array")
    exit(1)

json_str = match.group(1)
data = json.loads(json_str)

# 2. Add IPA
for item in data:
    word = item['word']
    transcription = ipa.convert(word)
    # eng_to_ipa sometimes returns the word with an asterisk if it doesn't know it.
    if '*' in transcription:
        # Fallback or just remove the asterisk
        transcription = transcription.replace('*', '')
    item['ipa'] = f"/{transcription}/"

new_json_str = json.dumps(data, separators=(',', ':'))

# 3. Replace the JSON
content = content.replace(f"const _D={json_str};", f"const _D={new_json_str};")

# 4. Inject HTML for IPA
# Find: <div class="pos" id="q-pos"></div>
content = content.replace(
    '<div class="pos" id="q-pos"></div>',
    '<div class="pos" id="q-pos"></div>\n      <div class="ipa" id="q-ipa"></div>'
)

# 5. Inject CSS for IPA
# Find: .pos { ... }
css_insertion = ".ipa { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); margin-top: 1rem; margin-left: 0.5rem; display: inline-block; letter-spacing: 0.05em; }"
content = content.replace(
    '.pos { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); margin-top: 1rem; display: inline-block; padding: 0.15rem 0.5rem; border: 1px solid var(--border); }',
    '.pos { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); margin-top: 1rem; display: inline-block; padding: 0.15rem 0.5rem; border: 1px solid var(--border); }\n  ' + css_insertion
)

# 6. Update JS logic to set IPA
js_insertion = "el('q-pos').textContent=W.pos;\n  el('q-ipa').textContent=W.ipa || '';"
content = content.replace("el('q-pos').textContent=W.pos;", js_insertion)

# 7. Also clear it on ALL MASTERED state
clear_insertion = "el('q-pos').textContent='';\n    el('q-ipa').textContent='';"
content = content.replace("el('q-pos').textContent='';", clear_insertion)


with open('projects/gre-500/index.html', 'w') as f:
    f.write(content)

print("Done.")
