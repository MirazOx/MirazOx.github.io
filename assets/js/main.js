/* ==========================================================
   mirazhossain.com — shared JS
   Theme toggle · reveal animations · rotating tags · lightbox
   ========================================================== */

// ---------- THEME ----------
(function initTheme() {
  const saved = localStorage.getItem('miraz-theme');

  if (saved === 'dark' || saved === 'light') {
    document.documentElement.setAttribute('data-theme', saved);
  }
})();

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

  let next;

  if (current === 'dark') next = 'light';
  else if (current === 'light') next = 'dark';
  else next = prefersDark ? 'light' : 'dark';

  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('miraz-theme', next);
}

function bindThemeToggle() {
  const btn = document.getElementById('themeToggle');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleTheme);
}

// ---------- MODERN NAV ----------
function initModernNav() {
  const nav = document.getElementById('siteNav');
  const more = document.querySelector('.nav-more');
  const moreBtn = document.getElementById('navMoreBtn');

  if (!nav) return;

  function setCompactNav() {
    if (window.scrollY > 18) nav.classList.add('is-compact');
    else nav.classList.remove('is-compact');
  }

  setCompactNav();
  window.addEventListener('scroll', setCompactNav, { passive: true });

  if (more && moreBtn) {
    moreBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const open = more.classList.toggle('is-open');
      moreBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', (e) => {
      if (!more.contains(e.target)) {
        more.classList.remove('is-open');
        moreBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const current = window.location.pathname.split('/').pop() || 'index.html';
  const bodyPage = document.body && document.body.dataset ? document.body.dataset.page : '';
  const pageAliases = {
    projects: 'projects.html',
    interventions: 'interventions.html'
  };
  const navLinks = document.querySelectorAll('.nav-main a, .nav-dropdown a');
  let matched = false;

  navLinks.forEach(link => {
    const href = link.getAttribute('href');

    if (href === current || (current === '' && href === 'index.html')) {
      link.classList.add('is-active');
      matched = true;
    }
  });

  if (!matched && pageAliases[bodyPage]) {
    navLinks.forEach(link => {
      if (link.getAttribute('href') === pageAliases[bodyPage]) {
        link.classList.add('is-active');
      }
    });
  }
}

// ---------- REVEAL ON SCROLL ----------
function initReveal() {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
    return;
  }

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('is-visible');
        obs.unobserve(e.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  document.querySelectorAll('.reveal:not(.is-visible)').forEach(el => obs.observe(el));
}

window.__reInitReveal = initReveal;

// ---------- ROTATING TAG WIDGET ----------
function initRotatingTags() {
  const box = document.querySelector('.rotating-tag-box');
  if (!box) return;

  const items = Array.from(box.querySelectorAll('.rotating-tag-item'));
  if (!items.length) return;

  let idx = 0;
  items[0].classList.add('is-active');

  setInterval(() => {
    const current = items[idx];
    idx = (idx + 1) % items.length;
    const next = items[idx];

    current.classList.remove('is-active');
    current.classList.add('is-leaving');
    next.classList.add('is-active');

    setTimeout(() => {
      current.classList.remove('is-leaving');
    }, 700);
  }, 1800);
}

// ---------- LIGHTBOX ----------
function initLightbox() {
  const cards = document.querySelectorAll('.award-card[data-full]');
  const box = document.getElementById('lightbox');

  if (!cards.length || !box) return;

  const img = box.querySelector('.lightbox-img');
  const cap = box.querySelector('.lightbox-cap');
  const close = box.querySelector('.lightbox-close');

  function open(card) {
    if (card.querySelector('.is-placeholder')) return;

    const imgEl = card.querySelector('img');
    if (!imgEl) return;

    const src = card.getAttribute('data-full');
    const badge = card.querySelector('.award-badge');
    const note = card.querySelector('.award-note');

    img.src = src;
    img.alt = imgEl.alt || '';
    cap.textContent = [
      badge && badge.textContent.trim(),
      note && note.textContent.trim()
    ].filter(Boolean).join(' — ');

    box.classList.add('is-open');
    box.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeBox() {
    box.classList.remove('is-open');
    box.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    img.src = '';
  }

  cards.forEach(card => {
    card.addEventListener('click', () => open(card));
    card.setAttribute('tabindex', '0');

    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(card);
      }
    });
  });

  if (close) close.addEventListener('click', closeBox);

  box.addEventListener('click', e => {
    if (e.target === box) closeBox();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeBox();
  });
}

// ---------- INIT ----------
document.addEventListener('DOMContentLoaded', () => {
  bindThemeToggle();
  initModernNav();
  initReveal();
  initRotatingTags();
  initLightbox();
});
