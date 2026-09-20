with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

old_btn_mode = '''el('btn-mode').onclick = () => {
  studyMode = studyMode === 'word' ? 'context' : 'word';
  el('btn-mode').textContent = studyMode === 'word' ? 'Switch to Context Mode' : 'Switch to Word Mode';
  loadNext(true);
};'''

new_btn_mode = '''el('btn-mode').onclick = () => {
  studyMode = studyMode === 'word' ? 'context' : 'word';
  el('btn-mode').textContent = studyMode === 'word' ? 'Switch to Context Mode' : 'Switch to Word Mode';
  shown = false;
  loadNext(true);
};'''
html = html.replace(old_btn_mode, new_btn_mode)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied fix.")
