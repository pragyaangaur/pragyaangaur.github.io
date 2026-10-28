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

  // Columns in a spread finish at different heights. Spread each short column's slack over the
  // gaps above its cards, so the white space sits between cards and not at the end of a section.
  function layout() { draw(); }
  var pending;
  function later() { clearTimeout(pending); pending = setTimeout(layout, 120); }
  window.addEventListener("resize", later);
  window.addEventListener("load", layout);
  if (document.fonts) document.fonts.ready.then(layout);
  board.querySelectorAll("img").forEach(function (img) { img.addEventListener("load", later); });
  layout();

  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.preload = "auto"; e.target.play().catch(function () {}); }
      else e.target.pause();
    });
  }, { rootMargin: "200px" });
  board.querySelectorAll("video").forEach(function (v) { seen.observe(v); });

  // By order of the Crown: five quick clicks on the name.
  var name = document.querySelector(".bar .name"), clicks = 0, timer;
  name.addEventListener("click", function (e) {
    e.preventDefault();
    clicks += 1;
    clearTimeout(timer);
    timer = setTimeout(function () { clicks = 0; }, 1200);
    if (clicks < 5 || document.querySelector(".crown")) return;
    clicks = 0;
    var stamp = document.createElement("div");
    stamp.className = "crown";
    stamp.innerHTML = "<span>By order of the Crown</span>";
    document.body.appendChild(stamp);
    setTimeout(function () { stamp.remove(); }, 2700);
  });

  // Korobeiniki on hover over TriKing, on desktop only, and only once the page has had a click or key
  // press, because browsers keep audio locked until then.
  var tri = document.getElementById("triking"), ctx = null, playing = false;
  function unlock() { if (!ctx && window.AudioContext) ctx = new AudioContext(); if (ctx && ctx.state === "suspended") ctx.resume(); }
  document.addEventListener("pointerdown", unlock, { once: true });
  document.addEventListener("keydown", unlock, { once: true });
  if (tri && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    tri.addEventListener("mouseenter", function () {
      if (!ctx || ctx.state !== "running" || playing) return;
      playing = true;
      var E5 = 659.25, D5 = 587.33, C5 = 523.25, B4 = 493.88, A4 = 440, q = 0.24;
      var tune = [[E5, 2], [B4, 1], [C5, 1], [D5, 2], [C5, 1], [B4, 1], [A4, 2], [A4, 1], [C5, 1], [E5, 2], [D5, 1], [C5, 1],
                  [B4, 3], [C5, 1], [D5, 2], [E5, 2], [C5, 2], [A4, 2], [A4, 4]];
      var t = ctx.currentTime + 0.05;
      tune.forEach(function (n) {
        var o = ctx.createOscillator(), g = ctx.createGain(), len = n[1] * q;
        o.type = "square";
        o.frequency.value = n[0];
        g.gain.setValueAtTime(0.0001, t);
        g.gain.exponentialRampToValueAtTime(0.035, t + 0.01);
        g.gain.exponentialRampToValueAtTime(0.0001, t + len * 0.9);
        o.connect(g).connect(ctx.destination);
        o.start(t);
        o.stop(t + len);
        t += len;
      });
      setTimeout(function () { playing = false; }, (t - ctx.currentTime) * 1000 + 3000);
    });
  }

  // Cards are pinned to the board as they scroll into view.
  var cards = board.querySelectorAll(".card");
  if ("IntersectionObserver" in window) {
    var pin = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.remove("later"); pin.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    cards.forEach(function (c) {
      if (c.getBoundingClientRect().top > window.innerHeight) { c.classList.add("later"); pin.observe(c); }
    });
  }

  // A click on a card lifts it off the board to centre stage and blurs the rest. Each card has its own
  // address, so pragyaangaur.dev/#uno opens straight onto Uno.
  var stage = document.querySelector(".stage"), slot = stage.querySelector(".stage-card"), open = null;
  function show(card, push) {
    if (open) open.classList.remove("lifted");
    open = card;
    var copy = card.cloneNode(true);
    copy.removeAttribute("id");
    copy.classList.remove("later");
    slot.replaceChildren(copy);
    copy.querySelectorAll("video").forEach(function (v) { v.preload = "auto"; v.play().catch(function () {}); });
    card.classList.add("lifted");
    stage.hidden = false;
    document.body.classList.add("staged");
    slot.scrollTop = 0;
    if (push) history.pushState({ card: card.id }, "", "#" + card.id);
    stage.querySelector(".stage-close").focus({ preventScroll: true });
  }
  function hide(push) {
    if (!open) return;
    open.classList.remove("lifted");
    stage.hidden = true;
    slot.replaceChildren();
    document.body.classList.remove("staged");
    if (push) history.pushState(null, "", location.pathname + location.search);
    open.scrollIntoView({ block: "center", behavior: "instant" });
    open = null;
  }
  board.addEventListener("click", function (e) {
    var card = e.target.closest(".card");
    if (!card || e.metaKey || e.ctrlKey || e.shiftKey) return;
    // Plain text links on a card still go where they say; everything else opens the card.
    if (e.target.closest("h3 a, .more a, li a, .cap a")) return;
    e.preventDefault();
    show(card, true);
  });
  stage.addEventListener("click", function (e) {
    if (!slot.contains(e.target)) return hide(true);
    // Related cards open in place of this one.
    var rel = e.target.closest("a[data-card]");
    if (rel) { e.preventDefault(); var next = document.getElementById(rel.dataset.card); if (next) show(next, true); return; }
    // A demo loads only when asked for, and replaces its button.
    var run = e.target.closest(".demo button");
    if (run) {
      var frame = document.createElement("iframe");
      frame.src = run.dataset.src;
      frame.title = run.textContent;
      frame.setAttribute("allow", "autoplay; fullscreen");
      run.replaceWith(frame);
    }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(true); });
  function fromHash() {
    var el = location.hash && document.getElementById(location.hash.slice(1));
    if (el && el.classList.contains("card")) show(el, false); else hide(false);
  }
  window.addEventListener("popstate", fromHash);
  fromHash();

  // The lamp switches the lights off and on, and remembers the choice.
  var lamp = document.querySelector(".lamp"), root = document.documentElement;
  lamp.addEventListener("click", function () {
    var dark = root.dataset.theme !== "dark";
    if (dark) root.dataset.theme = "dark"; else delete root.dataset.theme;
    lamp.title = dark ? "Lights on" : "Lights off";
    try { localStorage.theme = dark ? "dark" : "light"; } catch (e) {}
    draw();
  });
  if (root.dataset.theme === "dark") lamp.title = "Lights on";

  // For whoever opens the console.
  console.log("%cHello, fellow inspector.", "font: 700 16px Georgia, serif; color: #7d1f2c");
  console.log("The llms.txt is for the robots. This one is for you.\nIf you read this far, write to pragyaangaur12@gmail.com and tell me what you would build next.");
})();
