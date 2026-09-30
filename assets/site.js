// Figure 1: a clade simulated by the emphasis forward simulator (assets/emphasis-sim.js),
// drawn three ways — everything that lived, what survives, what is sampled — with
// sliders for the rates. Layout follows the documentation simulator: a lineage's
// daughters branch off it in birth order, alternating above and below.
(function () {
  'use strict';
  var S = window.EmphasisSim;
  var fig = document.getElementById('tree');
  if (!S || !fig) return;
  var svg = fig.querySelector('svg');
  var $ = function (id) { return document.getElementById(id); };
  var NS = 'http://www.w3.org/2000/svg';
  var W = 1000, H = 300, X0 = 8, X1 = 930;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var st = { lam: 1.0, mu: 0.55, bn: 0, T: 6, rho: 1, seed: 121, view: 'complete', sim: null };

  // ---- simulation -------------------------------------------------------------
  function simulate() {
    var prev = st.sim;
    st.sim = S.simulate({ model: 'dd', link: 'linear', pars: [st.lam, st.bn, st.mu, 0],
                          maxT: st.T, rho: st.rho, seed: st.seed, maxTries: 300, maxLin: 500 });
    // carry positions over by row, so a slider move morphs rather than jumps
    if (prev) st.sim.rows.forEach(function (r, i) { r.y = prev.rows[i] ? prev.rows[i].y : undefined; });
    report();
    animate();
  }

  // ---- layout -----------------------------------------------------------------
  function order(rows, vis) {
    var out = [];
    function place(i) {
      var kids = rows[i].kids.filter(function (c) { return vis[c]; });
      var above = kids.filter(function (_, j) { return j % 2 === 0; });
      var below = kids.filter(function (_, j) { return j % 2 === 1; }).reverse();
      above.forEach(place); out.push(i); below.forEach(place);
    }
    if (vis[0]) place(0);
    if (vis[1]) place(1);
    return out;
  }

  function targets() {
    var sim = st.sim, rows = sim.rows, T = st.T, done = sim.status === 'done';
    var living = S.survivors(rows, T, false);
    var sampled = done ? S.survivors(rows, T, true) : living;
    var vis = st.view === 'complete' ? rows.map(function () { return true; })
            : st.view === 'recon' ? living : sampled;
    var ord = order(rows, vis), K = Math.max(ord.length, 1);
    ord.forEach(function (i, k) { rows[i].ty = 10 + (k + 0.5) / K * (H - 20); });
    return { rows: rows, ord: ord, vis: vis, living: living, sampled: sampled, K: K };
  }

  // ---- drawing ----------------------------------------------------------------
  function x(t) { return X0 + (X1 - X0) * t / st.T; }
  function f(v) { return v.toFixed(1); }

  function endOf(r, L) {
    if (st.view === 'complete') return r.end < 0 ? st.T : r.end;
    var alive = st.view === 'sampled' ? (r.end < 0 && r.sampled) : r.end < 0;
    if (alive) return st.T;
    var e = r.birth;
    r.kids.forEach(function (c) { if (L.vis[c] && L.rows[c].birth > e) e = L.rows[c].birth; });
    return e;
  }

  function draw(L) {
    var rows = L.rows, d = { alive: [], unsampled: [], dead: [] }, dots = [], rings = [];
    var CLS = ['dead', 'unsampled', 'alive'];
    var rank = function (c) { return L.sampled[c] ? 2 : L.living[c] ? 1 : 0; };
    L.ord.forEach(function (i) {
      var r = rows[i], start = r.parent >= 0 ? r.birth : 0, e = endOf(r, L);
      // the connector takes the colour of the best thing below it
      if (r.parent >= 0)
        d[CLS[rank(i)]].push('M' + f(x(r.birth)) + ' ' + f(rows[r.parent].y) + 'V' + f(r.y));
      // each stretch of the lineage is coloured by what it still leads to:
      // walking back from its end, a daughter's subtree counts from her birth on
      var cur = r.end < 0 ? (r.sampled || st.sim.status !== 'done' ? 2 : 1) : 0, to = e;
      var kids = r.kids.filter(function (c) { return L.vis[c]; })
                       .sort(function (a, b) { return rows[a].birth - rows[b].birth; });
      for (var k = kids.length - 1; k >= 0; k--) {
        var b = rows[kids[k]].birth;
        if (b < to) { d[CLS[cur]].push('M' + f(x(b)) + ' ' + f(r.y) + 'H' + f(x(to))); to = b; }
        cur = Math.max(cur, rank(kids[k]));
      }
      if (to - start > 1e-9) d[CLS[cur]].push('M' + f(x(start)) + ' ' + f(r.y) + 'H' + f(x(to)));
      if (r.end < 0) {
        if (r.sampled || st.sim.status !== 'done') dots.push('M' + f(x(st.T)) + ' ' + f(r.y) + 'h0.001');
        else if (st.view !== 'sampled') rings.push('M' + f(x(st.T)) + ' ' + f(r.y) + 'h0.001');
      }
    });
    var crown = [0, 1].filter(function (i) { return L.vis[i]; }).map(function (i) { return rows[i].y; });
    if (crown.length) {
      var lo = Math.min.apply(null, crown), hi = Math.max.apply(null, crown);
      d.alive.push('M' + f(x(0)) + ' ' + f(lo) + 'V' + f(hi) + 'M0 ' + f((lo + hi) / 2) + 'H' + f(x(0)));
    }
    var lw = Math.max(0.8, Math.min(2, 160 / L.K));
    svg.style.setProperty('--lw', lw);
    set('p-dead', d.dead.join(''));
    set('p-unsampled', d.unsampled.join(''));
    set('p-alive', d.alive.join(''));
    set('p-rings', rings.join(''));
    set('p-dots', dots.join(''));
  }
  function set(id, dstr) { svg.querySelector('#' + id).setAttribute('d', dstr || 'M0 0'); }

  var raf = null;
  function animate() {
    if (!st.sim || st.sim.status !== 'done') { clearTree(); return; }
    var L = targets();
    L.ord.forEach(function (i) {
      var r = L.rows[i];
      if (r.y === undefined || isNaN(r.y)) r.y = r.parent >= 0 && L.rows[r.parent].y !== undefined ? L.rows[r.parent].y : r.ty;
    });
    if (reduced) { L.ord.forEach(function (i) { L.rows[i].y = L.rows[i].ty; }); draw(L); return; }
    cancelAnimationFrame(raf);
    (function step() {
      var moving = false;
      L.ord.forEach(function (i) {
        var r = L.rows[i], dy = r.ty - r.y;
        if (Math.abs(dy) > 0.2) { r.y += dy * 0.2; moving = true; } else r.y = r.ty;
      });
      draw(L);
      if (moving) raf = requestAnimationFrame(step);
    })();
  }
  function clearTree() { ['p-dead', 'p-unsampled', 'p-alive', 'p-rings', 'p-dots'].forEach(function (id) { set(id, ''); }); }

  function report() {
    var s = st.sim, out = $('tree-status');
    if (s.status === 'too_large') { out.textContent = 'More than 500 lineages at once: lower speciation, or shorten the crown age.'; return; }
    if (s.status !== 'done') { out.textContent = 'No clade survived 300 tries: extinction outweighs speciation here.'; return; }
    var alive = 0, dead = 0, seen = 0;
    s.rows.forEach(function (r) { if (r.end < 0) { alive++; if (r.sampled) seen++; } else dead++; });
    out.textContent = alive + ' living species, ' + dead + ' extinct lineages' +
      (st.rho < 1 ? ', ' + seen + ' living species sampled.' : '.');
  }

  // ---- build the figure -------------------------------------------------------
  svg.innerHTML = '';
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  [['line', { 'class': 'present', x1: X1, y1: 0, x2: X1, y2: H }],
   ['path', { 'class': 'dead', id: 'p-dead' }],
   ['path', { 'class': 'unsampled', id: 'p-unsampled' }],
   ['path', { 'class': 'alive', id: 'p-alive' }],
   ['path', { 'class': 'rings', id: 'p-rings' }],
   ['path', { 'class': 'tips', id: 'p-dots' }]].forEach(function (spec) {
    var el = document.createElementNS(NS, spec[0]);
    Object.keys(spec[1]).forEach(function (k) { el.setAttribute(k, spec[1][k]); });
    svg.appendChild(el);
  });

  // ---- controls ---------------------------------------------------------------
  var views = fig.querySelectorAll('[data-view]');
  views.forEach(function (b) {
    b.addEventListener('click', function () {
      st.view = b.getAttribute('data-view');
      views.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      animate();
    });
  });

  function slider(id, key, digits, resetSeed) {
    var inp = $(id), out = $(id + '-v');
    inp.value = st[key]; out.textContent = (+st[key]).toFixed(digits);
    inp.addEventListener('input', function () {
      st[key] = +inp.value; out.textContent = st[key].toFixed(digits);
      simulate();
    });
  }
  slider('s-lam', 'lam', 2); slider('s-mu', 'mu', 2); slider('s-bn', 'bn', 3);
  slider('s-T', 'T', 1); slider('s-rho', 'rho', 2);

  $('tree-new').addEventListener('click', function () {
    st.seed = (Math.random() * 4294967296) >>> 0;
    st.sim = null;
    simulate();
  });

  var open = $('tree-open'), panel = $('tree-panel');
  open.addEventListener('click', function () {
    var show = panel.hidden;
    panel.hidden = !show;
    open.setAttribute('aria-expanded', show ? 'true' : 'false');
  });

  simulate();

  // the first reveal: grow through time once, then settle
  if (!reduced) {
    svg.addEventListener('animationend', function () { fig.classList.add('faded'); }, { once: true });
    setTimeout(function () { fig.classList.add('faded'); }, 3600);
  } else {
    fig.classList.add('faded');
  }
})();

// Tabs: Research, Teaching and Contact show one at a time. Without JavaScript
// every section stays visible and the links scroll, as on any page.
(function () {
  'use strict';
  var links = document.querySelectorAll('nav.tabs a[href^="#"]');
  var panels = document.querySelectorAll('.panel');
  if (!links.length || !panels.length) return;
  var ids = Array.prototype.map.call(panels, function (p) { return p.id; });

  function panelFor(hash) {
    var id = (hash || '').replace('#', '');
    if (ids.indexOf(id) >= 0) return id;
    var el = id && document.getElementById(id);          // e.g. #publications, #talks
    var host = el && el.closest && el.closest('.panel');
    return host ? host.id : ids[0];
  }

  function show(hash, scrollTo) {
    var id = panelFor(hash);
    panels.forEach(function (p) { p.hidden = p.id !== id; });
    links.forEach(function (a) {
      if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    var target = scrollTo && document.getElementById((hash || '').replace('#', ''));
    if (target && target.id !== id) target.scrollIntoView();
  }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var h = a.getAttribute('href');
      history.replaceState(null, '', h);
      show(h, false);
    });
  });
  window.addEventListener('hashchange', function () { show(location.hash, true); });
  show(location.hash, true);
})();
