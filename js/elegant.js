/* ============================================================
   JL-Dex · Elegant edition — behaviour
   Vanilla, no dependencies.  Data comes from js/data.js,
   palette from js/accents.js.
   ============================================================ */
(function () {
  'use strict';

  var DATA = window.JLDEX || [];
  var ACC = window.JLDEX_ACCENTS || {};
  var PORTRAITS = window.JLDEX_PORTRAITS || {};
  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var STATS = [['hp', 'HP'], ['atk', 'ATK'], ['def', 'DEF'], ['spd', 'SPD'], ['int', 'INT'], ['wil', 'WIL']];

  /* ── helpers ─────────────────────────────────────────────── */
  function $(id) { return document.getElementById(id); }
  function slugOf(m) { return (m.image || '').split('/').pop().replace(/\.[a-z]+$/, ''); }
  function accentOf(m) { var a = ACC[slugOf(m)]; return (a && a.accent) || '#c9a227'; }
  /* Portraits where the archive has one, crests where it does not yet. */
  function artFor(m) {
    return PORTRAITS[slugOf(m)] ? 'images/heroes/' + slugOf(m) + '.jpg' : m.image;
  }
  function deepOf(m) { var a = ACC[slugOf(m)]; return (a && a.deep) || '#0a0d16'; }
  function pad(n) { return String(n).padStart(3, '0'); }
  function yearOf(m) { var x = /\((\d{4})\)/.exec(m.first || ''); return x ? +x[1] : 0; }
  function eraOf(m) {
    var y = yearOf(m);
    if (!y) return 'Modern Age';
    if (y <= 1955) return 'Golden Age';
    if (y <= 1969) return 'Silver Age';
    if (y <= 1985) return 'Bronze Age';
    return 'Modern Age';
  }
  var FOUNDERS = ['Superman', 'Batman', 'Wonder Woman', 'Aquaman', 'Martian Manhunter'];
  function isFounder(m) {
    if (FOUNDERS.indexOf(m.name) !== -1) return true;
    return (m.name === 'The Flash' && /Barry/.test(m.alias)) ||
           (m.name === 'Green Lantern' && /Hal/.test(m.alias));
  }
  function abilHTML(list) {
    return (list || []).map(function (a) { return a; }).join('<em>·</em>');
  }

  /* ── starfield ───────────────────────────────────────────── */
  (function stars() {
    var cv = $('stars'); if (!cv) return;
    var ctx = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, pts = [];
    function build() {
      w = cv.width = cv.offsetWidth * dpr;
      h = cv.height = cv.offsetHeight * dpr;
      var count = Math.min(150, Math.round(w / (11 * dpr)));
      pts = [];
      for (var i = 0; i < count; i++) {
        pts.push({
          x: Math.random() * w, y: Math.random() * h * 0.75,
          r: (Math.random() * 1.1 + 0.25) * dpr,
          a: Math.random() * 0.55 + 0.12,
          s: Math.random() * 0.02 + 0.004,
          p: Math.random() * Math.PI * 2
        });
      }
    }
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        var a = p.a * (0.62 + 0.38 * Math.sin(t * 0.0009 + p.p));
        ctx.beginPath();
        ctx.fillStyle = 'rgba(244,241,234,' + a.toFixed(3) + ')';
        ctx.arc(p.x, p.y, p.r, 0, 6.2832);
        ctx.fill();
      }
    }
    function loop(t) { draw(t); requestAnimationFrame(loop); }
    build();
    window.addEventListener('resize', build);
    if (REDUCED) { draw(0); } else { requestAnimationFrame(loop); }
  })();

  /* ── nav shadow on scroll ────────────────────────────────── */
  (function nav() {
    var el = $('nav');
    function on() { el.classList.toggle('is-stuck', window.scrollY > 24); }
    on(); window.addEventListener('scroll', on, { passive: true });
  })();

  /* ── reveal on scroll ────────────────────────────────────── */
  (function reveal() {
    var els = document.querySelectorAll('.reveal');
    if (REDUCED || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(els, function (e) { e.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.14 });
    Array.prototype.forEach.call(els, function (e) { io.observe(e); });
  })();

  /* ── stat rows ───────────────────────────────────────────── */
  /* Widths are written as a CSS custom property so the bars are laid out
     immediately (no timers, no rAF) and the growth runs as a CSS animation. */
  function statRows(m, mount) {
    mount.innerHTML = STATS.map(function (s, n) {
      var v = (m.stats || {})[s[0]] || 0;
      return '<div class="stat"><span class="stat__l">' + s[1] + '</span>' +
             '<span class="stat__t"><i style="--w:' + v + '%;animation-delay:' + (n * 55) + 'ms"></i></span>' +
             '<span class="stat__v">' + v + '</span></div>';
    }).join('');
  }

  /* ── spotlight ───────────────────────────────────────────── */
  var spot = (function () {
    var i = 0, timer = null, paused = false, PROGRESS = 7000;
    var frame = $('spotFrame'), img = $('spImg'), no = $('spNo'), name = $('spName'), alias = $('spAlias'),
        era = $('spEra'), origin = $('spOrigin'), vitals = $('spVitals'), bio = $('spBio'),
        stats = $('spStats'), abils = $('spAbils'), count = $('spCount'), prog = $('spProgress');
    function reduced() { return REDUCED; }

    function show(n) {
      i = (n + DATA.length) % DATA.length;
      var m = DATA[i];
      img.style.opacity = 0;
      img.src = artFor(m); img.alt = 'Portrait of ' + m.name;
      img.onload = function () { img.style.opacity = 1; };
      if (img.complete) img.style.opacity = 1;
      no.textContent = '№ ' + pad(m.id);
      name.textContent = m.name;
      alias.textContent = m.alias;
      era.textContent = eraOf(m) + (isFounder(m) ? ' · Founding Seven' : '');
      origin.textContent = m.origin;
      vitals.innerHTML = '<span>Height<b>' + m.height + '</b></span>' +
                         '<span>Weight<b>' + m.weight + '</b></span>' +
                         '<span>Debut<b>' + (m.first || '') + '</b></span>';
      bio.textContent = m.bio;
      abils.innerHTML = abilHTML(m.abilities);
      statRows(m, stats);
      count.textContent = pad(i + 1) + ' / ' + pad(DATA.length);
      frame.style.setProperty('--accent', accentOf(m));
      restartProgress();
    }
    function restartProgress() {
      prog.classList.remove('run');
      prog.style.width = '0%';
      if (REDUCED) return;
      void prog.offsetWidth;
      prog.classList.add('run');
      prog.style.width = '100%';
      clearTimeout(timer);
      if (!paused) timer = setTimeout(function () { show(i + 1); }, PROGRESS);
    }
    function pause(v) {
      paused = v;
      if (v) { clearTimeout(timer); prog.classList.remove('run'); prog.style.width = getComputedStyle(prog).width; }
      else { restartProgress(); }
    }
    frame.addEventListener('mouseenter', function () { pause(true); });
    frame.addEventListener('mouseleave', function () { pause(false); });
    frame.addEventListener('focusin', function () { pause(true); });
    frame.addEventListener('focusout', function () { pause(false); });
    document.addEventListener('visibilitychange', function () { pause(document.hidden); });
    $('spPrev').addEventListener('click', function () { show(i - 1); });
    $('spNext').addEventListener('click', function () { show(i + 1); });
    $('spOpen').addEventListener('click', function () { sheet.open(DATA[i]); });
    return { show: show, index: function () { return i; } };
  })();

  /* ── roster ──────────────────────────────────────────────── */
  var grid = $('grid'), none = $('none'), tally = $('tally'), q = $('q');
  var ERAS = ['All', 'Golden Age', 'Silver Age', 'Bronze Age', 'Modern Age'];
  var state = { era: 'All', sort: 'dex', list: [] };
  var eraBox = $('eras');

  ERAS.forEach(function (e) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'erabtn' + (e === 'All' ? ' is-on' : '');
    b.dataset.era = e;
    b.textContent = e;
    b.addEventListener('click', function () {
      state.era = e;
      Array.prototype.forEach.call(eraBox.children, function (c) {
        c.classList.toggle('is-on', c === b);
      });
      render();
    });
    eraBox.appendChild(b);
  });

  Array.prototype.forEach.call(document.querySelectorAll('.sortbtn'), function (b) {
    b.addEventListener('click', function () {
      state.sort = b.dataset.sort;
      Array.prototype.forEach.call(document.querySelectorAll('.sortbtn'), function (x) {
        x.classList.toggle('is-on', x === b);
      });
      render();
    });
  });

  function matches(m, words) {
    if (!words.length) return true;
    var hay = [m.name, m.alias, m.origin, (m.types || []).join(' '), (m.abilities || []).join(' '), m.bio,
               m.first, eraOf(m)].join(' ').toLowerCase();
    return words.every(function (w) { return hay.indexOf(w) !== -1; });
  }

  function render() {
    var words = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    var list = DATA.filter(function (m) {
      if (state.era !== 'All' && eraOf(m) !== state.era) return false;
      return matches(m, words);
    });
    if (state.sort === 'az') {
      list.sort(function (a, b) { return (a.name + a.alias).localeCompare(b.name + b.alias); });
    }
    state.list = list;
    tally.innerHTML = list.length
      ? '<b>' + list.length + '</b> of ' + DATA.length + ' members' + (state.era === 'All' ? '' : ' · ' + state.era)
      : '';
    none.hidden = list.length > 0;
    grid.innerHTML = '';
    list.forEach(function (m, k) {
      var card = document.createElement('article');
      card.className = 'card';
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-label', 'Open entry for ' + m.name + ', ' + m.alias);
      card.style.animationDelay = Math.min(k * 22, 420) + 'ms';
      card.style.setProperty('--accent', accentOf(m));
      card.innerHTML =
        '<span class="card__no">' + pad(m.id) + '</span>' +
        (isFounder(m) ? '<span class="card__star" title="Founding member">◆ FOUNDING</span>' : '') +
        '<span class="card__art"><img loading="lazy" src="' + artFor(m) + '" alt="' + m.name + '"></span>' +
        '<h3 class="card__name">' + m.name + '</h3>' +
        '<p class="card__alias">' + m.alias + '</p>' +
        '<span class="card__hair"></span>' +
        '<p class="card__types">' + (m.types || []).join(' · ') + '</p>' +
        '<span class="card__view">View entry →</span>';
      card.addEventListener('click', function () { sheet.open(k); });
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sheet.open(k); }
      });
      grid.appendChild(card);
    });
  }
  q.addEventListener('input', render);

  /* ── entry sheet ─────────────────────────────────────────── */
  var sheet = (function () {
    var el = $('sheet'), i = 0, lastFocus = null, active = DATA;
    var img = $('eImg'), no = $('eNo'), name = $('eName'), alias = $('eAlias'), era = $('eEra'),
        facts = $('eFacts'), stats = $('eStats'), abils = $('eAbils'), bio = $('eBio'), first = $('eFirst'),
        crest = $('eCrest');

    function list() { return state.list.length ? state.list : DATA; }

    /* open(target): target is an index into the visible roster, or a member record */
    function open(target) {
      var L = list();
      if (target && typeof target === 'object') {
        var k = L.indexOf(target);
        if (k === -1) { L = DATA; k = Math.max(0, DATA.indexOf(target)); }
        active = L; i = k;
      } else {
        active = L;
        i = ((target == null ? 0 : target) + L.length) % L.length;
      }
      lastFocus = document.activeElement;
      el.hidden = false;
      document.body.style.overflow = 'hidden';
      fill();
      $('eNext').focus({ preventScroll: true });
    }
    function fill() {
      var m = active[i];
      img.src = artFor(m); img.alt = 'Portrait of ' + m.name;
      crest.src = m.image; crest.alt = m.name + ' crest';
      no.textContent = '№ ' + pad(m.id);
      name.textContent = m.name;
      alias.textContent = m.alias;
      era.textContent = eraOf(m) + (isFounder(m) ? ' · Founding Seven' : '');
      first.textContent = 'First appearance — ' + (m.first || '');
      facts.innerHTML =
        '<div><dt>Origin</dt><dd>' + m.origin + '</dd></div>' +
        '<div><dt>Classification</dt><dd>' + (m.types || []).join(', ') + '</dd></div>' +
        '<div><dt>Height</dt><dd>' + m.height + '</dd></div>' +
        '<div><dt>Weight</dt><dd>' + m.weight + '</dd></div>';
      statRows(m, stats);
      abils.innerHTML = abilHTML(m.abilities);
      bio.textContent = m.bio;
    }
    function close() {
      el.hidden = true;
      document.body.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
    function step(d) { i = (i + d + active.length) % active.length; fill(); }

    Array.prototype.forEach.call(el.querySelectorAll('[data-close]'), function (b) {
      b.addEventListener('click', close);
    });
    $('ePrev').addEventListener('click', function () { step(-1); });
    $('eNext').addEventListener('click', function () { step(1); });
    document.addEventListener('keydown', function (e) {
      if (el.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });
    return { open: open, close: close };
  })();

  /* ── go ──────────────────────────────────────────────────── */
  render();
  spot.show(0);
})();
