import re

with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# 1. CSS for Light Theme
old_css_root = '''  :root {
    --bg: #0a0a0c;
    --fg: #e2e4e9;
    --muted: #737882;
    --border: #22252a;
    --accent: #d94a38; /* Editorial vermilion for emphasis/errors */
    --accent-hover: #f1523e;
    --font-serif: 'Literata', Georgia, serif;
    --font-mono: 'JetBrains Mono', Menlo, monospace;
    --font-sans: 'Inter', -apple-system, sans-serif;
  }'''
new_css_root = '''  :root {
    --bg: #0a0a0c;
    --fg: #e2e4e9;
    --muted: #737882;
    --border: #22252a;
    --accent: #d94a38;
    --accent-hover: #f1523e;
    --font-serif: 'Literata', Georgia, serif;
    --font-mono: 'JetBrains Mono', Menlo, monospace;
    --font-sans: 'Inter', -apple-system, sans-serif;
  }
  
  html[data-theme="light"] {
    --bg: #ffffff;
    --fg: #111111;
    --muted: #666666;
    --border: #e2e4e9;
    --accent: #d94a38;
  }'''
html = html.replace(old_css_root, new_css_root)

# 2. HTML: Theme Button in Nav
nav_old = '''      <button data-v="browse">Browse</button>
    </nav>'''
nav_new = '''      <button data-v="browse">Browse</button>
      <button id="btn-theme" style="margin-left:auto; border-bottom:none;">Light/Dark</button>
    </nav>'''
html = html.replace(nav_old, nav_new)

# 3. HTML: Mode Button in Tools
tools_old = '''    <div class="tools">
      <button id="btn-skip">Skip Word</button>'''
tools_new = '''    <div class="tools">
      <button id="btn-mode">Mode: Word First</button>
      <button id="btn-skip">Skip Word</button>'''
html = html.replace(tools_old, tools_new)

# 4. HTML: Import Button in Decks
decks_tools_old = '''    <div class="tools" style="margin-top: 3rem;">
      <button id="btn-export">Export Progress (JSON)</button>'''
decks_tools_new = '''    <div class="tools" style="margin-top: 3rem;">
      <button id="btn-export">Export Progress</button>
      <button id="btn-import">Import JSON</button>
      <input type="file" id="file-import" accept=".json" style="display:none">'''
html = html.replace(decks_tools_old, decks_tools_new)

# 5. JS: Global Variables for Mode and Theme
js_init_old = '''let STATE = { stats:{}, log:[], cur:null, v:1, focus:null };
const KEY = 'gre500_v1';
let ready = false;'''
js_init_new = '''let STATE = { stats:{}, log:[], cur:null, v:1, focus:null };
const KEY = 'gre500_v1';
let ready = false;
let studyMode = 'word';

let theme = localStorage.getItem('gre500_theme') || 'dark';
document.documentElement.setAttribute('data-theme', theme);
'''
html = html.replace(js_init_old, js_init_new)

# 6. JS: loadNext function modification
# Need to replace the part that sets the word and pos
old_loadNext_part = '''  const W=WORDS[i], s=st(i);
  el('q-word').textContent=W.word;
  el('q-pos').textContent=W.pos;
  el('q-ipa').textContent=W.ipa || '';
  el('q-def').textContent=W.def;
  el('q-ex').textContent=W.ex;'''

new_loadNext_part = '''  const W=WORDS[i], s=st(i);
  
  if(studyMode === 'word') {
      el('q-word').style.fontSize = '3.5rem';
      el('q-word').textContent = W.word;
      el('q-pos').textContent = W.pos;
      el('q-ipa').textContent = W.ipa || '';
      el('q-pos').style.display = 'inline-block';
      el('q-ipa').style.display = 'inline-block';
      document.querySelector('.prompt').textContent = 'Recall the meaning';
      el('q-ex').innerHTML = esc(W.ex);
  } else {
      el('q-word').style.fontSize = '1.35rem';
      el('q-pos').style.display = 'none';
      el('q-ipa').style.display = 'none';
      
      // Blank out the word (and basic variants like -s, -ed, -ing if possible, but mostly just the base word)
      let blanked = W.ex;
      if (W.ex) {
          const reg = new RegExp(W.word.substring(0, W.word.length-1) + "[a-z]*", "gi");
          blanked = W.ex.replace(reg, '_______');
      }
      el('q-word').textContent = blanked || "No example sentence available.";
      document.querySelector('.prompt').textContent = 'Recall the word';
      
      const posIpa = `<span style="font-family:var(--font-mono); color:var(--muted); font-size:0.75rem;">[${W.pos}] ${W.ipa || ''}</span>`;
      el('q-ex').innerHTML = `<strong>Word:</strong> ${W.word} ${posIpa}<br><br><strong>Context:</strong> ${esc(W.ex)}`;
  }
  
  el('q-def').textContent=W.def;'''
html = html.replace(old_loadNext_part, new_loadNext_part)

# 7. JS: Events and Bindings
old_bindings = '''el('btn-show').onclick=showDef;'''
new_bindings = '''el('btn-show').onclick=showDef;

el('btn-theme').onclick = () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('gre500_theme', theme);
};

el('btn-mode').onclick = () => {
  studyMode = studyMode === 'word' ? 'context' : 'word';
  el('btn-mode').textContent = studyMode === 'word' ? 'Mode: Word First' : 'Mode: Context First';
  loadNext();
};

el('btn-import').onclick = () => el('file-import').click();
el('file-import').onchange = (e) => {
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const data = JSON.parse(ev.target.result);
      if(data && data.stats) {
        STATE = data;
        save();
        loadNext();
        if(el('v-decks').classList.contains('show')) renderDecks();
        toast('PROGRESS IMPORTED');
      } else {
        toast('INVALID FILE');
      }
    } catch(err) {
      toast('ERROR READING FILE');
    }
  };
  reader.readAsText(file);
};
'''
html = html.replace(old_bindings, new_bindings)


with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied new features.")
