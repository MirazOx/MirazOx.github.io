import os

with open('interventions/index.html', 'r') as f:
    content = f.read()

snippet = """
        <a class="project-banner reveal" href="/projects/gre-500/">
          <div class="project-banner-media">
            <img src="/assets/images/projects/gre-500-cover.svg" alt="Cover artwork for GRE 500 trainer">
          </div>
          <div class="project-banner-content">
            <div>
              <div class="project-banner-top">
                <span class="project-banner-type">Software tool · GRE · Language</span>
                <span class="badge" style="background: var(--text); color: var(--bg);">new</span>
              </div>
              <h2 class="project-banner-title">GRE 500 — Adaptive Vocabulary Trainer</h2>
              <p class="project-banner-brief">A brutalist, anti-gamified vocabulary trainer implementing spaced repetition and strict editorial aesthetics for mastering high-frequency GRE traps. Stripped of all emojis and glowing progress bars in favor of high-contrast Literata typography and stark grid-based logic.</p>
            </div>
            <div class="project-banner-footer">
              <div class="project-banner-tags">
                <span class="project-banner-tag">UI/UX</span>
                <span class="project-banner-tag">learning</span>
                <span class="project-banner-tag">tools</span>
              </div>
              <span class="project-banner-cta">Open tool →</span>
            </div>
          </div>
        </a>
"""

content = content.replace('<a class="project-banner reveal" href="/projects/bachelor-economy/">', snippet + '\n        <a class="project-banner reveal" href="/projects/bachelor-economy/">')

with open('interventions/index.html', 'w') as f:
    f.write(content)
