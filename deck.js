// LinkedIn 101 deck navigation: arrows, dots, swipe, deep-link via hash.
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  if (!slides.length) return;
  var dotwrap = document.querySelector('.dots');
  var cur = document.querySelector('#cur');
  var tot = document.querySelector('#tot');
  var i = 0, dots = [];

  slides.forEach(function (s, n) {
    var d = document.createElement('button');
    d.className = 'dot';
    d.setAttribute('aria-label', 'Go to slide ' + (n + 1));
    d.addEventListener('click', function () { go(n); });
    dotwrap.appendChild(d);
    dots.push(d);
  });
  if (tot) tot.textContent = String(slides.length).padStart(2, '0');

  function go(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s, k) { s.classList.toggle('active', k === i); });
    dots.forEach(function (d, k) { d.classList.toggle('on', k === i); });
    if (cur) cur.textContent = String(i + 1).padStart(2, '0');
    if (history.replaceState) history.replaceState(null, '', '#' + (i + 1));
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { go(i + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { go(i - 1); e.preventDefault(); }
    if (e.key === 'Home') go(0);
    if (e.key === 'End') go(slides.length - 1);
  });
  var nx = document.querySelector('.next'), pv = document.querySelector('.prev');
  if (nx) nx.addEventListener('click', function () { go(i + 1); });
  if (pv) pv.addEventListener('click', function () { go(i - 1); });

  var x0 = null;
  document.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });

  var h = parseInt((location.hash || '').slice(1), 10);
  go(h ? h - 1 : 0);
})();
