// Draws the pencil threads between related cards, and plays the loops only while they are on screen.
(function () {
  var board = document.querySelector(".board");
  var svg = board.querySelector(".threads");
  var NS = "http://www.w3.org/2000/svg";
  var INK = { red: "#c4392c", blue: "#2347a6", green: "#2c7a45", graphite: "#5a5c56" };
  var links = (board.dataset.links || "").split(";").filter(Boolean).map(function (s) { return s.split(">"); });

  function box(el) {
    var b = board.getBoundingClientRect(), r = el.getBoundingClientRect();
    return { l: r.left - b.left, t: r.top - b.top, r: r.right - b.left, b: r.bottom - b.top, cx: (r.left + r.right) / 2 - b.left, cy: (r.top + r.bottom) / 2 - b.top };
  }

  function add(tag, attrs, parent) {
    var el = document.createElementNS(NS, tag);
    for (var k in attrs) el.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(el);
    return el;
  }

  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    if (window.innerWidth <= 1100) return;
    links.forEach(function (l) {
      var a = document.getElementById(l[0]), b = document.getElementById(l[1]);
      if (!a || !b) return;
      var A = box(a), Bx = box(b), color = INK[l[3]] || INK.graphite;
      // Leave from the side of the source that faces the target, and land just outside the target.
      var right = Bx.cx > A.cx;
      var x1 = right ? A.r + 10 : A.l - 10, y1 = Math.min(Math.max(A.cy, A.t + 40), A.b - 40);
      var x2 = right ? Bx.l - 14 : Bx.r + 14, y2 = Math.min(Math.max(y1 + 10, Bx.t + 60), Bx.b - 60);
      // A shallow arc that sags a little, more for longer reaches.
      var dx = x2 - x1, bow = Math.abs(dx) * 0.38, sag = Math.min(60, 16 + Math.abs(dx) * 0.12);
      var c1x = x1 + (right ? bow : -bow), c1y = y1 + sag;
      var c2x = x2 - (right ? bow : -bow), c2y = y2 + sag * 0.6;
      add("path", { d: "M" + x1 + " " + y1 + " C" + c1x + " " + c1y + " " + c2x + " " + c2y + " " + x2 + " " + y2, stroke: color });
      // Arrowhead along the final tangent.
      var ang = Math.atan2(y2 - c2y, x2 - c2x), h = 11;
      [0.45, -0.45].forEach(function (s) {
        add("path", { d: "M" + x2 + " " + y2 + " L" + (x2 - h * Math.cos(ang + s)) + " " + (y2 - h * Math.sin(ang + s)), stroke: color });
      });
      var t = 0.5, mt = 1 - t;
      var mx = mt * mt * mt * x1 + 3 * mt * mt * t * c1x + 3 * mt * t * t * c2x + t * t * t * x2;
      var my = mt * mt * mt * y1 + 3 * mt * mt * t * c1y + 3 * mt * t * t * c2y + t * t * t * y2;
      var text = add("text", { x: mx, y: my + 26, fill: color, "text-anchor": "middle", transform: "rotate(-3 " + mx + " " + my + ")" });
      text.textContent = l[2];
    });
  }

  var pending;
  function later() { clearTimeout(pending); pending = setTimeout(draw, 120); }
  window.addEventListener("resize", later);
  window.addEventListener("load", draw);
  if (document.fonts) document.fonts.ready.then(draw);
  board.querySelectorAll("img").forEach(function (img) { img.addEventListener("load", later); });
  draw();

  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.preload = "auto"; e.target.play().catch(function () {}); }
      else e.target.pause();
    });
  }, { rootMargin: "200px" });
  board.querySelectorAll("video").forEach(function (v) { seen.observe(v); });
})();
