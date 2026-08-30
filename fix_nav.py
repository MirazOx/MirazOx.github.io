import re

with open('assets/css/style.css', 'r') as f:
    css = f.read()

# Replace desktop size
css = re.sub(r'font-size:\s*0\.68rem;', 'font-size: 0.75rem; letter-spacing: 0.1em;', css)

# Replace mid-tablet size
css = re.sub(r'font-size:\s*0\.64rem;', 'font-size: 0.72rem;', css)

# Replace small mobile size
css = re.sub(r'font-size:\s*0\.62rem;', 'font-size: 0.7rem;', css)

# Replace smallest mobile size
css = re.sub(r'font-size:\s*0\.58rem;', 'font-size: 0.68rem;', css)

with open('assets/css/style.css', 'w') as f:
    f.write(css)
