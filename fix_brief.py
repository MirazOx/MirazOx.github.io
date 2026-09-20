with open('interventions/index.html', 'r') as f:
    content = f.read()

old_brief = '<p class="project-banner-brief">A brutalist, anti-gamified vocabulary trainer implementing spaced repetition and strict editorial aesthetics for mastering high-frequency GRE traps. Stripped of all emojis and glowing progress bars in favor of high-contrast Literata typography and stark grid-based logic.</p>'
new_brief = '<p class="project-banner-brief">An adaptive vocabulary trainer designed to master the 500 highest-frequency GRE traps. It uses a spaced-repetition engine that aggressively targets your weak spots—forcing you to confront words you keep missing while automatically filtering out the ones you already know.</p>'

old_tags = """              <div class="project-banner-tags">
                <span class="project-banner-tag">UI/UX</span>
                <span class="project-banner-tag">learning</span>
                <span class="project-banner-tag">tools</span>
              </div>"""

new_tags = """              <div class="project-banner-tags">
                <span class="project-banner-tag">spaced repetition</span>
                <span class="project-banner-tag">adaptive learning</span>
                <span class="project-banner-tag">GRE</span>
              </div>"""

content = content.replace(old_brief, new_brief)
content = content.replace(old_tags, new_tags)

with open('interventions/index.html', 'w') as f:
    f.write(content)
