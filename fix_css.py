with open('assets/css/style.css', 'r') as f:
    css = f.read()

import re
css = re.sub(r'\.beyond-page \.nav-modern \{[^}]*\}', '', css)

with open('assets/css/style.css', 'w') as f:
    f.write(css)
