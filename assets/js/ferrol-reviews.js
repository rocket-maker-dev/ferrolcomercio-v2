// Load Google reviews for the current ficha page
(function() {
  const section = document.querySelector('.reviews-section[data-place-id]');
  if (!section) return;
  
  const placeId = section.dataset.placeId;
  // API endpoint - relative path works from both preview and production
  const apiBase = document.querySelector('meta[name="api-base"]')?.content || '/cca-preview/api';
  
  // Load rating + reviews
  Promise.all([
    fetch(`${apiBase}/ferrol-reviews.php?action=details&place_id=${placeId}`).then(r => r.json()),
    fetch(`${apiBase}/ferrol-reviews.php?action=reviews&place_id=${placeId}`).then(r => r.json())
  ]).then(([details, reviewsData]) => {
    // Rating summary
    if (details.rating) {
      document.getElementById('rating-value').textContent = details.rating.toFixed(1);
      document.getElementById('rating-stars').innerHTML = renderStars(details.rating);
      document.getElementById('rating-count').textContent = 
        `${details.totalReviews || ''} reseñas`;
    }
    
    // Reviews list
    const list = document.getElementById('reviews-list');
    const reviews = reviewsData.reviews || [];
    
    if (reviews.length === 0) {
      list.innerHTML = '<p class="no-reviews">Aínda non hai reseñas.</p>';
      return;
    }
    
    list.innerHTML = reviews.map(r => `
      <div class="review-card">
        <div class="review-header">
          <img src="${r.profile_photo_url || ''}" alt="${r.author_name}" 
               class="review-avatar" onerror="this.style.display='none'">
          <div class="review-meta">
            <strong class="review-author">${r.author_name}</strong>
            <div class="review-stars">${renderStars(r.rating)}</div>
            <span class="review-time">${r.relative_time_description || ''}</span>
          </div>
        </div>
        <p class="review-text">${r.text || ''}</p>
      </div>
    `).join('');
    
  }).catch(err => {
    const list = document.getElementById('reviews-list');
    if (list) list.innerHTML = '';
    console.warn('Reviews not loaded:', err);
  });
  
  function renderStars(rating) {
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.5 ? 1 : 0;
    const empty = 5 - full - half;
    return '★'.repeat(full) + (half ? '☆' : '') + '☆'.repeat(empty);
  }
})();
