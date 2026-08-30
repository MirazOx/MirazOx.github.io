import re
import glob

html_files = glob.glob('beyond/*/index.html')

for path in html_files:
    with open(path, 'r') as f:
        content = f.read()
    
    # regex to remove <div class="beyond-return reveal"> ... </div>
    # we need to be careful with nested divs. 
    # Since it's a known small block:
    pattern = r'<div class="beyond-return reveal">.*?</div>\s*</div>' 
    # wait, the block is:
    '''
    <div class="beyond-return reveal">
      <div class="cta-box">
        <h3>Return to the shelf</h3>
        <p>This folder is rendered from <code>content/beyond.json</code>. Update the <em id="b-folder-label">...</em> entry there to change this page.</p>
        <a href="/beyond/" class="hero-cta">back to Beyond the work</a>
      </div>
    </div>
    '''
    content = re.sub(r'<div class="beyond-return reveal">[\s\S]*?</div>\s*</div>', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

print(f"Removed beyond-return from {len(html_files)} files.")
