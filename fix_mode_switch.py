with open('projects/gre-500/index.html', 'r') as f:
    html = f.read()

# 1. Update btn-mode onclick
old_btn_mode = '''el('btn-mode').onclick = () => {
  studyMode = studyMode === 'word' ? 'context' : 'word';
  el('btn-mode').textContent = studyMode === 'word' ? 'Switch to Context Mode' : 'Switch to Word Mode';
  loadNext();
};'''

new_btn_mode = '''el('btn-mode').onclick = () => {
  studyMode = studyMode === 'word' ? 'context' : 'word';
  el('btn-mode').textContent = studyMode === 'word' ? 'Switch to Context Mode' : 'Switch to Word Mode';
  loadNext(true);
};'''
html = html.replace(old_btn_mode, new_btn_mode)

# 2. Update loadNext() signature and picking logic
old_loadNext_start = '''function loadNext(){
  const i=pick();
  STATE.cur=i;
  shown=false;
  if(i==null){
    el('q-word').textContent= STATE.focus ? 'DECK CLEARED' : 'ALL 500 MASTERED';'''

new_loadNext_start = '''function loadNext(keepCurrent = false){
  let i;
  if (keepCurrent && STATE.cur != null) {
      i = STATE.cur;
  } else {
      i = pick();
      STATE.cur = i;
      shown = false;
  }
  
  if(i==null){
    el('q-word').textContent= STATE.focus ? 'DECK CLEARED' : 'ALL 500 MASTERED';'''
html = html.replace(old_loadNext_start, new_loadNext_start)

# 3. Add el('q-mcq').style.display='none'; and el('q-btns-next').style.display='none'; to the empty state block
old_empty_state = '''    el('q-btns-front').style.display='none';
    el('q-btns-back').style.display='none';
    el('q-flash').textContent='Review decks or reset a word.';'''

new_empty_state = '''    el('q-btns-front').style.display='none';
    el('q-btns-back').style.display='none';
    el('q-mcq').style.display='none';
    el('q-btns-next').style.display='none';
    el('q-flash').textContent='Review decks or reset a word.';'''
html = html.replace(old_empty_state, new_empty_state)

with open('projects/gre-500/index.html', 'w') as f:
    f.write(html)

print("Applied fix.")
