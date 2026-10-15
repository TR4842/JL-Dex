(function () {
  var DATA = window.JLDEX || [];
  var PORTRAITS = window.JLDEX_PORTRAITS || {};
  var grid = document.getElementById('grid');
  var search = document.getElementById('search');
  var filters = document.getElementById('filters');
  var countEl = document.getElementById('count');
  var activeType = '';
  var modal = document.getElementById('modal');
  var currentIndex = -1;

  function pad(n) { return String(n).padStart(3, '0'); }

  // ── art: hero portraits when available, archive crests otherwise ──
  var artMode = 'crest';
  try {
    artMode = localStorage.getItem('jldex-art') ||
      (Object.keys(PORTRAITS).length ? 'portrait' : 'crest');
  } catch (e) {}
  function slugOf(m) { return (m.image || '').split('/').pop().replace(/\.[a-z]+$/, ''); }
  function hasPortrait(m) { return !!PORTRAITS[slugOf(m)]; }
  function artFor(m) {
    return (artMode === 'portrait' && hasPortrait(m)) ? 'images/heroes/' + slugOf(m) + '.jpg' : m.image;
  }
  function syncArtButtons() {
    Array.prototype.forEach.call(document.querySelectorAll('.ambtn'), function (b) {
      b.classList.toggle('active', b.dataset.art === artMode);
      b.disabled = b.dataset.art === 'portrait' && !Object.keys(PORTRAITS).length;
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('.ambtn'), function (b) {
    b.addEventListener('click', function () {
      artMode = b.dataset.art;
      try { localStorage.setItem('jldex-art', artMode); } catch (e) {}
      syncArtButtons();
      render();
      if (!modal.classList.contains('hidden') && currentIndex > -1) open(DATA[currentIndex]);
    });
  });

  // Build type filter chips
  var types = [];
  DATA.forEach(function (m) {
    (m.types || []).forEach(function (t) { if (types.indexOf(t) === -1) types.push(t); });
  });
  var counts = {};
  types.forEach(function (t) {
    counts[t] = DATA.filter(function (m) { return (m.types || []).indexOf(t) !== -1; }).length;
  });
  var always = ['Magic', 'Speedster', 'Lantern', 'Kryptonian', 'Tech', 'Meta-human',
    'Human', 'Cosmic', 'Alien', 'Atlantean', 'Amazon', 'Martian'];
  var shown = types.filter(function (t) { return counts[t] >= 3 || always.indexOf(t) !== -1; });
  if (shown.length > 20) {
    shown.sort(function (a, b) { return counts[b] - counts[a] || a.localeCompare(b); });
    shown = shown.slice(0, 20);
  }
  shown.sort();
  [''].concat(shown).forEach(function (t) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'fbtn' + (t === activeType ? ' active' : '');
    b.dataset.type = t;
    b.textContent = t || 'All';
    b.addEventListener('click', function () {
      activeType = t;
      Array.prototype.forEach.call(filters.children, function (el) {
        el.classList.toggle('active', el.dataset.type === t);
      });
      render();
    });
    filters.appendChild(b);
  });

  function matches(m, q, t) {
    if (t && (m.types || []).indexOf(t) === -1) return false;
    if (!q) return true;
    var hay = [m.name, m.alias, m.origin, (m.types || []).join(' '), (m.abilities || []).join(' '), m.bio]
      .join(' ').toLowerCase();
    return q.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }

  function render() {
    var q = search.value.trim().toLowerCase();
    var t = activeType;
    var list = DATA.filter(function (m) { return matches(m, q, t); });
    countEl.innerHTML = 'Showing <b>' + list.length + '</b> of ' + DATA.length + ' members';
    if (!list.length) {
      grid.innerHTML = '<div class="empty">No members match that search.</div>';
      return;
    }
    grid.innerHTML = '';
    list.forEach(function (m) {
      var card = document.createElement('article');
      card.className = 'card';
      card.tabIndex = 0;
      card.innerHTML =
        '<div class="imgbox"><span class="num">#' + pad(m.id) + '</span>' +
        '<img loading="lazy" src="' + artFor(m) + '" alt="' + m.name + '"></div>' +
        '<div class="body"><h3>' + m.name + '</h3>' +
        '<div class="alias">' + m.alias + '</div>' +
        '<div class="chips">' + (m.types || []).map(function (x) { return '<span class="chip">' + x + '</span>'; }).join('') + '</div></div>';
      card.addEventListener('click', function () { open(m); });
      card.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(m); });
      grid.appendChild(card);
    });
  }

  function statClass(v) { return v >= 90 ? 'high' : v >= 75 ? 'mid' : 'low'; }

  function open(m) {
    currentIndex = DATA.indexOf(m);
    document.getElementById('mImg').src = artFor(m);
    document.getElementById('mImg').alt = m.name;
    document.getElementById('mId').textContent = '#' + pad(m.id);
    document.getElementById('mName').textContent = m.name;
    document.getElementById('mAlias').textContent = m.alias;
    document.getElementById('mTypes').innerHTML = (m.types || []).map(function (x) { return '<span class="chip">' + x + '</span>'; }).join('');
    document.getElementById('mOrigin').textContent = m.origin;
    document.getElementById('mHeight').textContent = m.height;
    document.getElementById('mWeight').textContent = m.weight;
    document.getElementById('mFirst').textContent = m.first;
    var s = m.stats || {};
    var labels = { hp: 'HP', atk: 'ATK', def: 'DEF', spd: 'SPD', int: 'INT', wil: 'WIL' };
    document.getElementById('mStats').innerHTML = Object.keys(labels).map(function (k) {
      var v = s[k] || 0;
      return '<div class="stat"><span class="lbl">' + labels[k] + '</span>' +
        '<span class="bar ' + statClass(v) + '"><i style="width:' + v + '%"></i></span>' +
        '<span class="val">' + v + '</span></div>';
    }).join('');
    document.getElementById('mAbilities').innerHTML = (m.abilities || []).map(function (a) { return '<li>' + a + '</li>'; }).join('');
    document.getElementById('mBio').textContent = m.bio;
    modal.classList.remove('hidden');
    document.querySelector('.modal-card').scrollTop = 0;
  }

  function close() { modal.classList.add('hidden'); }
  function step(d) {
    if (currentIndex < 0) return;
    currentIndex = (currentIndex + d + DATA.length) % DATA.length;
    open(DATA[currentIndex]);
  }

  document.getElementById('closeModal').addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  document.addEventListener('keydown', function (e) {
    if (modal.classList.contains('hidden')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft') step(-1);
  });
  search.addEventListener('input', render);
  search.addEventListener('keydown', function (e) { if (e.key === 'Escape') search.blur(); });

  syncArtButtons();
  render();
})();
