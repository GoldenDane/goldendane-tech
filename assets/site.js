/* Optional: paste a Cal.com / Calendly link here and every "Book" button goes straight to the calendar. */
const BOOKING_URL = '';
const EMAIL = 'hello@goldenda.com';
// Interface text in the page's language (<html lang="da"> or "en").
const DA = document.documentElement.lang === 'da';
const T = DA
  ? { open: 'Åbn menu', close: 'Luk menu', copy: 'Kopiér adresse', copied: 'Kopieret', subject: 'Gennemgang af arbejdsgang: ', topic: t => 'Vi vil gerne høre om et ' + t + ' af vores proces: ' }
  : { open: 'Open menu', close: 'Close menu', copy: 'Copy address', copied: 'Copied', subject: 'Workflow review: ', topic: t => 'We would like to hear about a ' + t + ' of our process: ' };

document.documentElement.classList.add('js');
document.getElementById('yr').textContent = new Date().getFullYear();
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (BOOKING_URL) document.querySelectorAll('[data-book]').forEach(a => { a.href = BOOKING_URL; a.target = '_blank'; a.rel = 'noopener'; });

// Sticky nav border + active section
const nav = document.querySelector('header.nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 8);
window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
const links = [...document.querySelectorAll('.nav-links a')];
if ('IntersectionObserver' in window) {
  const spy = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
  }), {rootMargin:'-45% 0px -50% 0px'});
  links.forEach(l => { const s = document.querySelector(l.getAttribute('href')); if (s) spy.observe(s); });
}

// Mobile menu
const menuBtn = document.querySelector('.menu-btn'), mainNav = document.getElementById('main-nav');
const setMenu = open => { mainNav.classList.toggle('open', open); menuBtn.setAttribute('aria-expanded', open); menuBtn.setAttribute('aria-label', open ? T.close : T.open); };
menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
mainNav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

// Hero mock: tabs that rotate on their own until the visitor interacts
(() => {
  const mock = document.getElementById('mock');
  const tabs = [...mock.querySelectorAll('[role=tab]')];
  const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));
  const DUR = 7000; let i = 0, timer = null, stopped = reduce;
  mock.style.setProperty('--dur', DUR + 'ms');
  if (stopped) mock.classList.remove('auto');
  const show = n => {
    i = (n + tabs.length) % tabs.length;
    tabs.forEach((t, k) => { const on = k === i; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; panels[k].hidden = !on;
      const p = t.querySelector('.prog'); p.style.animation = 'none'; void p.offsetWidth; p.style.animation = ''; });
  };
  const schedule = () => { clearTimeout(timer); if (!stopped && !mock.classList.contains('paused')) timer = setTimeout(() => { show(i + 1); schedule(); }, DUR); };
  const stop = () => { stopped = true; clearTimeout(timer); mock.classList.remove('auto'); };
  tabs.forEach((t, k) => t.addEventListener('click', () => { stop(); show(k); }));
  mock.querySelector('[role=tablist]').addEventListener('keydown', e => {
    const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (d) { e.preventDefault(); stop(); show(i + d); tabs[i].focus(); }
  });
  // Pausing restarts the current step's timer on resume; the progress bar resumes from where it was.
  mock.addEventListener('mouseenter', () => { mock.classList.add('paused'); clearTimeout(timer); });
  mock.addEventListener('mouseleave', () => { mock.classList.remove('paused'); schedule(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) clearTimeout(timer); else schedule(); });
  show(0); schedule();
})();

// Contact: copy address, and a form that composes an email
document.getElementById('copyEmail').addEventListener('click', e => {
  const b = e.currentTarget;
  const done = () => { b.textContent = T.copied; setTimeout(() => b.textContent = T.copy, 1600); };
  try { navigator.clipboard.writeText(EMAIL).then(done, () => { b.textContent = EMAIL; }); } catch (_) { b.textContent = EMAIL; }
});
document.querySelectorAll('[data-topic]').forEach(a => a.addEventListener('click', () => {
  const m = document.getElementById('f-msg'); if (!m.value) m.value = T.topic(a.dataset.topic);
}));
document.getElementById('contactForm').addEventListener('submit', e => {
  e.preventDefault();
  const f = e.currentTarget, v = k => f.elements[k].value.trim();
  const missing = ['name','company','msg'].find(k => !v(k));
  if (missing) { f.elements[missing].focus(); f.elements[missing].style.borderColor = 'var(--gold-bright)'; return; }
  const subject = T.subject + v('company');
  const body = v('msg') + '\n\n' + v('name') + '\n' + v('company');
  location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  // Many people use webmail, where mailto links open nothing: always say what to do next.
  document.getElementById('formSent').hidden = false;
});

// Gentle reveal: content is visible by default; only elements below the fold fade in.
if ('IntersectionObserver' in window && !reduce) {
  const els = [...document.querySelectorAll('.reveal, .bars')].filter(el => el.getBoundingClientRect().top > innerHeight);
  els.forEach(el => el.classList.add('pending'));
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.remove('pending'); io.unobserve(en.target); }
  }), {rootMargin:'0px 0px -8% 0px'});
  els.forEach(el => io.observe(el));
}
