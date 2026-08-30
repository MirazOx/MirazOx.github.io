import re

with open('beyond/index.html', 'r') as f:
    content = f.read()

count = 0
def replacer(match):
    global count
    count += 1
    return f'class="interest-card has-photo bento-{count}"'

new_content = re.sub(r'class="interest-card has-photo"', replacer, content)

with open('beyond/index.html', 'w') as f:
    f.write(new_content)
