document.documentElement.classList.add("js");
const carousel = document.querySelector(".photo-carousel");
if (carousel) {
  const slides = [...carousel.querySelectorAll(".carousel-slide")];
  const track = carousel.querySelector(".carousel-slides");
  const controls = carousel.querySelector(".carousel-controls");
  const playback = carousel.querySelector('[data-carousel="toggle"]');
  const count = carousel.querySelector(".carousel-count");
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let current = 0;
  let paused = motion.matches;
  let hovering = false;
  let timer;
  let controlsTimer;
  let playbackIntent;

  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === current);
      slide.setAttribute("aria-hidden", String(i !== current));
    });
    count.textContent = `${current + 1} / ${slides.length}`;
  }

  function schedule() {
    clearInterval(timer);
    playback.textContent = paused ? "Play" : "Pause";
    playback.setAttribute(
      "aria-label",
      paused ? "Play slideshow" : "Pause slideshow",
    );
    track.setAttribute("aria-live", paused ? "polite" : "off");
    if (!paused && !hovering && !document.hidden) {
      timer = setInterval(() => show(current + 1), 5000);
    }
  }

  function revealTouchControls() {
    clearTimeout(controlsTimer);
    carousel.classList.add("is-controls-visible");
    controlsTimer = setTimeout(() => {
      carousel.classList.remove("is-controls-visible");
      if (controls.contains(document.activeElement)) {
        document.activeElement.blur();
      }
    }, 4000);
  }

  controls.hidden = false;
  carousel.addEventListener("pointerdown", (event) => {
    if (event.pointerType !== "mouse") {
      revealTouchControls();
    }
  });
  // Preserve pointer intent when focusing the button also pauses rotation.
  playback.addEventListener("pointerdown", () => {
    playbackIntent = !paused;
  });
  playback.addEventListener("pointercancel", () => {
    playbackIntent = undefined;
  });
  playback.addEventListener("keydown", () => {
    playbackIntent = undefined;
  });
  playback.addEventListener("click", () => {
    paused = playbackIntent ?? !paused;
    playbackIntent = undefined;
    schedule();
  });
  controls
    .querySelector('[data-carousel="previous"]')
    .addEventListener("click", () => {
      paused = true;
      schedule();
      show(current - 1);
    });
  controls
    .querySelector('[data-carousel="next"]')
    .addEventListener("click", () => {
      paused = true;
      schedule();
      show(current + 1);
    });
  carousel.addEventListener("pointerenter", (event) => {
    if (event.pointerType === "mouse") {
      hovering = true;
      schedule();
    }
  });
  carousel.addEventListener("pointerleave", () => {
    hovering = false;
    schedule();
  });
  carousel.addEventListener("focusin", (event) => {
    if (!carousel.contains(event.relatedTarget)) {
      paused = true;
      schedule();
    }
  });
  document.addEventListener("visibilitychange", schedule);
  motion.addEventListener("change", () => {
    if (motion.matches) paused = true;
    schedule();
  });
  schedule();
}

const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("#main-nav");
function closeMenu() {
  toggle.setAttribute("aria-expanded", "false");
  nav.classList.remove("is-open");
}
toggle?.addEventListener("click", () => {
  const open = toggle.getAttribute("aria-expanded") !== "true";
  toggle.setAttribute("aria-expanded", String(open));
  nav.classList.toggle("is-open", open);
});
document.addEventListener("keydown", (event) => {
  if (
    event.key === "Escape" &&
    toggle?.getAttribute("aria-expanded") === "true"
  ) {
    closeMenu();
    toggle.focus();
  }
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".site-header")) closeMenu();
});

const dialog = document.querySelector(".photo-dialog");
if (dialog && typeof dialog.showModal === "function") {
  document.querySelectorAll("[data-gallery]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
        return;
      event.preventDefault();
      const original = link.querySelector("img");
      const image = dialog.querySelector("img");
      image.src = link.href;
      image.alt = original.alt;
      dialog.querySelector("p").textContent = original.alt;
      dialog.showModal();
    });
  });
  dialog
    .querySelector("button")
    .addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
}
