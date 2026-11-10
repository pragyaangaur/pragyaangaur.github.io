// A project's own page: the lamp, the loops, and a demo that loads only when asked for.
(function () {
  var root = document.documentElement, lamp = document.querySelector(".lamp");
  lamp.addEventListener("click", function () {
    var dark = root.dataset.theme !== "dark";
    if (dark) root.dataset.theme = "dark"; else delete root.dataset.theme;
    lamp.title = dark ? "Lights on" : "Lights off";
    try { localStorage.theme = dark ? "dark" : "light"; } catch (e) {}
  });
  if (root.dataset.theme === "dark") lamp.title = "Lights on";

  document.querySelectorAll("video").forEach(function (v) { v.preload = "auto"; v.play().catch(function () {}); });

  var run = document.querySelector(".demo button");
  if (run) run.addEventListener("click", function () {
    var frame = document.createElement("iframe");
    frame.src = run.dataset.src;
    frame.title = run.textContent;
    frame.setAttribute("allow", "autoplay; fullscreen");
    run.replaceWith(frame);
    frame.focus();
  });
})();
