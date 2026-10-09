/* Teleport website — Google Analytics 4
 *
 * Set GA_MEASUREMENT_ID to the property's web stream ID (Admin → Data streams → Web → "G-…").
 * While it is the placeholder, nothing loads and nothing is sent.
 *
 * Events (all carry page_variant = "v2" | "v3" and site_language = "en" | "zh-HK" | "zh-CN"):
 *   generate_lead     — any "Book…" / mailto click (GA4 recommended event; mark as a Key event)
 *   cta_click         — every button/pill click, with cta_text + cta_location (section id)
 *   language_switch   — EN / 繁 / 简 clicks, with from_language + to_language
 *   section_view      — first time each main section is 50% on screen
 * Scrolls, outbound clicks and page views come from GA4 Enhanced Measurement.
 */
(function () {
  var GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';
  if (!/^G-[A-Z0-9]{6,}$/.test(GA_MEASUREMENT_ID) || GA_MEASUREMENT_ID === 'G-XXXXXXXXXX') return;
  if (location.protocol === 'file:') return; // don't count local previews

  var variant = /v3\.html$/.test(location.pathname) ? 'v3' : 'v2';
  function lang() { return document.documentElement.lang || 'en'; }

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_MEASUREMENT_ID, {
    page_variant: variant,
    site_language: lang()
  });

  function send(name, params) {
    params = params || {};
    params.page_variant = variant;
    params.site_language = lang();
    gtag('event', name, params);
  }

  function sectionOf(el) {
    var sec = el.closest('section[id], header, footer, section');
    if (!sec) return 'unknown';
    return sec.id || (sec.tagName === 'HEADER' ? 'nav' : sec.tagName === 'FOOTER' ? 'footer' : sec.className.split(' ').slice(0, 2).join('.'));
  }

  // CTA + lead clicks
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a.pill, a[href^="mailto:"]');
    if (!a) return;
    var text = (a.textContent || '').trim().slice(0, 60);
    var where = sectionOf(a);
    send('cta_click', { cta_text: text, cta_location: where, link_url: a.getAttribute('href') });
    if (/^mailto:/.test(a.getAttribute('href') || '')) {
      send('generate_lead', { method: 'email', cta_text: text, cta_location: where });
    }
  }, true);

  // Language switch (capture phase: read the language before the i18n handler changes it)
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.lang button[data-lang]');
    if (!b || b.dataset.lang === lang()) return;
    send('language_switch', { from_language: lang(), to_language: b.dataset.lang });
  }, true);

  // Section views
  if ('IntersectionObserver' in window) {
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id || en.target.getAttribute('aria-label') || 'section';
        if (seen[id]) return;
        seen[id] = 1;
        send('section_view', { section_id: id });
        io.unobserve(en.target);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('main section').forEach(function (s) { io.observe(s); });
  }
})();
