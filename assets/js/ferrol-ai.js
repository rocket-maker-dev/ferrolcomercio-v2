/**
 * ferrol-ai.js — Frontend del buscador IA para CCA Ferrol Comercio
 * Widget de chat + buscador con sugerencias + resultados IA
 */
(function() {
  'use strict';

  // ── Config ──────────────────────────────────────────────────────────────
  var _apiMeta = document.querySelector('meta[name="api-base"]');
  var API_BASE = (_apiMeta ? _apiMeta.content : (window.location.origin + '/api')) + '/ferrol-ai.php';
  var _baseMeta = document.querySelector('meta[name="site-base"]');
  var BASE_URL = _baseMeta ? _baseMeta.content : window.location.origin;
  var IMG_BASE = 'https://ferrolcomercio.es/wp-content/';
  var LANG = document.documentElement.lang || 'gl';
  var SUGGEST_DEBOUNCE = 300;
  var MIN_CHARS = 3;

  // ── i18n ────────────────────────────────────────────────────────────────
  var t = {
    gl: {
      chatTitle: 'Asistente CCA Ferrol',
      chatWelcome: '¡Ola! Son o asistente do CCA Ferrol Comercio. ¿En que podo axudarche? Podes preguntarme por calquera comercio, produto ou servizo do barrio da Magdalena.',
      placeholder: 'Onde podo mercar...',
      send: 'Enviar',
      thinking: 'Pensando...',
      error: 'Erro ao procesar. Téntao de novo.',
      viewProfile: 'Ver ficha',
      noResults: 'Non atopei comercios para esa busca. Proba con outros termos.',
      searchResults: 'Resultados da busca',
      askMe: 'Pregúntame',
      category: 'Categoría',
      comercio: 'Comercio',
      searching: 'Buscando...',
      poweredBy: 'Busca con IA'
    },
    es: {
      chatTitle: 'Asistente CCA Ferrol',
      chatWelcome: '¡Hola! Soy el asistente del CCA Ferrol Comercio. ¿En qué puedo ayudarte? Puedes preguntarme por cualquier comercio, producto o servicio del barrio de A Magdalena.',
      placeholder: '¿Dónde puedo comprar...',
      send: 'Enviar',
      thinking: 'Pensando...',
      error: 'Error al procesar. Inténtalo de nuevo.',
      viewProfile: 'Ver ficha',
      noResults: 'No encontré comercios para esa búsqueda. Prueba con otros términos.',
      searchResults: 'Resultados de la búsqueda',
      askMe: 'Pregúntame',
      category: 'Categoría',
      comercio: 'Comercio',
      searching: 'Buscando...',
      poweredBy: 'Búsqueda con IA'
    }
  };
  var txt = t[LANG] || t.gl;

  // ── Utils ───────────────────────────────────────────────────────────────
  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function(k) {
      if (k === 'className') e.className = attrs[k];
      else if (k === 'innerHTML') e.innerHTML = attrs[k];
      else if (k === 'textContent') e.textContent = attrs[k];
      else if (k.startsWith('on')) e.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    if (children) children.forEach(function(c) {
      if (typeof c === 'string') e.appendChild(document.createTextNode(c));
      else if (c) e.appendChild(c);
    });
    return e;
  }

  function debounce(fn, ms) {
    var timer;
    return function() {
      var args = arguments, ctx = this;
      clearTimeout(timer);
      timer = setTimeout(function() { fn.apply(ctx, args); }, ms);
    };
  }

  // ── API Calls ─────────────────────────────────────────────────────────
  function apiSearch(query, callback) {
    fetch(API_BASE + '?action=search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, lang: LANG })
    })
    .then(function(r) { return r.json(); })
    .then(callback)
    .catch(function(err) {
      console.error('Search error:', err);
      callback({ error: true, resposta: txt.error, comercios: [] });
    });
  }

  function apiChat(messages, callback) {
    fetch(API_BASE + '?action=chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: messages, lang: LANG })
    })
    .then(function(r) { return r.json(); })
    .then(callback)
    .catch(function(err) {
      console.error('Chat error:', err);
      callback({ error: true, resposta: txt.error, comercios: [] });
    });
  }

  function apiSuggest(q, callback) {
    fetch(API_BASE + '?action=suggest&q=' + encodeURIComponent(q) + '&lang=' + LANG)
    .then(function(r) { return r.json(); })
    .then(callback)
    .catch(function() { callback({ suggestions: [] }); });
  }

  // ── Render comercio card ──────────────────────────────────────────────
  function renderComercioCard(c, compact) {
    var catLabel = (c.categorias && c.categorias[0]) ? c.categorias[0].replace(/-/g, ' ') : '';
    catLabel = catLabel.charAt(0).toUpperCase() + catLabel.slice(1);
    
    var card = el('a', {
      className: 'ai-comercio-card' + (compact ? ' ai-comercio-card--compact' : ''),
      href: BASE_URL + '/' + LANG + '/comercio/' + c.slug + '/'
    });
    
    if (!compact && c.imagen) {
      var imgWrap = el('div', { className: 'ai-comercio-img' });
      var img = el('img', {
        src: IMG_BASE + c.imagen,
        alt: c.nombre,
        loading: 'lazy'
      });
      img.onerror = function() { this.src = BASE_URL + '/assets/images/header-ferrolcomercio.png'; };
      imgWrap.appendChild(img);
      card.appendChild(imgWrap);
    }
    
    var info = el('div', { className: 'ai-comercio-info' });
    if (catLabel) info.appendChild(el('span', { className: 'ai-comercio-cat', textContent: catLabel }));
    info.appendChild(el('strong', { className: 'ai-comercio-name', textContent: c.nombre }));
    if (c.direccion) info.appendChild(el('span', { className: 'ai-comercio-addr', innerHTML: '<i class="fas fa-map-marker-alt"></i> ' + c.direccion }));
    if (c.telefono) info.appendChild(el('span', { className: 'ai-comercio-tel', innerHTML: '<i class="fas fa-phone"></i> ' + c.telefono }));
    
    var viewBtn = el('span', { className: 'ai-comercio-link', textContent: txt.viewProfile + ' →' });
    info.appendChild(viewBtn);
    card.appendChild(info);
    
    return card;
  }

  // ══════════════════════════════════════════════════════════════════════
  // CHAT WIDGET
  // ══════════════════════════════════════════════════════════════════════
  function initChatWidget() {
    var chatHistory = [];
    var isOpen = false;

    // Create button
    var btn = el('button', {
      className: 'ai-chat-btn',
      'aria-label': txt.askMe,
      innerHTML: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>'
    });

    // Create panel
    var panel = el('div', { className: 'ai-chat-panel', role: 'dialog', 'aria-label': txt.chatTitle });

    // Header
    var header = el('div', { className: 'ai-chat-header' });
    var headerLogo = el('img', {
      src: BASE_URL + '/assets/images/cca-logo-color.png',
      alt: 'CCA Ferrol',
      className: 'ai-chat-logo'
    });
    var headerTitle = el('div', { className: 'ai-chat-header-text' });
    headerTitle.appendChild(el('h3', { textContent: txt.chatTitle }));
    headerTitle.appendChild(el('span', { className: 'ai-chat-status', innerHTML: '<span class="ai-status-dot"></span> Online' }));
    var closeBtn = el('button', { className: 'ai-chat-close', innerHTML: '&times;', 'aria-label': 'Close' });
    header.appendChild(headerLogo);
    header.appendChild(headerTitle);
    header.appendChild(closeBtn);
    panel.appendChild(header);

    // Messages area
    var messagesArea = el('div', { className: 'ai-chat-messages' });
    panel.appendChild(messagesArea);

    // Input form
    var form = el('form', { className: 'ai-chat-form' });
    var input = el('input', {
      type: 'text',
      className: 'ai-chat-input',
      placeholder: txt.placeholder,
      autocomplete: 'off'
    });
    var submitBtn = el('button', {
      type: 'submit',
      className: 'ai-chat-submit',
      innerHTML: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>'
    });
    form.appendChild(input);
    form.appendChild(submitBtn);

    // Powered by
    var powered = el('div', { className: 'ai-chat-powered', innerHTML: '<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> ' + txt.poweredBy });
    
    var formWrap = el('div', { className: 'ai-chat-form-wrap' });
    formWrap.appendChild(form);
    formWrap.appendChild(powered);
    panel.appendChild(formWrap);

    document.body.appendChild(btn);
    document.body.appendChild(panel);

    // Welcome message
    addAIMessage(txt.chatWelcome);

    // Toggle
    function toggle() {
      isOpen = !isOpen;
      panel.classList.toggle('open', isOpen);
      btn.classList.toggle('active', isOpen);
      if (isOpen) {
        input.focus();
        messagesArea.scrollTop = messagesArea.scrollHeight;
      }
    }

    btn.addEventListener('click', toggle);
    closeBtn.addEventListener('click', toggle);

    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && isOpen) toggle();
    });

    // Send message
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var msg = input.value.trim();
      if (!msg) return;

      addUserMessage(msg);
      input.value = '';
      input.disabled = true;
      submitBtn.disabled = true;

      chatHistory.push({ role: 'user', content: msg });
      var thinking = addThinking();

      apiChat(chatHistory, function(data) {
        thinking.remove();
        input.disabled = false;
        submitBtn.disabled = false;
        input.focus();

        var resposta = data.resposta || data.message || txt.error;
        chatHistory.push({ role: 'assistant', content: resposta });
        addAIMessage(resposta, data.comercios);
      });
    });

    function addUserMessage(text) {
      var msg = el('div', { className: 'ai-msg ai-msg--user' });
      msg.appendChild(el('div', { className: 'ai-msg-bubble', textContent: text }));
      messagesArea.appendChild(msg);
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function addAIMessage(text, comercios) {
      var msg = el('div', { className: 'ai-msg ai-msg--ai' });
      var bubble = el('div', { className: 'ai-msg-bubble', textContent: text });
      msg.appendChild(bubble);

      if (comercios && comercios.length > 0) {
        var cards = el('div', { className: 'ai-msg-cards' });
        comercios.forEach(function(c) {
          cards.appendChild(renderComercioCard(c, true));
        });
        msg.appendChild(cards);
      }

      messagesArea.appendChild(msg);
      messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function addThinking() {
      var msg = el('div', { className: 'ai-msg ai-msg--ai ai-msg--thinking' });
      msg.appendChild(el('div', {
        className: 'ai-msg-bubble',
        innerHTML: '<span class="ai-thinking-dots"><span></span><span></span><span></span></span> ' + txt.thinking
      }));
      messagesArea.appendChild(msg);
      messagesArea.scrollTop = messagesArea.scrollHeight;
      return msg;
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // SEARCH BAR ENHANCEMENT (home page)
  // ══════════════════════════════════════════════════════════════════════
  function initSearchEnhancement() {
    var searchForm = document.getElementById('search-form');
    var searchInput = document.getElementById('hero-q');
    if (!searchForm || !searchInput) return;

    // Create suggestions dropdown
    var suggestBox = el('div', { className: 'ai-suggest-box' });
    searchForm.style.position = 'relative';
    searchForm.appendChild(suggestBox);

    // Create results container (below hero)
    var hero = document.querySelector('.site-hero');
    var resultsContainer = el('div', { className: 'ai-search-results', id: 'ai-search-results' });
    if (hero && hero.nextElementSibling) {
      hero.parentNode.insertBefore(resultsContainer, hero.nextElementSibling);
    } else {
      hero.parentNode.appendChild(resultsContainer);
    }

    // Suggestions on typing
    var fetchSuggestions = debounce(function(q) {
      if (q.length < MIN_CHARS) { suggestBox.innerHTML = ''; suggestBox.classList.remove('visible'); return; }
      apiSuggest(q, function(data) {
        suggestBox.innerHTML = '';
        if (!data.suggestions || data.suggestions.length === 0) {
          suggestBox.classList.remove('visible');
          return;
        }
        data.suggestions.forEach(function(s) {
          var item = el('a', {
            className: 'ai-suggest-item',
            href: s.type === 'category' 
              ? BASE_URL + '/' + LANG + '/categoria/' + s.slug + '/'
              : BASE_URL + '/' + LANG + '/comercio/' + s.slug + '/'
          });
          var icon = s.type === 'category' ? 'fas fa-tag' : 'fas fa-store';
          item.innerHTML = '<i class="' + icon + '"></i> <span>' + s.text + '</span><small>' + (s.type === 'category' ? txt.category : txt.comercio) + '</small>';
          
          item.addEventListener('click', function(e) {
            // Let categories/comercios navigate naturally
          });
          
          suggestBox.appendChild(item);
        });
        suggestBox.classList.add('visible');
      });
    }, SUGGEST_DEBOUNCE);

    searchInput.addEventListener('input', function() { fetchSuggestions(this.value.trim()); });
    
    // Close suggestions on click outside
    document.addEventListener('click', function(e) {
      if (!searchForm.contains(e.target)) {
        suggestBox.classList.remove('visible');
      }
    });

    // Submit: IA search
    searchForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var q = searchInput.value.trim();
      if (!q) return;

      suggestBox.classList.remove('visible');
      
      // Show loading
      resultsContainer.innerHTML = '';
      resultsContainer.classList.add('visible');
      var loading = el('div', { className: 'ai-results-loading' });
      loading.innerHTML = '<div class="ai-spinner"></div><p>' + txt.searching + '</p>';
      resultsContainer.appendChild(loading);

      // Scroll to results
      resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

      apiSearch(q, function(data) {
        resultsContainer.innerHTML = '';

        if (data.error && !data.resposta) {
          resultsContainer.innerHTML = '<div class="ai-results-inner"><p class="ai-results-error">' + txt.error + '</p></div>';
          return;
        }

        var inner = el('div', { className: 'ai-results-inner container' });
        
        // Header
        var header = el('div', { className: 'ai-results-header' });
        header.appendChild(el('h2', { textContent: txt.searchResults }));
        var closeResults = el('button', { className: 'ai-results-close', innerHTML: '&times;', 'aria-label': 'Close' });
        closeResults.addEventListener('click', function() { 
          resultsContainer.classList.remove('visible');
          resultsContainer.innerHTML = '';
        });
        header.appendChild(closeResults);
        inner.appendChild(header);

        // AI response text
        if (data.resposta) {
          var respBox = el('div', { className: 'ai-results-response' });
          respBox.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>';
          respBox.appendChild(el('p', { textContent: data.resposta }));
          inner.appendChild(respBox);
        }

        // Comercio cards
        if (data.comercios && data.comercios.length > 0) {
          var grid = el('div', { className: 'ai-results-grid' });
          data.comercios.forEach(function(c) {
            grid.appendChild(renderComercioCard(c, false));
          });
          inner.appendChild(grid);
        } else if (!data.error) {
          inner.appendChild(el('p', { className: 'ai-results-empty', textContent: txt.noResults }));
        }

        resultsContainer.appendChild(inner);
      });
    });
  }

  // ── Init ──────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function() {
    initChatWidget();
    initSearchEnhancement();
  });
})();
