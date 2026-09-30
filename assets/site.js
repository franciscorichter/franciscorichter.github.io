// The tree: grow once through time, then fade the lineages that died out.
// The button switches between the full history and what a living tree records.
(function () {
  var tree = document.getElementById('tree');
  var button = document.getElementById('tree-toggle');
  if (!tree || !button) return;

  var svg = tree.querySelector('svg');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function settle() { tree.classList.add('faded'); }

  if (reduced || !svg) {
    settle();
  } else {
    svg.addEventListener('animationend', settle, { once: true });
    setTimeout(settle, 3600);   // in case the animation never runs (e.g. hidden tab)
  }

  button.addEventListener('click', function () {
    var only = tree.classList.toggle('survivors-only');
    button.setAttribute('aria-pressed', only ? 'true' : 'false');
    button.textContent = only ? 'Show the full history' : 'Show only what survives';
  });
})();
