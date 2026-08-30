/* ==========================================================
   Beyond-the-work folder renderer
   Loads content from content/beyond.json and renders a shared page shell.
   ========================================================== */

(function () {
  const slug = document.body.getAttribute('data-slug');
  const hero = document.body.getAttribute('data-hero');

  if (!slug) return;

  function sectionMarkup(section) {
    if (section.kind === 'memory') {
      return `
        <section class="beyond-memory reveal">
          ${section.image ? `<img src="${section.image}" class="beyond-memory-img" alt="">` : ''}
          <div>
            <p class="beyond-memory-label">${section.title || 'A memory'}</p>
            <blockquote class="beyond-memory-body">${section.body || ''}</blockquote>
          </div>
        </section>
      `;
    }

    if (section.kind === 'photo-grid') {
      const items = (section.items || []).map((img) => `
        <div style="aspect-ratio: 4/3; border-radius: 12px; overflow: hidden;">
          <img src="${img}" style="width: 100%; height: 100%; object-fit: cover; filter: grayscale(15%) contrast(1.1);" alt="Placeholder">
        </div>
      `).join('');
      return `
        <section class="beyond-list reveal">
          <h2 class="section-subtitle">${section.title || ''}</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
            ${items}
          </div>
        </section>
      `;
    }

    const items = (section.items || []).map((item) => `
      <li class="folder-entry-clean ${item.cover ? 'has-cover' : ''}">
        <div style="display:flex; align-items:center; flex:1;">
          ${item.cover ? `<img src="${item.cover}" class="entry-cover-img" alt="">` : ''}
          <span class="folder-entry-text">${item.text || ''}</span>
        </div>
        ${item.meta ? `<span class="folder-entry-meta">${item.meta}</span>` : ''}
      </li>
    `).join('');

    return `
      <section class="beyond-list reveal">
        <h2 class="section-subtitle">${section.title || ''}</h2>
        <ul class="folder-list-clean">${items}</ul>
      </section>
    `;
  }

  function render(data) {
    const entry = data[slug];
    if (!entry) {
      const title = document.getElementById('b-title');
      const intro = document.getElementById('b-intro');
      if (title) title.textContent = 'Folder not found';
      if (intro) intro.textContent = 'This Beyond page could not find its matching content entry.';
      return;
    }

    const breadcrumbSlug = document.getElementById('bc-slug');
    const title = document.getElementById('b-title');
    const subtitle = document.getElementById('b-subtitle');
    const intro = document.getElementById('b-intro');
    const heroMedia = document.getElementById('b-hero-media');
    const heroMeta = document.getElementById('b-meta');
    const sectionsHost = document.getElementById('b-sections');
    const addLabel = document.getElementById('b-folder-label');

    if (breadcrumbSlug) breadcrumbSlug.textContent = entry.title;
    if (title) title.innerHTML = entry.title || '';
    if (subtitle) subtitle.textContent = entry.subtitle || '';
    if (intro) intro.innerHTML = entry.intro || '';
    if (addLabel) addLabel.textContent = slug;

    if (heroMedia && hero) {
      heroMedia.style.backgroundImage = `url('${hero}')`;
    }

    if (heroMeta) {
      const listCount = (entry.sections || []).filter((section) => Array.isArray(section.items)).length;
      heroMeta.innerHTML = `
        <span class="beyond-meta-chip">Beyond the work</span>
        <span class="beyond-meta-chip">${(entry.sections || []).length} blocks</span>
      `;
    }

    if (sectionsHost) {
      sectionsHost.innerHTML = (entry.sections || []).map(sectionMarkup).join('');
    }

    if (window.__reInitReveal) window.__reInitReveal();
  }

  fetch('/content/beyond.json?v=5')
    .then((response) => response.json())
    .then(render)
    .catch(() => {
      const title = document.getElementById('b-title');
      const intro = document.getElementById('b-intro');
      if (title) title.textContent = 'Could not load folder';
      if (intro) {
        intro.innerHTML = '<span style="color:var(--text3);font-family:DM Mono,monospace;font-size:12px;">Folder data is unavailable right now.</span>';
      }
    });
})();
