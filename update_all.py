import re

# 1. Update brief in interventions/index.html
with open('interventions/index.html', 'r') as f:
    interventions_html = f.read()

old_brief = '<p class="project-banner-brief">An adaptive vocabulary trainer designed to master the 500 highest-frequency GRE traps. It uses a spaced-repetition engine that aggressively targets your weak spots—forcing you to confront words you keep missing while automatically filtering out the ones you already know.</p>'
new_brief = '<p class="project-banner-brief">An adaptive vocabulary trainer designed to master the 500 highest-frequency GRE traps. The rules of the game are strictly enforced: get a word right 5 times in a row and it retires permanently. Miss it, and it returns again and again until you break your bad habits.</p>'

interventions_html = interventions_html.replace(old_brief, new_brief)

with open('interventions/index.html', 'w') as f:
    f.write(interventions_html)


# 2. Update Footer in projects/gre-500/index.html
with open('projects/gre-500/index.html', 'r') as f:
    app_html = f.read()

old_footer = '''  <footer>
    Progress saves automatically to this artifact and persists across sessions.<br>
    Self-graded recall — The error log only helps if you remain honest.
  </footer>'''

new_footer = '''  <footer>
    <div style="margin-bottom: 1rem; font-family: var(--font-sans); font-size: 0.8rem; letter-spacing: 0;">Developed by Miraz Hossain</div>
    Progress saves automatically and persists across sessions.<br>
    Self-graded recall — The error log only helps if you remain honest.
  </footer>'''

# Just in case the old footer text changed slightly, let's use regex
app_html = re.sub(r'<footer>.*?</footer>', new_footer, app_html, flags=re.DOTALL)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(app_html)

print("HTML updates applied.")
