with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# 1. Add q-hint div
html = html.replace('<div id="q-mcq" style="display:none; width: 100%;"></div>', '<div id="q-hint" style="display:none; font-family: var(--font-serif); font-size: 1.2rem; font-style: italic; color: var(--muted); margin-top: 1.5rem; text-align: center;"></div>\n      <div id="q-mcq" style="display:none; width: 100%;"></div>')

# 2. Add btn-hint to q-btns-front
old_btns_front = '''      <div class="btns" id="q-btns-front">
        <button id="btn-show">Show definition</button>
      </div>'''
new_btns_front = '''      <div class="btns" id="q-btns-front">
        <button id="btn-hint" style="grid-column: 1 / 2;">Context Hint</button>
        <button id="btn-show" style="grid-column: 2 / -1;">Show definition</button>
      </div>'''
html = html.replace(old_btns_front, new_btns_front)

# 3. Update loadNext() to setup the hint button
old_word_mode = '''  if(studyMode === 'word') {
      el('q-word').style.fontSize = '3.5rem';
      el('q-word').textContent = W.word;
      el('q-pos').textContent = W.pos;
      el('q-ipa').textContent = W.ipa || '';
      el('q-pos').style.display = 'inline-block';
      el('q-ipa').style.display = 'inline-block';
      document.querySelector('.prompt').textContent = 'Recall the meaning';
      el('q-ex').innerHTML = esc(W.ex);
      el('q-btns-front').style.display='grid';
  }'''

new_word_mode = '''  if(studyMode === 'word') {
      el('q-word').style.fontSize = '3.5rem';
      el('q-word').textContent = W.word;
      el('q-pos').textContent = W.pos;
      el('q-ipa').textContent = W.ipa || '';
      el('q-pos').style.display = 'inline-block';
      el('q-ipa').style.display = 'inline-block';
      document.querySelector('.prompt').textContent = 'Recall the meaning';
      el('q-ex').innerHTML = esc(W.ex);
      
      el('q-hint').style.display = 'none';
      el('btn-hint').style.display = 'block';
      el('btn-show').style.gridColumn = '2 / -1';
      el('q-btns-front').style.display='grid';
      
      el('btn-hint').onclick = () => {
          el('q-hint').innerHTML = esc(W.ex).replace(new RegExp(W.word, 'gi'), '_______');
          el('q-hint').style.display = 'block';
          el('btn-hint').style.display = 'none';
          el('btn-show').style.gridColumn = '1 / -1';
      };
  }'''
html = html.replace(old_word_mode, new_word_mode)

# 4. Hide q-hint when switching to Context Mode
old_context_mode = '''      el('q-word').style.fontSize = '1.35rem';'''
new_context_mode = '''      el('q-hint').style.display = 'none';
      el('q-word').style.fontSize = '1.35rem';'''
html = html.replace(old_context_mode, new_context_mode)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied hint logic.")
