/* Home hero: one message over two scenes, ten seconds each.
   Car footage from cinematic-five-review /carro/landing; world footage from the cinematic globe
   (Pablo, 7 Oct 2026: "solo usaremos el carro y el mundo, 10 segundos cada uno con el mismo copy").
   Only the visible scene plays. The world file loads late, after the car has been on screen. */
(() => {
  'use strict';

  const hero = document.querySelector('.car-hero');
  const media = hero?.querySelector('.car-media');
  const carVideo = media?.querySelector('video');
  if (!hero || !media || !carVideo) return;

  const portrait = matchMedia('(max-width:1023px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion:reduce)');
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  const carVersion = 'whiskers-flex-89262c8d-5f6ca10d';
  const worldVersion = 'world-10s-d563b31d-fffbe0e3';
  const SCENE_MS = 10000;
  const FADE_MS = 800;
  const PRELOAD_MS = 4000;

  const car = {
    name: 'car',
    video: carVideo,
    variant: '',
    version: 0,
    pending: false,
    sources: {
      desktop: `/a/media/car/car-desktop.mp4?v=${carVersion}`,
      mobile: `/a/media/car/car-mobile.mp4?v=${carVersion}`,
    },
  };
  const world = {
    name: 'world',
    video: null,
    variant: '',
    version: 0,
    pending: false,
    disabled: false,
    sources: {
      desktop: `/a/media/world/world-desktop.mp4?v=${worldVersion}`,
      mobile: `/a/media/world/world-mobile.mp4?v=${worldVersion}`,
    },
    posters: {
      desktop: `/a/media/world/world-desktop.webp?v=${worldVersion}`,
      mobile: `/a/media/world/world-mobile.webp?v=${worldVersion}`,
    },
  };

  let active = car;
  let visible = hero.getBoundingClientRect().bottom > 0 && hero.getBoundingClientRect().top < innerHeight;
  // A car failure keeps the whole hero on its poster; a world failure only drops the second scene.
  let unavailable = false;
  let failedVariant = '';
  let targetRate = 1;
  let rateFrame = 0;
  let lastRateTime = 0;
  let settleTimer = 0;
  let previousScroll = scrollY;
  let previousScrollTime = performance.now();
  let elapsed = 0;
  let lastTick = 0;
  let clockFrame = 0;
  let switching = false;
  let fadeTimer = 0;

  function prepareVideo(video) {
    video.muted = true;
    video.defaultMuted = true;
    video.playsInline = true;
    video.disablePictureInPicture = true;
  }
  prepareVideo(carVideo);
  hero.dataset.scene = 'car';

  function variantNow() {
    return portrait.matches ? 'mobile' : 'desktop';
  }

  function motionAllowed() {
    return media.dataset.videoEnabled === 'true' && !reducedMotion.matches && !connection?.saveData;
  }

  function shouldPlay() {
    return motionAllowed() && visible && !document.hidden && !unavailable;
  }

  function resetRate() {
    clearTimeout(settleTimer);
    cancelAnimationFrame(rateFrame);
    rateFrame = 0;
    targetRate = 1;
    lastRateTime = 0;
    car.video.playbackRate = 1;
    if (world.video) world.video.playbackRate = 1;
    previousScroll = scrollY;
    previousScrollTime = performance.now();
  }

  function stopClock() {
    cancelAnimationFrame(clockFrame);
    clockFrame = 0;
    lastTick = 0;
  }

  function startClock() {
    if (!clockFrame && shouldPlay()) clockFrame = requestAnimationFrame(tick);
  }

  function pauseAtCurrentFrame() {
    car.video.pause();
    world.video?.pause();
    resetRate();
    stopClock();
    if (media.dataset.videoReady === 'true') media.dataset.mediaState = 'paused';
  }

  // Bring the car back to the front; the world layer fades out over it.
  function returnToCar() {
    clearTimeout(fadeTimer);
    switching = false;
    world.pending = false;
    active = car;
    hero.dataset.scene = 'car';
    world.video?.pause();
    elapsed = 0;
    lastTick = 0;
  }

  function showPoster(state) {
    pauseAtCurrentFrame();
    returnToCar();
    delete media.dataset.videoReady;
    media.dataset.mediaState = state;
  }

  function markUnavailable(state) {
    unavailable = true;
    failedVariant = car.variant;
    car.pending = false;
    showPoster(state);
  }

  function disableWorld() {
    if (world.disabled) return;
    world.disabled = true;
    world.pending = false;
    if (world.video) {
      world.video.pause();
      world.video.removeAttribute('src');
      world.video.load();
    }
    if (active === world || switching) {
      returnToCar();
      requestPlayback(car);
    }
  }

  function ensureWorld() {
    if (world.video) return world.video;
    const layer = document.createElement('div');
    layer.className = 'car-world';
    layer.setAttribute('aria-hidden', 'true');
    const video = document.createElement('video');
    video.className = 'car-world-video';
    prepareVideo(video);
    for (const name of ['muted', 'playsinline', 'disablepictureinpicture', 'disableremoteplayback']) video.setAttribute(name, '');
    video.preload = 'auto';
    video.tabIndex = -1;
    const shade = document.createElement('div');
    shade.className = 'car-world-shade';
    layer.append(video, shade);
    media.append(layer);
    video.addEventListener('error', () => {
      if (video.getAttribute('src')) disableWorld();
    });
    video.addEventListener('playing', () => {
      if (!shouldPlay()) video.pause();
    });
    world.video = video;
    return video;
  }

  // The world file for the current viewport, loaded once the car has been on screen a while.
  function loadWorld() {
    if (world.disabled) return;
    ensureWorld();
    const variant = variantNow();
    if (world.variant === variant) return;
    world.version += 1;
    world.pending = false;
    world.variant = variant;
    world.video.poster = world.posters[variant];
    world.video.src = world.sources[variant];
    world.video.load();
  }

  function requestPlayback(scene) {
    if (!shouldPlay() || scene.pending || !scene.video?.paused) return;
    scene.pending = true;
    const requestVersion = scene.version;
    const attempt = scene.video.play();
    if (!attempt?.then) {
      scene.pending = false;
      return;
    }
    attempt.then(() => {
      if (requestVersion !== scene.version) return;
      scene.pending = false;
      if (!shouldPlay()) pauseAtCurrentFrame();
      else startClock();
    }).catch((error) => {
      if (requestVersion !== scene.version) return;
      scene.pending = false;
      // Pausing an in-flight play request is normal when visibility changes.
      if (error.name === 'AbortError') {
        if (shouldPlay() && active === scene) requestPlayback(scene);
        return;
      }
      if (scene === world) {
        disableWorld();
        return;
      }
      markUnavailable(error.name === 'NotAllowedError' ? 'autoplay-blocked' : 'error');
    });
  }

  function commit(next) {
    const previous = active;
    active = next;
    hero.dataset.scene = next.name;
    elapsed = 0;
    lastTick = 0;
    clearTimeout(fadeTimer);
    fadeTimer = setTimeout(() => {
      switching = false;
      if (active !== previous) previous.video.pause();
    }, FADE_MS);
  }

  function beginSwitch() {
    const next = active === car ? world : car;
    if (next === world) {
      if (world.disabled) {
        // Without the world the car simply keeps looping.
        elapsed = 0;
        return;
      }
      loadWorld();
      // Not buffered yet: the car keeps playing and the switch is retried next frame.
      if (world.video.readyState < 3) return;
    }
    switching = true;
    const requestVersion = next.version;
    try {
      next.video.currentTime = 0;
    } catch {
      // Some browsers refuse a seek before metadata; playback still starts at the beginning.
    }
    next.pending = true;
    Promise.resolve(next.video.play()).then(() => {
      next.pending = false;
      if (requestVersion !== next.version || !switching) return;
      if (!shouldPlay()) {
        next.video.pause();
        switching = false;
        return;
      }
      commit(next);
    }).catch((error) => {
      next.pending = false;
      switching = false;
      if (next === world) disableWorld();
      else if (error?.name !== 'AbortError') markUnavailable(error?.name === 'NotAllowedError' ? 'autoplay-blocked' : 'error');
    });
  }

  // Scene time only advances while the active film is actually playing.
  function tick(now) {
    clockFrame = 0;
    if (!shouldPlay()) {
      lastTick = 0;
      return;
    }
    const video = active.video;
    if (video.paused || video.readyState < 2) {
      lastTick = 0;
      clockFrame = requestAnimationFrame(tick);
      return;
    }
    if (lastTick) elapsed += Math.min(now - lastTick, 100);
    lastTick = now;
    if (!switching) {
      if (active === car && elapsed >= PRELOAD_MS) loadWorld();
      // The world file is a single ten-second pass: leave before it reaches its last frame.
      const nearEnd = active === world && video.duration - video.currentTime < (FADE_MS + 250) / 1000;
      if (elapsed >= SCENE_MS - FADE_MS || nearEnd) beginSwitch();
    }
    clockFrame = requestAnimationFrame(tick);
  }

  function reconcile() {
    if (!motionAllowed()) {
      showPoster('poster');
      return;
    }
    if (!visible || document.hidden) {
      pauseAtCurrentFrame();
      return;
    }
    const variant = variantNow();
    if (unavailable) {
      // A failure stays on its poster until a genuinely different file is selected.
      if (variant === failedVariant) return;
      unavailable = false;
      failedVariant = '';
    }
    if (variant !== car.variant) {
      // A viewport change restarts on the car with the matching file; the world reloads later.
      car.version += 1;
      car.pending = false;
      showPoster('loading');
      car.variant = variant;
      media.dataset.mediaVariant = variant;
      car.video.src = car.sources[variant];
      car.video.load();
    }
    requestPlayback(active);
    startClock();
  }

  function smoothRate(now) {
    rateFrame = 0;
    const video = active.video;
    if (!shouldPlay() || video.paused) {
      resetRate();
      return;
    }
    const elapsedRate = lastRateTime ? Math.min(now - lastRateTime, 80) : 16;
    lastRateTime = now;
    const next = video.playbackRate + (targetRate - video.playbackRate) * (1 - Math.exp(-elapsedRate / 120));
    video.playbackRate = Math.min(1.25, Math.max(0.85, next));
    if (Math.abs(targetRate - next) > 0.002) {
      rateFrame = requestAnimationFrame(smoothRate);
    } else {
      video.playbackRate = targetRate;
      lastRateTime = 0;
    }
  }

  function scheduleRate() {
    if (!rateFrame) rateFrame = requestAnimationFrame(smoothRate);
  }

  window.addEventListener('scroll', () => {
    const now = performance.now();
    const position = scrollY;
    const velocity = (position - previousScroll) / Math.max(now - previousScrollTime, 16);
    previousScroll = position;
    previousScrollTime = now;
    if (!shouldPlay() || active.video.paused) return;
    targetRate = Math.min(1.25, Math.max(0.85, 1 + velocity * 0.15));
    scheduleRate();
    clearTimeout(settleTimer);
    settleTimer = setTimeout(() => {
      targetRate = 1;
      scheduleRate();
    }, 140);
  }, { passive: true });

  carVideo.addEventListener('playing', () => {
    car.pending = false;
    if (!shouldPlay()) {
      if (!motionAllowed() || unavailable) showPoster(unavailable ? 'error' : 'poster');
      else pauseAtCurrentFrame();
      return;
    }
    media.dataset.videoReady = 'true';
    media.dataset.mediaState = 'playing';
    startClock();
  });
  carVideo.addEventListener('error', () => markUnavailable('error'));
  document.addEventListener('visibilitychange', reconcile);
  portrait.addEventListener('change', () => {
    // Switching viewport selects the other file; it never loads both variants upfront.
    reconcile();
  });
  reducedMotion.addEventListener('change', reconcile);
  connection?.addEventListener?.('change', reconcile);
  window.addEventListener('pagehide', pauseAtCurrentFrame);
  window.addEventListener('pageshow', reconcile);

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting && entry.intersectionRatio > 0;
      reconcile();
    }, { threshold: [0, 0.01] }).observe(hero);
  } else {
    window.addEventListener('scroll', () => {
      const bounds = hero.getBoundingClientRect();
      const next = bounds.bottom > 0 && bounds.top < innerHeight;
      if (next !== visible) {
        visible = next;
        reconcile();
      }
    }, { passive: true });
  }
  reconcile();
})();
