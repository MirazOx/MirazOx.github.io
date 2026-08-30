import os
import re

footer_new = """<footer>
  <div class="container-wide">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 2rem;">
      <div>
        <p class="footer-text" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text3); margin-bottom: 0.25rem;">Location & Local Time</p>
        <p class="footer-text" style="font-family: var(--font-mono); color: var(--text);">Dhaka, Bangladesh — <span id="dhaka-time">--:--</span></p>
      </div>
      <div class="footer-links">
        <a href="mailto:miraz8395@gmail.com"><svg class="footer-icon" aria-hidden="true" focusable="false"><use href="/assets/svg/socials.svg#email"></use></svg><span>email</span></a>
        <a href="https://www.linkedin.com/in/miraz-hossain-a6b278180/" target="_blank" rel="noopener"><svg class="footer-icon" aria-hidden="true" focusable="false"><use href="/assets/svg/socials.svg#linkedin"></use></svg><span>linkedin</span></a>
        <a href="https://x.com/Miraz8395" target="_blank" rel="noopener"><svg class="footer-icon" aria-hidden="true" focusable="false"><use href="/assets/svg/socials.svg#x"></use></svg><span>x</span></a>
        <a href="https://signal.me/#eu/ylklb4x-Gx18h3DzQjtP-vHmFn4lwtTe9dqiCG3wpY0onLpReQBBxoRr0dsrwCoA" target="_blank" rel="noopener"><svg class="footer-icon" aria-hidden="true" focusable="false"><use href="/assets/svg/socials.svg#signal"></use></svg><span>signal</span></a>
        <a href="https://www.strava.com/athletes/182472704" target="_blank" rel="noopener"><svg class="footer-icon" aria-hidden="true" focusable="false"><use href="/assets/svg/socials.svg#strava"></use></svg><span>strava</span></a>
      </div>
    </div>
    <div style="margin-top: 3rem; border-top: 1px solid var(--border); padding-top: 1.5rem; display: flex; justify-content: space-between; font-size: 12px; color: var(--text3);">
      <span>© 2026 Miraz Hossain. All rights reserved.</span>
      <span><a href="/about/" style="color: inherit; text-decoration: none; border-bottom: 0.5px dotted var(--text3);">About</a></span>
    </div>
  </div>
</footer>"""

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Simple regex to replace footer
            content = re.sub(r'<footer>.*?</footer>', footer_new, content, flags=re.DOTALL)
            
            with open(filepath, 'w') as f:
                f.write(content)
