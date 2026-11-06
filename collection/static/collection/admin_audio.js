(function () {
  var audio = new Audio();
  var current = null;

  function show(btn, playing) {
    btn.textContent = playing ? "⏸" : "▶";
    btn.setAttribute("aria-label", playing ? "Pause" : "Play");
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".play-btn");
    if (!btn) return;

    if (btn === current && !audio.paused) {
      audio.pause();
      show(btn, false);
      return;
    }
    if (btn !== current) {
      if (current) show(current, false);
      audio.src = btn.dataset.src;
      current = btn;
    }
    show(btn, true);
    audio.play().catch(function (err) {
      console.error("Couldn't play", btn.dataset.src, err);
      show(btn, false);
    });
  });

  audio.addEventListener("ended", function () {
    if (current) show(current, false);
  });
})();