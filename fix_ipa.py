import re
import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

match = re.search(r'const _D=(\[.*?\]);', html, re.DOTALL)
json_str = match.group(1)
data = json.loads(json_str)

count = 0
for item in data:
    word = item['word']
    if item['ipa'] == f"/{word}/":
        try:
            url = f"https://api.datamuse.com/words?sp={word}&md=r&ipa=1&max=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, context=ctx, timeout=10).read()
            api_data = json.loads(resp)
            if api_data and api_data[0].get('word') == word:
                tags = api_data[0].get('tags', [])
                for t in tags:
                    if t.startswith('ipa_pron:'):
                        ipa_val = t.split(':')[1]
                        item['ipa'] = f"/{ipa_val}/"
                        count += 1
                        print(f"Fixed {word} -> {item['ipa']}")
                        break
        except Exception as e:
            print(f"Failed API for {word}: {e}")

data.sort(key=lambda x: x['word'])
new_json_str = json.dumps(data, separators=(',', ':'))
html = html.replace(f"const _D={json_str};", f"const _D={new_json_str};")

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print(f"Fixed {count} IPAs.")
