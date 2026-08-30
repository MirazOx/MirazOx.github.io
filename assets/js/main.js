/* ==========================================================
   mirazhossain.com — shared JS
   Theme toggle · reveal animations · rotating tags · lightbox
   ========================================================== */

// ---------- HTTPS GUARD ----------
(function enforceCanonicalHttps() {
  const secureHosts = new Set(['mirazhossain.com', 'www.mirazhossain.com']);
  const host = window.location.hostname;

  if (window.location.protocol === 'http:' && secureHosts.has(host)) {
    window.location.replace(`https://${host}${window.location.pathname}${window.location.search}${window.location.hash}`);
  }
})();

// ---------- THEME ----------
(function initTheme() {
  const saved = localStorage.getItem('miraz-theme');

  if (saved === 'dark' || saved === 'light') {
    document.documentElement.setAttribute('data-theme', saved);
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
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

  const current = window.location.pathname.replace(/\/index\.html$/, '/');
  const bodyPage = document.body && document.body.dataset ? document.body.dataset.page : '';
  const pageAliases = {
    academic: '/academic/',
    projects: '/interventions/',
    interventions: '/interventions/',
    services: '/services/',
    credentials: '/credentials/',
    about: '/about/',
    beyond: '/beyond/',
    research: '/research/',
    writing: '/writing/'
  };
  const navLinks = document.querySelectorAll('.nav-main a, .nav-dropdown a');
  const isHome = bodyPage === 'home' || current === '/' || current === '';
  let matched = isHome;

  navLinks.forEach(link => {
    const href = link.getAttribute('href');

    if (!isHome && href === current) {
      link.classList.add('is-active');
      link.setAttribute('aria-current', 'page');
      matched = true;
    }
  });

  if (!matched && pageAliases[bodyPage]) {
    const alias = pageAliases[bodyPage];
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === alias) {
        link.classList.add('is-active');
        link.setAttribute('aria-current', 'page');
      }
    });
  }
}

// ---------- MOBILE NAV PANEL ----------
function initResponsiveNav() {
  const nav = document.getElementById('siteNav');
  if (!nav || nav.dataset.mobileNavReady === 'true') return;

  const navMain = nav.querySelector('.nav-main');
  const navActions = nav.querySelector('.nav-actions');
  if (!navMain || !navActions) return;

  nav.dataset.mobileNavReady = 'true';

  const button = document.createElement('button');
  button.className = 'nav-menu-toggle';
  button.type = 'button';
  button.setAttribute('aria-expanded', 'false');
  button.setAttribute('aria-controls', 'mobileNavPanel');
  button.setAttribute('aria-label', 'More pages');
  button.innerHTML = '<span class="sr-only">More pages</span>';

  const panel = document.createElement('div');
  panel.className = 'nav-mobile-panel';
  panel.id = 'mobileNavPanel';
  panel.hidden = true;

  navActions.insertBefore(button, navActions.firstChild);
  nav.appendChild(panel);

  const links = Array.from(navMain.querySelectorAll('a'));
  const mobileQuery = window.matchMedia('(max-width: 720px)');

  function closePanel() {
    panel.hidden = true;
    nav.classList.remove('is-menu-open');
    button.setAttribute('aria-expanded', 'false');
  }

  function cloneLink(link) {
    const clone = link.cloneNode(true);
    if (link.classList.contains('is-active')) clone.classList.add('is-active');
    clone.addEventListener('click', closePanel);
    return clone;
  }

  function syncResponsiveNav() {
    links.forEach(link => link.classList.remove('is-overflowed'));
    panel.innerHTML = '';

    if (!mobileQuery.matches) {
      button.hidden = true;
      closePanel();
      return;
    }

    button.hidden = false;

    const available = navMain.clientWidth;
    const widths = new Map(links.map(link => [
      link,
      Math.ceil(link.getBoundingClientRect().width) + 4
    ]));
    const visible = [];
    const overflow = [];
    let used = 0;

    links.forEach(link => {
      const width = widths.get(link) || 0;
      if (used + width <= available) {
        visible.push(link);
        used += width;
      } else {
        overflow.push(link);
      }
    });

    const active = links.find(link => link.classList.contains('is-active'));
    if (active && overflow.includes(active)) {
      const activeWidth = widths.get(active) || 0;

      while (used + activeWidth > available && visible.length) {
        const candidate = [...visible].reverse().find(link => link !== active);
        if (!candidate) break;
        visible.splice(visible.indexOf(candidate), 1);
        overflow.unshift(candidate);
        used -= widths.get(candidate) || 0;
      }

      if (used + activeWidth <= available) {
        overflow.splice(overflow.indexOf(active), 1);
        visible.push(active);
        used += activeWidth;
      }
    }

    links.forEach(link => {
      const isOverflowed = !visible.includes(link);
      link.classList.toggle('is-overflowed', isOverflowed);
    });

    overflow.forEach(link => panel.appendChild(cloneLink(link)));
    button.hidden = overflow.length === 0;
    if (!overflow.length) closePanel();
  }

  button.addEventListener('click', event => {
    event.stopPropagation();
    const open = panel.hidden;
    panel.hidden = !open;
    nav.classList.toggle('is-menu-open', open);
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  document.addEventListener('click', event => {
    if (!nav.contains(event.target)) closePanel();
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closePanel();
  });

  window.addEventListener('resize', () => window.requestAnimationFrame(syncResponsiveNav), { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(syncResponsiveNav);
  window.requestAnimationFrame(syncResponsiveNav);
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
  }, 2000);
}

// ---------- LIGHTBOX ----------
function initLightbox() {
  const cards = document.querySelectorAll('.award-card[data-full]');
  const box = document.getElementById('lightbox');

  if (!box) return;

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

  if (cards.length) {
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
  }

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
  initResponsiveNav();
  initReveal();
  initRotatingTags();
  initLightbox();
});

// Impeccable: Live Timezone (Dhaka)
function updateDhakaTime() {
  const timeEl = document.getElementById('dhaka-time');
  if (!timeEl) return;
  const now = new Date();
  const options = { timeZone: 'Asia/Dhaka', hour: '2-digit', minute: '2-digit', hour12: true };
  const formatter = new Intl.DateTimeFormat('en-US', options);
  timeEl.textContent = formatter.format(now);
}
setInterval(updateDhakaTime, 1000);
updateDhakaTime();
