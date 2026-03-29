/**
 * aceternity.js — CCA Ferrol Comercio v2 · Efectos Aceternity-style
 * HTML/CSS/JS puro · Sin dependencias externas
 * Autor: Halo (rocket-maker-dev)
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------ */
  /* 0. Reducción de movimiento                                          */
  /* ------------------------------------------------------------------ */
  var prefersReducedMotion =
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------ */
  /* 1. GLASSMORPHISM NAVBAR — añadir .scrolled al hacer scroll         */
  /* ------------------------------------------------------------------ */
  (function initNavScroll() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    header.classList.add('glass-nav');

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          if (window.scrollY > 40) {
            header.classList.add('scrolled');
          } else {
            header.classList.remove('scrolled');
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  })();

  /* ------------------------------------------------------------------ */
  /* 2. AURORA HERO — generar capas dinámicamente si existe .hero-aurora */
  /* ------------------------------------------------------------------ */
  (function initAurora() {
    var heroAurora = document.querySelector('.hero-aurora');
    if (!heroAurora) return;

    // Verificar si ya tiene .hero-aurora-bg (inyectado desde HTML)
    if (!heroAurora.querySelector('.hero-aurora-bg')) {
      var bg = document.createElement('div');
      bg.className = 'hero-aurora-bg';
      for (var i = 0; i < 5; i++) {
        var layer = document.createElement('div');
        layer.className = 'aurora-layer';
        bg.appendChild(layer);
      }
      var fade = document.createElement('div');
      fade.className = 'hero-aurora-bottom-fade';
      heroAurora.insertBefore(bg, heroAurora.firstChild);
      heroAurora.appendChild(fade);
    }
  })();

  /* ------------------------------------------------------------------ */
  /* 3. SPARKLES — Generar partículas en elementos .sparkle-container    */
  /* ------------------------------------------------------------------ */
  (function initSparkles() {
    if (prefersReducedMotion) return;

    var containers = document.querySelectorAll('.sparkle-container');
    containers.forEach(function (container) {
      var count = parseInt(container.dataset.sparkleCount || '18');
      for (var i = 0; i < count; i++) {
        var s = document.createElement('div');
        s.className = 'sparkle';
        s.style.setProperty('--sparkle-top',   Math.random() * 100 + '%');
        s.style.setProperty('--sparkle-left',  Math.random() * 100 + '%');
        s.style.setProperty('--sparkle-dur',   (2.5 + Math.random() * 4) + 's');
        s.style.setProperty('--sparkle-delay', (Math.random() * 5) + 's');
        container.appendChild(s);
      }
    })
  })();

  /* ------------------------------------------------------------------ */
  /* 4. TYPEWRITER — mejorado con cursor                                 */
  /* ------------------------------------------------------------------ */
  (function initTypewriter() {
    var el = document.querySelector('.hero-typing');
    if (!el) return;

    el.classList.add('hero-typing-cursor');

    var wordsRaw = el.dataset.words || '';
    var words = wordsRaw.split(',').map(function (w) { return w.trim(); }).filter(Boolean);
    if (!words.length) return;

    var idx = 0, charIdx = 0, deleting = false;
    var pauseMs = 2000, typeMs = 85, deleteMs = 50;

    function tick() {
      var word = words[idx % words.length];
      if (!deleting) {
        el.textContent = word.slice(0, ++charIdx);
        if (charIdx >= word.length) {
          deleting = true;
          setTimeout(tick, pauseMs);
          return;
        }
      } else {
        el.textContent = word.slice(0, --charIdx);
        if (charIdx === 0) {
          deleting = false;
          idx++;
          setTimeout(tick, 400);
          return;
        }
      }
      setTimeout(tick, deleting ? deleteMs : typeMs);
    }

    // Solo activar si el base.html no ha iniciado su propio typewriter
    if (!window.__ferrolTypingActive) {
      window.__ferrolTypingActive = true;
      tick();
    }
  })();

  /* ------------------------------------------------------------------ */
  /* 5. SPOTLIGHT ON HOVER — radial-gradient siguiendo el cursor         */
  /* ------------------------------------------------------------------ */
  (function initSpotlight() {
    var cards = document.querySelectorAll('.spotlight-card');
    if (!cards.length) return;

    cards.forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--spotlight-x', x + '%');
        card.style.setProperty('--spotlight-y', y + '%');
      });

      card.addEventListener('mouseleave', function () {
        card.style.setProperty('--spotlight-x', '-100%');
        card.style.setProperty('--spotlight-y', '-100%');
      });
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 6. AC CARD GRID — spotlight individual en cards                     */
  /* ------------------------------------------------------------------ */
  (function initCardSpotlight() {
    var cards = document.querySelectorAll('.ac-comercio-card');
    if (!cards.length) return;

    cards.forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--card-x', x + '%');
        card.style.setProperty('--card-y', y + '%');
      });

      card.addEventListener('mouseleave', function () {
        card.style.setProperty('--card-x', '-100%');
        card.style.setProperty('--card-y', '-100%');
      });
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 7. 3D CARD TILT — perspectiva 3D en hover                           */
  /* ------------------------------------------------------------------ */
  (function initTilt() {
    if (prefersReducedMotion) return;

    var cards = document.querySelectorAll('.tilt-card');
    if (!cards.length) return;

    cards.forEach(function (card) {
      var inner = card.querySelector('.tilt-card-inner') || card;
      var maxTilt = parseFloat(card.dataset.maxTilt || '8');

      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var cx = rect.left + rect.width / 2;
        var cy = rect.top + rect.height / 2;
        var dx = (e.clientX - cx) / (rect.width / 2);
        var dy = (e.clientY - cy) / (rect.height / 2);

        var rotX = -dy * maxTilt;
        var rotY =  dx * maxTilt;

        inner.style.transform =
          'perspective(800px) rotateX(' + rotX + 'deg) rotateY(' + rotY + 'deg) scale3d(1.02, 1.02, 1.02)';

        // Actualizar posición del shine
        var mx = ((e.clientX - rect.left) / rect.width) * 100;
        var my = ((e.clientY - rect.top) / rect.height) * 100;
        inner.style.setProperty('--tilt-mx', mx + '%');
        inner.style.setProperty('--tilt-my', my + '%');
      });

      card.addEventListener('mouseleave', function () {
        inner.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 8. INFINITE MARQUEE — clonar elementos para el loop infinito       */
  /* ------------------------------------------------------------------ */
  (function initMarquee() {
    if (prefersReducedMotion) return;

    var tracks = document.querySelectorAll('.marquee-track');
    tracks.forEach(function (track) {
      // Clonar el contenido para el loop
      var items = track.children;
      if (!items.length) return;

      // Clonar suficientes items para llenar el ancho
      var clone = track.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.parentNode.insertBefore(clone, track.nextSibling);

      // Pausar al hover en el contenedor padre
      var section = track.closest('.marquee-section');
      if (section) {
        section.addEventListener('mouseenter', function () {
          track.style.animationPlayState = 'paused';
          if (clone) clone.style.animationPlayState = 'paused';
        });
        section.addEventListener('mouseleave', function () {
          track.style.animationPlayState = 'running';
          if (clone) clone.style.animationPlayState = 'running';
        });
      }
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 9. FADE-IN REVEAL — Intersection Observer                           */
  /* ------------------------------------------------------------------ */
  (function initReveal() {
    if (prefersReducedMotion) {
      // Si prefiere reducido, mostrar todo directamente
      document.querySelectorAll('.ac-reveal').forEach(function (el) {
        el.classList.add('ac-visible');
      });
      return;
    }

    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('.ac-reveal').forEach(function (el) {
        el.classList.add('ac-visible');
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('ac-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.ac-reveal').forEach(function (el) {
      observer.observe(el);
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 10. BENTO GRID — hover ligero con mouse tracking                    */
  /* ------------------------------------------------------------------ */
  (function initBento() {
    var cells = document.querySelectorAll('.bento-cell');
    if (!cells.length) return;

    cells.forEach(function (cell) {
      cell.addEventListener('mousemove', function (e) {
        var rect = cell.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        cell.style.setProperty('--bento-x', x + '%');
        cell.style.setProperty('--bento-y', y + '%');
      });
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 11. CONTADOR ANIMADO — para stats de hero                           */
  /* ------------------------------------------------------------------ */
  function animateCounter(el) {
    var target = parseInt(el.dataset.target || el.textContent || '0');
    var duration = 1800;
    var start = null;

    function step(ts) {
      if (!start) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
      el.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  (function initCounters() {
    if (prefersReducedMotion) return;
    if (!('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    document.querySelectorAll('[data-counter]').forEach(function (el) {
      el.dataset.target = el.textContent;
      el.textContent = '0';
      observer.observe(el);
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 12. BÚSQUEDA HERO — mejorar UX con clase focus                      */
  /* ------------------------------------------------------------------ */
  (function initSearchFocus() {
    var searchWrap = document.querySelector('.ac-search-wrap');
    var searchInput = document.querySelector('.ac-search-input, .hero-search-input');
    if (!searchWrap || !searchInput) return;

    searchInput.addEventListener('focus', function () {
      searchWrap.classList.add('is-focused');
    });

    searchInput.addEventListener('blur', function () {
      searchWrap.classList.remove('is-focused');
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 13. GALERÍA FICHA — lightbox sencillo                               */
  /* ------------------------------------------------------------------ */
  (function initGallery() {
    var galleryItems = document.querySelectorAll('.gallery-item img');
    if (!galleryItems.length) return;

    // Crear overlay
    var overlay = document.createElement('div');
    overlay.style.cssText = [
      'position:fixed', 'inset:0', 'z-index:9999',
      'background:rgba(2,11,24,0.92)',
      'display:flex', 'align-items:center', 'justify-content:center',
      'cursor:zoom-out', 'opacity:0',
      'transition:opacity 250ms ease',
      'backdrop-filter:blur(8px)',
      '-webkit-backdrop-filter:blur(8px)'
    ].join(';');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('role', 'dialog');
    overlay.style.display = 'none';

    var overlayImg = document.createElement('img');
    overlayImg.style.cssText = [
      'max-width:90vw', 'max-height:88vh',
      'border-radius:12px',
      'box-shadow:0 32px 80px rgba(0,0,0,0.5)',
      'transition:transform 300ms cubic-bezier(0.16,1,0.3,1)',
      'transform:scale(0.92)'
    ].join(';');
    overlay.appendChild(overlayImg);
    document.body.appendChild(overlay);

    function openLightbox(src, alt) {
      overlayImg.src = src;
      overlayImg.alt = alt || '';
      overlay.style.display = 'flex';
      requestAnimationFrame(function () {
        overlay.style.opacity = '1';
        overlayImg.style.transform = 'scale(1)';
      });
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      overlay.style.opacity = '0';
      overlayImg.style.transform = 'scale(0.92)';
      setTimeout(function () {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
      }, 250);
    }

    galleryItems.forEach(function (img) {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', function () {
        openLightbox(img.src, img.alt);
      });
    });

    overlay.addEventListener('click', closeLightbox);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.style.display !== 'none') {
        closeLightbox();
      }
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 14. COPY LINK — botón compartir                                     */
  /* ------------------------------------------------------------------ */
  (function initCopyLink() {
    var btns = document.querySelectorAll('[data-copy]');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var url = btn.dataset.copy;
        if (!url) return;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(url).then(function () {
            var orig = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i>';
            btn.style.background = '#38a169';
            setTimeout(function () {
              btn.innerHTML = orig;
              btn.style.background = '';
            }, 2200);
          });
        }
      });
    });
  })();

  /* ------------------------------------------------------------------ */
  /* 15. SCROLL PROGRESS BAR en ficha                                    */
  /* ------------------------------------------------------------------ */
  (function initScrollProgress() {
    var bar = document.querySelector('.scroll-progress-bar');
    if (!bar) return;

    window.addEventListener('scroll', function () {
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      var progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(progress, 100) + '%';
    }, { passive: true });
  })();

})();
