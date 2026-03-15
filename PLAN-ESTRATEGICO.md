# Plan Estratégico — ferrolcomercio.es v2

## Centro Comercial Abierto del Barrio de A Magdalena, Ferrol

**Versión:** 1.0 · **Fecha:** 7 de marzo de 2026  
**Preparado por:** Rocket Lanzadera Digital  
**Cliente:** CCA Ferrol Comercio

---

## 1. Resumen Ejecutivo

El proyecto **ferrolcomercio.es v2** transforma la web actual (WordPress + Listeo) en un directorio web de alto rendimiento construido con HTML estático y PHP backend ligero. Las Fases 1 y 2 ya están completadas: se han extraído los 116 comercios, 39 categorías, y se ha generado un sitio estático básico funcional.

**Las 5 fases restantes cubren:**

| Fase | Qué | Duración estimada |
|------|------|-------------------|
| **3** | Identidad visual definitiva + Header/Footer completos | 3-4 días |
| **4** | Integración Google Business (reseñas, mapas, Place IDs) | 4-5 días |
| **5** | Buscador inteligente con IA (bilingüe gl/es) | 3-4 días |
| **6** | Escaparate Boutique + funcionalidades extra | 5-6 días |
| **7** | SEO bilingüe + migración + lanzamiento | 3-4 días |

**Coste mensual estimado en producción:** 5-15 €/mes (APIs + hosting ya existente)  
**Tiempo total estimado:** 18-23 días de trabajo de IA  
**Inversión tecnológica inicial (APIs):** ~0 € (dentro del crédito gratuito de Google)

---

## 2. Estado Actual (Fases 1-2 completadas)

### Lo que ya existe:
- ✅ **116 comercios** extraídos en `comercios.json` con estructura completa
- ✅ **91 comercios** ya tienen `google_place_id` asignado (78%)
- ✅ **39 categorías** con slugs y jerarquía
- ✅ **371 imágenes** inventariadas (0 missing)
- ✅ **Generador estático** (`build.py`) con Jinja2, soporte bilingüe gl/es, `--base-url`
- ✅ **Preview online** en `rocketmaker.app/cca-preview/`
- ✅ **Templates base**: home, ficha, categoría, 404, base
- ✅ **Branding base**: Raleway + Open Sans, color #0663ac

### Datos de calidad de los comercios:
| Dato | Disponible | Faltante |
|------|-----------|----------|
| Teléfono | 84 | 13 |
| Web | 61 | 36 |
| Coordenadas | ~91 | ~25 |
| Horarios | 82 | 15 |
| Imágenes | 84 | 13 |
| Google Place ID | 91 | 25 |
| Email | 0 | 116 |

---

## 3. FASE 3: Identidad Visual + Header Completo

### 3.1 Objetivo
Implementar la identidad visual definitiva de CCA Ferrol Comercio con el header, hero y footer completos según las directrices del cliente.

### 3.2 Estructura del Header

```
┌──────────────────────────────────────────────────────────────────┐
│ [Logo CCA]    │  Inicio · Comercios · Mapa · Noticias  │  𝓐 𝓜𝓪𝓰𝓭𝓪𝓵𝓮𝓷𝓪  │ GL|ES │
│  ferrol       │         · Contacto                      │                     │       │
│  comercio     │                                         │                     │       │
└──────────────────────────────────────────────────────────────────┘
```

**Distribución CSS (flexbox):**
- **Izquierda:** Logo CCA (`cca-ferrol-comercio-color.png`, height: 48px)
- **Centro:** Menú principal (Raleway 600, 15px, uppercase, letter-spacing 0.5px)
- **Derecha:** Firma "A Magdalena" (script cursivo) + Selector idioma GL|ES

### 3.3 Firma "A Magdalena"

La firma es un elemento de identidad clave. Implementación con CSS custom:

```css
/* Firma "A Magdalena" — script cursivo con subrayado */
.firma-magdalena {
  font-family: 'Dancing Script', cursive; /* Google Font alternativa */
  font-size: 1.3rem;
  color: #ffffff;
  position: relative;
  white-space: nowrap;
  padding-bottom: 4px;
}

.firma-magdalena::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #ffffff 20%, #ffffff 80%, transparent);
}
```

**Alternativas tipográficas para la firma (Google Fonts):**
1. `Dancing Script` — cursiva elegante, muy legible
2. `Great Vibes` — más caligráfica, estilo script formal
3. `Parisienne` — fina y delicada
4. `Alex Brush` — script suave

**Recomendación:** `Dancing Script` (700 weight) por legibilidad en mobile y carga rápida.

**Decisión del cliente requerida:** Aprobar la fuente de la firma o proporcionar un SVG/imagen específica.

### 3.4 Header CSS completo

```css
/* ===== HEADER ===== */
.site-header {
  background-color: #0663ac;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 72px;
}

/* Logo */
.header-logo img {
  height: 48px;
  width: auto;
}

/* Menú central */
.header-nav {
  display: flex;
  gap: 32px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.header-nav a {
  font-family: 'Raleway', sans-serif;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #ffffff;
  text-decoration: none;
  transition: opacity 0.2s;
}

.header-nav a:hover,
.header-nav a.active {
  opacity: 0.85;
  border-bottom: 2px solid #fff;
  padding-bottom: 4px;
}

/* Zona derecha: firma + idioma */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.lang-switch {
  font-family: 'Raleway', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.lang-switch a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
}

.lang-switch a.active {
  color: #ffffff;
}

/* Mobile hamburger */
@media (max-width: 768px) {
  .header-nav { display: none; }
  .firma-magdalena { display: none; }
  .mobile-toggle { display: block; }
}
```

### 3.5 Hero Section

```html
<section class="hero">
  <div class="hero-bg" style="background-image: url('assets/images/header-ferrolcomercio.png')"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <h1>Descubre o comercio do barrio de A Magdalena</h1>
    <p>116 comercios, un barrio con alma</p>
    <div class="hero-search">
      <input type="text" placeholder="Busca un comercio, categoría ou servizo..." id="hero-search-input">
      <button type="submit"><i class="fas fa-search"></i></button>
    </div>
  </div>
</section>
```

```css
.hero {
  position: relative;
  height: 480px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(6, 99, 172, 0.7) 0%, rgba(6, 99, 172, 0.85) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #fff;
  padding-top: 140px;
}

.hero-content h1 {
  font-family: 'Raleway', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.hero-search {
  max-width: 560px;
  margin: 32px auto 0;
  display: flex;
  background: #fff;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.hero-search input {
  flex: 1;
  border: none;
  padding: 16px 24px;
  font-family: 'Open Sans', sans-serif;
  font-size: 16px;
  outline: none;
}

.hero-search button {
  background: #0663ac;
  color: #fff;
  border: none;
  padding: 16px 24px;
  cursor: pointer;
  font-size: 18px;
}
```

### 3.6 Cards Estilo Listeo

```css
.card-comercio {
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: box-shadow 0.3s, transform 0.2s;
}

.card-comercio:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.14);
  transform: translateY(-2px);
}

.card-comercio .card-img {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.card-comercio .card-category {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #0663ac;
  color: #fff;
  font-family: 'Raleway', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 3px;
}

.card-comercio .card-body {
  padding: 20px;
}

.card-comercio h3 {
  font-family: 'Raleway', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.card-comercio .card-address {
  font-family: 'Open Sans', sans-serif;
  font-size: 0.85rem;
  color: #777;
  margin-bottom: 12px;
}

.card-comercio .card-rating {
  color: #f5a623;
  font-size: 0.9rem;
}
```

### 3.7 Footer

```html
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-col">
      <img src="assets/images/cca-ferrol-comercio-color.png" alt="CCA Ferrol Comercio" class="footer-logo">
      <p>Centro Comercial Aberto do Barrio de A Magdalena, Ferrol</p>
    </div>
    <div class="footer-col">
      <h4>Navegación</h4>
      <ul>
        <li><a href="/comercios/">Comercios</a></li>
        <li><a href="/categorias/">Categorías</a></li>
        <li><a href="/mapa/">Mapa</a></li>
        <li><a href="/contacto/">Contacto</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contacto</h4>
      <p>📍 Barrio de A Magdalena, Ferrol</p>
      <p>📧 info@ferrolcomercio.es</p>
      <div class="footer-social">
        <a href="#"><i class="fab fa-facebook-f"></i></a>
        <a href="#"><i class="fab fa-instagram"></i></a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul>
        <li><a href="/aviso-legal/">Aviso Legal</a></li>
        <li><a href="/privacidade/">Privacidade</a></li>
        <li><a href="/cookies/">Cookies</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 CCA Ferrol Comercio. Todos os dereitos reservados.</p>
    <p class="footer-credit">Desenvolvido por <a href="https://rocketlanzadera.com">Rocket</a></p>
  </div>
</footer>
```

### 3.8 Modificaciones en build.py

Cambios necesarios en el generador:
1. Actualizar `base.html` con el nuevo header/footer
2. Añadir Google Fonts: Raleway (400, 600, 700), Open Sans (400, 600), Dancing Script (700)
3. Incluir Font Awesome 6 (CDN: `cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css`)
4. Separar CSS en archivos modulares: `base.css`, `header.css`, `cards.css`, `hero.css`, `footer.css`
5. Añadir template `mobile-menu.html` con hamburger icon + slide-in menu

### 3.9 Estimación Fase 3

| Tarea | Horas |
|-------|-------|
| Header + firma + logo | 4h |
| Hero section | 2h |
| Cards Listeo-style | 2h |
| Footer completo | 2h |
| Mobile responsive | 4h |
| Integrar en build.py + templates | 4h |
| Testing + ajustes | 3h |
| **Total** | **~21h (3 días IA)** |

---

## 4. FASE 4: Integración Google Business

### 4.1 Objetivo
Conectar cada comercio con su Google Business Profile: mostrar reseñas reales, rating, horarios verificados, y enlace directo a Google Maps.

### 4.2 Obtención de Place IDs (25 comercios restantes)

**Estado actual:** 91 de 116 comercios ya tienen `google_place_id`.

Para los 25 restantes, script Python con Google Places API (New):

```python
#!/usr/bin/env python3
"""
resolve_place_ids.py — Obtiene Place IDs faltantes via Text Search API
"""
import json
import requests
import time

API_KEY = "GOOGLE_MAPS_API_KEY"
SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

def buscar_place_id(nombre_comercio, direccion=None):
    """Busca Place ID por nombre del comercio en Ferrol"""
    query = f"{nombre_comercio} Ferrol A Magdalena"
    if direccion:
        query = f"{nombre_comercio} {direccion}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress"
    }
    
    resp = requests.post(SEARCH_URL, json={"textQuery": query}, headers=headers)
    data = resp.json()
    
    if data.get("places"):
        place = data["places"][0]
        return place["id"]  # Este es el Place ID
    return None

# Cargar comercios
with open("data/comercios.json") as f:
    comercios = json.load(f)

# Resolver solo los que faltan
sin_place_id = [c for c in comercios if not c.get("google_place_id")]
print(f"Comercios sin Place ID: {len(sin_place_id)}")

for comercio in sin_place_id:
    nombre = comercio["nombre"]["es"] or comercio["nombre"]["gl"]
    place_id = buscar_place_id(nombre, comercio.get("direccion"))
    
    if place_id:
        comercio["google_place_id"] = place_id
        print(f"  ✅ {nombre} → {place_id}")
    else:
        print(f"  ❌ {nombre} — no encontrado")
    
    time.sleep(0.5)  # Rate limiting

# Guardar actualizado
with open("data/comercios.json", "w") as f:
    json.dump(comercios, f, ensure_ascii=False, indent=2)
```

**Coste estimado:** 25 búsquedas × $0.032 = $0.80 (dentro del crédito gratuito de $200/mes)

### 4.3 Esquema MySQL para Reseñas Cacheadas

```sql
-- Base de datos: ferrolcomercio_db

CREATE TABLE comercios_google (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comercio_slug VARCHAR(255) NOT NULL UNIQUE,
    place_id VARCHAR(255),
    google_rating DECIMAL(2,1),
    google_total_reviews INT DEFAULT 0,
    google_maps_url VARCHAR(500),
    horarios_google JSON,
    ultima_sync DATETIME,
    estado ENUM('activo', 'sin_google', 'error') DEFAULT 'activo',
    INDEX idx_slug (comercio_slug),
    INDEX idx_place_id (place_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE resenas_google (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comercio_slug VARCHAR(255) NOT NULL,
    autor VARCHAR(255),
    autor_foto VARCHAR(500),
    rating TINYINT UNSIGNED,         -- 1-5
    texto TEXT,
    texto_original TEXT,             -- Si es traducida por Google
    idioma VARCHAR(10),
    fecha_publicacion VARCHAR(50),   -- "hace 2 meses" (relativo de Google)
    fecha_sync DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_comercio (comercio_slug),
    FOREIGN KEY (comercio_slug) REFERENCES comercios_google(comercio_slug)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4.4 Sincronización de Reseñas — Cron PHP

```php
<?php
/**
 * sync_reviews.php — Cron diario para sincronizar reseñas de Google
 * Ejecutar: php sync_reviews.php (o vía cron de Hostinger)
 * 
 * Hostinger cron: 0 4 * * * /usr/bin/php /home/u297969817/domains/ferrolcomercio.es/sync_reviews.php
 */

define('API_KEY', 'GOOGLE_MAPS_API_KEY');
define('FIELDS', 'id,displayName,rating,userRatingCount,reviews,currentOpeningHours,googleMapsUri');

$db = new PDO(
    'mysql:host=localhost;dbname=ferrolcomercio_db;charset=utf8mb4',
    'u297969817_ferrol',
    'DB_PASSWORD'
);

// Cargar comercios con Place ID
$comercios = $db->query("SELECT comercio_slug, place_id FROM comercios_google WHERE place_id IS NOT NULL AND estado = 'activo'")->fetchAll(PDO::FETCH_ASSOC);

$synced = 0;
$errors = 0;

foreach ($comercios as $com) {
    $url = "https://places.googleapis.com/v1/places/{$com['place_id']}";
    
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            "X-Goog-Api-Key: " . API_KEY,
            "X-Goog-FieldMask: " . FIELDS
        ]
    ]);
    
    $response = json_decode(curl_exec($ch), true);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode !== 200) {
        $errors++;
        error_log("Error syncing {$com['comercio_slug']}: HTTP {$httpCode}");
        continue;
    }
    
    // Actualizar datos del comercio
    $stmt = $db->prepare("UPDATE comercios_google SET 
        google_rating = ?, 
        google_total_reviews = ?, 
        google_maps_url = ?,
        horarios_google = ?,
        ultima_sync = NOW() 
        WHERE comercio_slug = ?");
    
    $stmt->execute([
        $response['rating'] ?? null,
        $response['userRatingCount'] ?? 0,
        $response['googleMapsUri'] ?? null,
        json_encode($response['currentOpeningHours'] ?? null),
        $com['comercio_slug']
    ]);
    
    // Borrar reseñas antiguas y guardar nuevas
    $db->prepare("DELETE FROM resenas_google WHERE comercio_slug = ?")->execute([$com['comercio_slug']]);
    
    if (!empty($response['reviews'])) {
        $ins = $db->prepare("INSERT INTO resenas_google 
            (comercio_slug, autor, autor_foto, rating, texto, texto_original, idioma, fecha_publicacion) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
        
        foreach (array_slice($response['reviews'], 0, 5) as $review) {
            $ins->execute([
                $com['comercio_slug'],
                $review['authorAttribution']['displayName'] ?? 'Anónimo',
                $review['authorAttribution']['photoUri'] ?? null,
                $review['rating'] ?? null,
                $review['text']['text'] ?? null,
                $review['originalText']['text'] ?? null,
                $review['originalText']['languageCode'] ?? 'es',
                $review['relativePublishTimeDescription'] ?? null
            ]);
        }
    }
    
    $synced++;
    usleep(200000); // 200ms entre requests
}

echo "Sync completado: {$synced} OK, {$errors} errores\n";
```

### 4.5 API de Reseñas (endpoint PHP para el frontend)

```php
<?php
// api/reviews.php?slug=zapateria-ejemplo
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: public, max-age=3600'); // 1h cache

$slug = $_GET['slug'] ?? '';
if (!$slug || !preg_match('/^[a-z0-9\-]+$/', $slug)) {
    http_response_code(400);
    echo json_encode(['error' => 'slug inválido']);
    exit;
}

$db = new PDO('mysql:host=localhost;dbname=ferrolcomercio_db;charset=utf8mb4', 'user', 'pass');

// Datos del comercio
$com = $db->prepare("SELECT google_rating, google_total_reviews, google_maps_url 
    FROM comercios_google WHERE comercio_slug = ?");
$com->execute([$slug]);
$info = $com->fetch(PDO::FETCH_ASSOC);

if (!$info) {
    echo json_encode(['rating' => null, 'reviews' => []]);
    exit;
}

// Reseñas
$rev = $db->prepare("SELECT autor, autor_foto, rating, texto, fecha_publicacion 
    FROM resenas_google WHERE comercio_slug = ? ORDER BY rating DESC LIMIT 5");
$rev->execute([$slug]);
$reviews = $rev->fetchAll(PDO::FETCH_ASSOC);

echo json_encode([
    'rating' => (float)$info['google_rating'],
    'totalReviews' => (int)$info['google_total_reviews'],
    'mapsUrl' => $info['google_maps_url'],
    'reviews' => $reviews
], JSON_UNESCAPED_UNICODE);
```

### 4.6 Componente de Reseñas en la Ficha del Comercio

```html
<!-- En ficha.html (template Jinja2) -->
<section class="ficha-reviews" id="reviews-section" data-slug="{{ comercio.slug }}">
  <h2>Opiniones en Google</h2>
  <div class="reviews-summary">
    <div class="rating-big">
      <span class="rating-number" id="google-rating">—</span>
      <div class="rating-stars" id="google-stars"></div>
      <span class="rating-count" id="google-count"></span>
    </div>
    <a href="#" id="google-maps-link" class="btn-maps" target="_blank">
      <i class="fas fa-map-marker-alt"></i> Ver en Google Maps
    </a>
    <a href="#" id="google-review-link" class="btn-review" target="_blank">
      <i class="fas fa-star"></i> Deixar unha opinión
    </a>
  </div>
  <div class="reviews-list" id="reviews-list">
    <!-- Cargado via JS -->
  </div>
</section>
```

```javascript
// reviews.js — Carga reseñas desde API
document.addEventListener('DOMContentLoaded', () => {
  const section = document.getElementById('reviews-section');
  if (!section) return;
  
  const slug = section.dataset.slug;
  
  fetch(`/api/reviews.php?slug=${slug}`)
    .then(r => r.json())
    .then(data => {
      if (!data.rating) {
        section.style.display = 'none';
        return;
      }
      
      document.getElementById('google-rating').textContent = data.rating.toFixed(1);
      document.getElementById('google-count').textContent = `(${data.totalReviews} opiniones)`;
      document.getElementById('google-stars').innerHTML = renderStars(data.rating);
      
      if (data.mapsUrl) {
        document.getElementById('google-maps-link').href = data.mapsUrl;
        // Link para dejar reseña: añadir /review al URL de Google Maps
        document.getElementById('google-review-link').href = 
          data.mapsUrl.replace('/place/', '/place//review/');
      }
      
      const list = document.getElementById('reviews-list');
      list.innerHTML = data.reviews.map(r => `
        <div class="review-card">
          <div class="review-header">
            <img src="${r.autor_foto || '/assets/images/avatar-default.svg'}" 
                 alt="${r.autor}" class="review-avatar">
            <div>
              <strong>${r.autor}</strong>
              <div class="review-stars">${renderStars(r.rating)}</div>
            </div>
            <span class="review-date">${r.fecha_publicacion}</span>
          </div>
          <p class="review-text">${r.texto || ''}</p>
        </div>
      `).join('');
    });
});

function renderStars(rating) {
  let html = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= rating) html += '<i class="fas fa-star"></i>';
    else if (i - 0.5 <= rating) html += '<i class="fas fa-star-half-alt"></i>';
    else html += '<i class="far fa-star"></i>';
  }
  return html;
}
```

### 4.7 Costes y Límites de Google Places API (New)

| Operación | Coste por llamada | Uso mensual estimado | Coste mensual |
|-----------|-------------------|----------------------|---------------|
| Text Search (resolver Place IDs) | $0.032 | 25 llamadas (una vez) | $0.80 |
| Place Details (sync reseñas) | $0.017 (Basic) | 116/día × 30 = 3,480 | $59.16 |
| **Total mensual** | | | **~$60** |

**Con el crédito gratuito de $200/mes de Google Maps Platform: $0 real.**

**Optimización para mantenerlo gratis:**
- Sync **semanal** en vez de diario: 116 × 4 = 464 llamadas/mes → $7.89/mes ✅
- Sync **cada 3 días**: 116 × 10 = 1,160 → $19.72/mes ✅
- **Recomendación:** Sync **cada 3 días** (reseñas no cambian a diario)

### 4.8 Comercios sin Google Business

Para los ~25 comercios sin Place ID:
1. **Fallback**: mostrar datos propios (del JSON) sin sección de reseñas
2. **Solución propuesta al CCA**: desde la asociación, ayudar a esos comercios a crear su Google Business Profile (beneficia a todos)
3. **Estado visual**: badge "Pendiente de verificación Google" en su ficha

### 4.9 Estimación Fase 4

| Tarea | Horas |
|-------|-------|
| Script resolve_place_ids.py | 2h |
| Schema MySQL + setup Hostinger | 2h |
| sync_reviews.php + cron | 4h |
| API endpoint reviews.php | 2h |
| Frontend reviews component | 4h |
| Botón "Ver en Maps" + "Dejar reseña" | 2h |
| Integrar en build.py templates | 3h |
| Testing + edge cases | 3h |
| **Total** | **~22h (4 días IA)** |

---

## 5. FASE 5: Buscador Inteligente con IA

### 5.1 Análisis de Opciones

Para **116 comercios**, el dataset es pequeño. Evaluamos tres approaches:

| Approach | Pros | Contras | Coste/mes |
|----------|------|---------|-----------|
| **A) Embeddings pre-calculados** | Rápido, sin latencia LLM, barato | Requiere server-side similarity | ~$0.01 |
| **B) LLM directo (Claude/GPT)** | Respuestas naturales, entiende gallego | Latencia 1-3s, coste por query | $5-20 |
| **C) Híbrido: embeddings + LLM** | Lo mejor de ambos | Más complejo | $3-10 |

### 5.2 Arquitectura Recomendada: Híbrido Ligero (Opción C simplificada)

Para 116 comercios, la solución más eficiente es:

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│  Frontend   │────▶│  PHP API         │────▶│  Archivo JSON  │
│  (búsqueda) │     │  search.php      │     │  embeddings    │
└─────────────┘     │                  │     │  precalculados │
                    │  1. Cosine sim   │     └────────────────┘
                    │  2. Si score < X │
                    │     → Claude API │
                    └──────────────────┘
```

**Por qué no usar un vector DB:** Con solo 116 comercios, el archivo JSON de embeddings cabe en ~500KB. Un vector DB (Pinecone, Qdrant) es overkill.

### 5.3 Paso 1: Pre-calcular Embeddings

```python
#!/usr/bin/env python3
"""
generate_embeddings.py — Genera embeddings para todos los comercios
Ejecutar UNA VEZ (o cuando cambien los datos)
"""
import json
import openai

client = openai.OpenAI(api_key="OPENAI_API_KEY")

with open("data/comercios.json") as f:
    comercios = json.load(f)

embeddings_data = []

for com in comercios:
    # Crear texto enriquecido para embedding (bilingüe)
    nombre = com["nombre"]["es"] or com["nombre"]["gl"] or ""
    categorias = ", ".join(com.get("categorias", []))
    direccion = com.get("direccion", "")
    descripcion_es = com.get("descripcion", {}).get("es", "") or ""
    descripcion_gl = com.get("descripcion", {}).get("gl", "") or ""
    
    # Texto combinado para el embedding
    text = f"""
    {nombre}. 
    Categorías: {categorias}. 
    Dirección: {direccion}.
    {descripcion_es}
    {descripcion_gl}
    """.strip()
    
    # Generar embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=256  # Reducido para eficiencia (suficiente para 116 docs)
    )
    
    embeddings_data.append({
        "slug": com["slug"],
        "nombre": nombre,
        "categorias": categorias,
        "direccion": direccion,
        "telefono": com.get("telefono"),
        "web": com.get("web"),
        "embedding": response.data[0].embedding
    })

with open("data/embeddings.json", "w") as f:
    json.dump(embeddings_data, f)

print(f"Generados {len(embeddings_data)} embeddings")
```

**Coste:** 116 comercios × ~200 tokens cada uno = ~23,200 tokens → **$0.0005** (prácticamente gratis)

### 5.4 Paso 2: API de Búsqueda Semántica (PHP)

```php
<?php
/**
 * api/search.php — Buscador semántico
 * GET /api/search.php?q=zapatos+de+señora&lang=gl
 */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=60');

$query = trim($_GET['q'] ?? '');
$lang = $_GET['lang'] ?? 'gl';

if (strlen($query) < 2) {
    echo json_encode(['results' => [], 'mode' => 'empty']);
    exit;
}

// Paso 1: Búsqueda por texto simple (fuzzy match)
$comercios = json_decode(file_get_contents(__DIR__ . '/../data/comercios.json'), true);
$textResults = buscarPorTexto($comercios, $query);

// Si la búsqueda textual da buenos resultados, devolver directamente
if (count($textResults) >= 3) {
    echo json_encode(['results' => array_slice($textResults, 0, 10), 'mode' => 'text']);
    exit;
}

// Paso 2: Búsqueda semántica con embeddings
$embeddings = json_decode(file_get_contents(__DIR__ . '/../data/embeddings.json'), true);
$queryEmbedding = getEmbedding($query);

$scored = [];
foreach ($embeddings as $item) {
    $score = cosineSimilarity($queryEmbedding, $item['embedding']);
    $scored[] = array_merge($item, ['score' => $score]);
}

usort($scored, fn($a, $b) => $b['score'] <=> $a['score']);
$results = array_slice($scored, 0, 10);

// Eliminar embeddings del output
$results = array_map(function($r) {
    unset($r['embedding']);
    return $r;
}, $results);

echo json_encode(['results' => $results, 'mode' => 'semantic']);

// ─── Funciones ───

function getEmbedding($text) {
    $ch = curl_init('https://api.openai.com/v1/embeddings');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . getenv('OPENAI_API_KEY')
        ],
        CURLOPT_POSTFIELDS => json_encode([
            'model' => 'text-embedding-3-small',
            'input' => $text,
            'dimensions' => 256
        ])
    ]);
    $resp = json_decode(curl_exec($ch), true);
    curl_close($ch);
    return $resp['data'][0]['embedding'];
}

function cosineSimilarity($a, $b) {
    $dot = 0; $normA = 0; $normB = 0;
    for ($i = 0; $i < count($a); $i++) {
        $dot += $a[$i] * $b[$i];
        $normA += $a[$i] * $a[$i];
        $normB += $b[$i] * $b[$i];
    }
    return $dot / (sqrt($normA) * sqrt($normB));
}

function buscarPorTexto($comercios, $query) {
    $query = mb_strtolower($query);
    $results = [];
    
    foreach ($comercios as $com) {
        $nombre = mb_strtolower($com['nombre']['es'] ?? $com['nombre']['gl'] ?? '');
        $cats = mb_strtolower(implode(' ', $com['categorias'] ?? []));
        $dir = mb_strtolower($com['direccion'] ?? '');
        
        $haystack = "$nombre $cats $dir";
        
        if (str_contains($haystack, $query)) {
            $results[] = [
                'slug' => $com['slug'],
                'nombre' => $com['nombre']['es'] ?? $com['nombre']['gl'],
                'categorias' => implode(', ', $com['categorias'] ?? []),
                'direccion' => $com['direccion'] ?? '',
                'score' => 1.0
            ];
        }
    }
    
    return $results;
}
```

### 5.5 Soporte Bilingüe Gallego/Español

El buscador maneja gallego de forma nativa porque:

1. **Los embeddings ya incluyen ambos idiomas** en el texto de entrada
2. **`text-embedding-3-small`** entiende gallego (basado en corpus multilingual que incluye pt/gl/es)
3. **Ejemplo real:**

| Query del usuario | Resultados esperados |
|-------------------|---------------------|
| "zapatos de señora" | Zapaterías (match directo) |
| "¿Onde podo mercar zapatos de señora?" | Mismas zapaterías (semántica) |
| "comer un buen pulpo" | Restaurantes con cocina gallega |
| "peluquería barata" | Peluquerías del directorio |
| "sitio para tomar café con wifi" | Cafeterías con feature "wireless-internet" |

### 5.6 Frontend del Buscador

```javascript
// search.js — Búsqueda en tiempo real desde el hero
const searchInput = document.getElementById('hero-search-input');
const resultsContainer = document.getElementById('search-results');

let debounceTimer;

searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  const query = e.target.value.trim();
  
  if (query.length < 2) {
    resultsContainer.innerHTML = '';
    resultsContainer.classList.remove('active');
    return;
  }
  
  debounceTimer = setTimeout(() => {
    fetch(`/api/search.php?q=${encodeURIComponent(query)}&lang=${document.documentElement.lang}`)
      .then(r => r.json())
      .then(data => {
        if (!data.results.length) {
          resultsContainer.innerHTML = '<div class="no-results">Non se atoparon resultados</div>';
        } else {
          resultsContainer.innerHTML = data.results.map(r => `
            <a href="/comercio/${r.slug}/" class="search-result-item">
              <strong>${r.nombre}</strong>
              <span class="search-cat">${r.categorias}</span>
              <span class="search-addr">${r.direccion}</span>
            </a>
          `).join('');
        }
        resultsContainer.classList.add('active');
      });
  }, 300); // 300ms debounce
});
```

### 5.7 Costes del Buscador IA

| Concepto | Coste |
|----------|-------|
| Pre-cálculo embeddings (una vez) | $0.001 |
| Embedding por búsqueda (~200 tokens) | $0.000002 |
| 1000 búsquedas/mes | $0.002 |
| 10,000 búsquedas/mes | $0.02 |
| **Total mensual realista** | **< $0.10** |

Esto es **absurdamente barato**. Incluso con 100K búsquedas/mes, el coste sería ~$0.20.

### 5.8 Estimación Fase 5

| Tarea | Horas |
|-------|-------|
| generate_embeddings.py | 2h |
| search.php (text + semantic) | 4h |
| Frontend búsqueda + dropdown resultados | 4h |
| Búsqueda gallego testing | 2h |
| Integrar en hero + página dedicada | 3h |
| Testing + optimización | 3h |
| **Total** | **~18h (3 días IA)** |

---

## 6. FASE 6: Escaparate Boutique + Funcionalidades Extra

### 6.1 "O Mellor do Centro" — Escaparate de Productos

#### Modelo de datos para productos

```json
// data/productos.json
[
  {
    "id": 1,
    "comercio_slug": "zapateria-ejemplo",
    "nombre": {
      "gl": "Zapatos de coiro artesanais",
      "es": "Zapatos de cuero artesanales"
    },
    "descripcion": {
      "gl": "Feitos a man en Galicia",
      "es": "Hechos a mano en Galicia"
    },
    "precio": 89.90,
    "precio_oferta": null,
    "imagen": "productos/zapatos-artesanales-1.jpg",
    "categoria": "calzado",
    "destacado": true,
    "activo": true,
    "fecha_alta": "2026-03-01"
  }
]
```

#### Opciones de gestión de productos

| Opción | Pros | Contras | Recomendación |
|--------|------|---------|---------------|
| **A) CSV manual** (CCA sube CSV periódicamente) | Simple, sin desarrollo extra | Dependencia del CCA, no real-time | ✅ Para MVP |
| **B) Admin PHP ligero** (login CCA) | Autonomía del CCA | Más desarrollo, gestión usuarios | Para Fase futura |
| **C) Panel por comerciante** (cada uno sube sus productos) | Escalable, descentralizado | Mucho más desarrollo, onboarding | Descartado por ahora |

**Recomendación:** Empezar con **CSV/JSON manual** que el CCA envía y Rocket sube. Evaluar el admin PHP ligero según adopción.

#### Sección escaparate en home

```html
<section class="escaparate">
  <div class="container">
    <h2 class="section-title">O Mellor do Centro</h2>
    <p class="section-subtitle">Produtos destacados das tendas da Magdalena</p>
    <div class="productos-grid">
      {% for producto in productos_destacados[:8] %}
      <div class="card-producto">
        <div class="producto-img" style="background-image: url('{{ producto.imagen }}')">
          {% if producto.precio_oferta %}
          <span class="badge-oferta">OFERTA</span>
          {% endif %}
        </div>
        <div class="producto-body">
          <span class="producto-tienda">{{ producto.comercio_nombre }}</span>
          <h3>{{ producto.nombre[lang] }}</h3>
          <div class="producto-precio">
            {% if producto.precio_oferta %}
            <span class="precio-old">{{ producto.precio }}€</span>
            <span class="precio-new">{{ producto.precio_oferta }}€</span>
            {% else %}
            <span class="precio">{{ producto.precio }}€</span>
            {% endif %}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
    <a href="/escaparate/" class="btn-ver-todos">Ver todos os produtos →</a>
  </div>
</section>
```

### 6.2 Mapa Interactivo Mejorado (Leaflet + Clustering)

```html
<div id="mapa-comercios" style="height: 500px; border-radius: 8px;"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<script>
const map = L.map('mapa-comercios').setView([43.485, -8.233], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

const markers = L.markerClusterGroup({
  maxClusterRadius: 40,
  spiderfyOnMaxZoom: true
});

// Iconos custom por categoría
const iconCategoria = (cat) => L.divIcon({
  html: `<div class="marker-icon marker-${cat}"><i class="${getIconForCategory(cat)}"></i></div>`,
  iconSize: [36, 36],
  className: 'custom-marker'
});

// Cargar comercios desde JSON embebido en la página
const comercios = {{ comercios_json | safe }};

comercios.forEach(com => {
  if (!com.coordenadas || !com.coordenadas.lat) return;
  
  const marker = L.marker(
    [com.coordenadas.lat, com.coordenadas.lng],
    { icon: iconCategoria(com.categorias[0]) }
  );
  
  marker.bindPopup(`
    <div class="map-popup">
      <strong><a href="/comercio/${com.slug}/">${com.nombre}</a></strong>
      <p>${com.direccion}</p>
      ${com.telefono ? `<p>📞 ${com.telefono}</p>` : ''}
      <span class="popup-status" data-slug="${com.slug}"></span>
    </div>
  `);
  
  markers.addLayer(marker);
});

map.addLayer(markers);
</script>
```

### 6.3 Estado Abierto/Cerrado en Tiempo Real

```javascript
// horarios.js — Calcula si un comercio está abierto AHORA
function isOpen(horarios) {
  if (!horarios || Object.keys(horarios).length === 0) return null; // desconocido
  
  const now = new Date();
  const dayNames = ['domingo', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado'];
  const today = dayNames[now.getDay()];
  const currentTime = now.getHours() * 100 + now.getMinutes();
  
  const todayHours = horarios[today];
  if (!todayHours) return false; // cerrado hoy
  
  // Formato esperado: "09:30 - 14:00, 17:00 - 20:30"
  const ranges = todayHours.split(',').map(r => r.trim());
  
  for (const range of ranges) {
    const [open, close] = range.split('-').map(t => {
      const [h, m] = t.trim().split(':').map(Number);
      return h * 100 + m;
    });
    
    if (currentTime >= open && currentTime <= close) return true;
  }
  
  return false;
}

// Mostrar estado en cada card
document.querySelectorAll('[data-horarios]').forEach(el => {
  const horarios = JSON.parse(el.dataset.horarios);
  const status = isOpen(horarios);
  
  if (status === true) {
    el.innerHTML = '<span class="status-open">● Aberto</span>';
  } else if (status === false) {
    el.innerHTML = '<span class="status-closed">● Pechado</span>';
  }
  // null = no mostrar nada
});
```

### 6.4 Filtros Avanzados

```html
<div class="filters-bar">
  <div class="filter-group">
    <label>Categoría</label>
    <select id="filter-categoria">
      <option value="">Todas</option>
      {% for cat in categorias %}
      <option value="{{ cat.slug }}">{{ cat.nombre[lang] }}</option>
      {% endfor %}
    </select>
  </div>
  
  <div class="filter-group">
    <label>Estado</label>
    <select id="filter-estado">
      <option value="">Todos</option>
      <option value="open">Aberto agora</option>
      <option value="closed">Pechado</option>
    </select>
  </div>
  
  <div class="filter-group">
    <label>Valoración</label>
    <select id="filter-rating">
      <option value="">Todas</option>
      <option value="4">⭐ 4+ estrellas</option>
      <option value="4.5">⭐ 4.5+ estrellas</option>
    </select>
  </div>
  
  <button id="filter-reset" class="btn-reset">Limpar filtros</button>
</div>
```

### 6.5 Páginas Estáticas Adicionales

| Página | Ruta | Contenido |
|--------|------|-----------|
| Asociados | `/asociados/` | Listado de todos los 116 comercios con logo |
| Hazte Socio | `/hazte-socio/` | Formulario de contacto + beneficios de pertenecer al CCA |
| Nosotros | `/sobre-nos/` | Historia del CCA, misión, equipo |
| Contacto | `/contacto/` | Formulario + mapa de la sede del CCA |
| Noticias | `/novas/` | Feed de noticias/eventos del barrio |

**Noticias:** Sistema simple basado en archivos Markdown en `data/noticias/`. El build.py los convierte a HTML.

```
data/noticias/
├── 2026-03-01-feira-primavera.md
├── 2026-02-15-horarios-semana-santa.md
└── 2026-02-01-nova-tenda-aberta.md
```

### 6.6 Estimación Fase 6

| Tarea | Horas |
|-------|-------|
| Escaparate Boutique (modelo + templates + CSS) | 6h |
| Mapa Leaflet + clustering | 4h |
| Horario abierto/cerrado JS | 3h |
| Filtros avanzados | 4h |
| Páginas estáticas (5 páginas) | 5h |
| Sistema noticias (Markdown → HTML) | 3h |
| Integrar todo en build.py | 4h |
| Testing responsive | 3h |
| **Total** | **~32h (5-6 días IA)** |

---

## 7. FASE 7: SEO Bilingüe + Migración + Lanzamiento

### 7.1 Estrategia SEO Bilingüe

#### Estructura de URLs

```
ferrolcomercio.es/                          ← Home (gallego por defecto)
ferrolcomercio.es/es/                       ← Home español

ferrolcomercio.es/comercio/zapateria-x/     ← Ficha GL
ferrolcomercio.es/es/comercio/zapateria-x/  ← Ficha ES

ferrolcomercio.es/categoria/calzado/        ← Categoría GL
ferrolcomercio.es/es/categoria/calzado/     ← Categoría ES

ferrolcomercio.es/mapa/                     ← Mapa GL
ferrolcomercio.es/es/mapa/                  ← Mapa ES
```

**Idioma por defecto: gallego** (gl) — El contenido del CCA está mayoritariamente en gallego y el público objetivo es local.

#### Tags hreflang

```html
<!-- En TODAS las páginas -->
<link rel="alternate" hreflang="gl" href="https://ferrolcomercio.es/comercio/zapateria-x/" />
<link rel="alternate" hreflang="es" href="https://ferrolcomercio.es/es/comercio/zapateria-x/" />
<link rel="alternate" hreflang="x-default" href="https://ferrolcomercio.es/comercio/zapateria-x/" />
```

#### Meta tags SEO por tipo de página

```html
<!-- HOME -->
<title>Comercios do Barrio de A Magdalena | Ferrol Comercio</title>
<meta name="description" content="Directorio de 116 comercios do Centro Comercial Aberto da Magdalena en Ferrol. Tendas, restaurantes, servizos e máis.">

<!-- FICHA COMERCIO -->
<title>{{ comercio.nombre }} | Ferrol Comercio</title>
<meta name="description" content="{{ comercio.nombre }} en {{ comercio.direccion }}. {{ comercio.categorias }}. Horarios, opinións e contacto.">

<!-- CATEGORÍA -->
<title>{{ categoria.nombre }} en A Magdalena | Ferrol Comercio</title>
<meta name="description" content="Descubre todos os {{ categoria.nombre|lower }} do barrio da Magdalena en Ferrol. Horarios, opinións e localización.">
```

### 7.2 Structured Data (Schema.org)

#### Mapping categorías → Schema types

```python
SCHEMA_TYPES = {
    "resturantes": "Restaurant",
    "bares": "BarOrPub",
    "cafeterias": "CafeOrCoffeeShop",
    "confiterias": "Bakery",
    "alimentacion": "GroceryStore",
    "moda": "ClothingStore",
    "calzado": "ShoeStore",
    "peluquerias": "HairSalon",
    "estetica": "HealthAndBeautyBusiness",
    "clinica-dental": "Dentist",
    "farmacia": "Pharmacy",
    "opticas": "Optician",
    "joyeria": "JewelryStore",
    "electronica": "ElectronicsStore",
    "agencia-de-viajes": "TravelAgency",
    "inmobiliarias": "RealEstateAgent",
    "floristerias": "Florist",
    "librerias": "BookStore",
    # Default para categorías sin mapping específico:
    "_default": "LocalBusiness"
}
```

#### JSON-LD por ficha de comercio

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "{{ schema_type }}",
  "name": "{{ comercio.nombre }}",
  "description": "{{ comercio.descripcion_corta }}",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "{{ comercio.direccion }}",
    "addressLocality": "Ferrol",
    "addressRegion": "A Coruña",
    "postalCode": "15403",
    "addressCountry": "ES"
  },
  {% if comercio.coordenadas.lat %}
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": {{ comercio.coordenadas.lat }},
    "longitude": {{ comercio.coordenadas.lng }}
  },
  {% endif %}
  {% if comercio.telefono %}
  "telephone": "{{ comercio.telefono }}",
  {% endif %}
  {% if comercio.web %}
  "url": "{{ comercio.web }}",
  {% endif %}
  "image": "{{ comercio.imagen_destacada_url }}",
  {% if comercio.google_rating %}
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "{{ comercio.google_rating }}",
    "reviewCount": "{{ comercio.google_total_reviews }}"
  },
  {% endif %}
  "isPartOf": {
    "@type": "ShoppingCenter",
    "name": "Centro Comercial Aberto da Magdalena",
    "url": "https://ferrolcomercio.es"
  }
}
</script>
```

#### JSON-LD para la home (Organization + ItemList)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "CCA Ferrol Comercio",
  "alternateName": "Centro Comercial Aberto do Barrio de A Magdalena",
  "url": "https://ferrolcomercio.es",
  "logo": "https://ferrolcomercio.es/assets/images/cca-ferrol-comercio-color.png",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Ferrol",
    "addressRegion": "A Coruña",
    "addressCountry": "ES"
  }
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Comercios da Magdalena",
  "numberOfItems": 116,
  "itemListElement": [
    {% for com in comercios[:20] %}
    {
      "@type": "ListItem",
      "position": {{ loop.index }},
      "url": "https://ferrolcomercio.es/comercio/{{ com.slug }}/"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ]
}
</script>
```

### 7.3 Core Web Vitals — Métricas Objetivo

| Métrica | Objetivo | Cómo lo conseguimos |
|---------|----------|---------------------|
| **LCP** (Largest Contentful Paint) | < 1.5s | HTML estático, imágenes optimizadas, hero con `loading="eager"` |
| **FID** (First Input Delay) | < 50ms | JS mínimo, sin frameworks pesados |
| **CLS** (Cumulative Layout Shift) | < 0.05 | Dimensiones fijas en imágenes, no font-swap tardío |
| **TTFB** (Time to First Byte) | < 200ms | HTML estático servido por Hostinger CDN |
| **FCP** (First Contentful Paint) | < 1.0s | CSS crítico inline, fonts con `font-display: swap` |

**Ventaja competitiva:** Al ser HTML estático (no WordPress), automáticamente superamos el 90% de las webs de directorios locales en velocidad.

### 7.4 Plan de Migración desde WordPress

#### Paso 1: Mapear URLs antiguas → nuevas

```python
# migrate_urls.py — Genera el .htaccess con redirects 301
"""
URLs WordPress típicas de Listeo:
  /listing/zapateria-ejemplo/
  /listing-category/calzado/
  /listing_region/ferrol/

URLs nuevas:
  /comercio/zapateria-ejemplo/
  /categoria/calzado/
  (regiones eliminadas — solo hay Ferrol)
"""

redirects = []

for comercio in comercios:
    old = f"/listing/{comercio['slug']}/"
    new = f"/comercio/{comercio['slug']}/"
    redirects.append(f"Redirect 301 {old} https://ferrolcomercio.es{new}")

for cat in categorias:
    old = f"/listing-category/{cat['slug']}/"
    new = f"/categoria/{cat['slug']}/"
    redirects.append(f"Redirect 301 {old} https://ferrolcomercio.es{new}")

# Páginas genéricas
redirects.append("Redirect 301 /listings/ https://ferrolcomercio.es/comercios/")
redirects.append("Redirect 301 /listing_region/ferrol/ https://ferrolcomercio.es/comercios/")
```

#### Paso 2: .htaccess generado

```apache
# ─── Redirects 301: WordPress → Nueva web ───
# Generado automáticamente por migrate_urls.py

# Fichas de comercios
Redirect 301 /listing/clinica-dental-ferrol-patricia-aneiros-dentista-en-ferrol/ https://ferrolcomercio.es/comercio/clinica-dental-ferrol-patricia-aneiros-dentista-en-ferrol/
Redirect 301 /listing/clinica-dental-vitaldent/ https://ferrolcomercio.es/comercio/clinica-dental-vitaldent/
# ... (116 redirects)

# Categorías
Redirect 301 /listing-category/calzado/ https://ferrolcomercio.es/categoria/calzado/
Redirect 301 /listing-category/moda/ https://ferrolcomercio.es/categoria/moda/
# ... (39 redirects)

# Genéricas
Redirect 301 /listings/ https://ferrolcomercio.es/comercios/
Redirect 301 /listing_region/ferrol/ https://ferrolcomercio.es/comercios/

# WordPress residuales
Redirect 301 /wp-login.php https://ferrolcomercio.es/
Redirect 301 /wp-admin/ https://ferrolcomercio.es/
RedirectMatch 301 ^/wp-content/(.*)$ https://ferrolcomercio.es/

# Trailing slash enforcement
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*[^/])$ /$1/ [L,R=301]
```

### 7.5 Sitemaps

```xml
<!-- sitemap.xml (índice) -->
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-pages-gl.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-pages-es.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-comercios-gl.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-comercios-es.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-categorias-gl.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://ferrolcomercio.es/sitemap-categorias-es.xml</loc>
  </sitemap>
</sitemapindex>
```

El `build.py` ya genera sitemaps; hay que extenderlo para generar los separados por idioma.

### 7.6 Checklist de Lanzamiento

```
PRE-LANZAMIENTO:
□ Dominio ferrolcomercio.es restaurado y apuntando a Hostinger
□ Certificado SSL activo (Let's Encrypt via Hostinger)
□ .htaccess con redirects 301 subido
□ robots.txt actualizado
□ Google Search Console verificado (ambos: con y sin www)
□ Sitemaps subidos a Search Console
□ Google Analytics 4 / Plausible instalado
□ Todas las imágenes optimizadas (WebP con fallback JPEG)
□ Favicon + apple-touch-icon + OG images
□ Test en PageSpeed Insights (objetivo: 95+ mobile)
□ Test en diferentes navegadores (Chrome, Safari, Firefox)
□ Test en móvil real

POST-LANZAMIENTO (semana 1):
□ Monitorizar errores 404 en Search Console
□ Verificar que los 301 funcionan (sample testing)
□ Comprobar indexación de páginas clave
□ Compartir en redes sociales del CCA
□ Enviar nota de prensa local
```

### 7.7 Estimación Fase 7

| Tarea | Horas |
|-------|-------|
| Implementar hreflang + meta tags | 3h |
| Schema.org JSON-LD por tipo | 4h |
| Generar .htaccess redirects 301 | 2h |
| Sitemaps separados por idioma | 2h |
| Optimización imágenes (WebP) | 3h |
| Core Web Vitals testing + fixes | 3h |
| Favicon + OG images | 1h |
| Deploy + verificación | 3h |
| **Total** | **~21h (3-4 días IA)** |

---

## 8. Resumen de Costes

### Costes únicos (desarrollo)

| Concepto | Coste |
|----------|-------|
| Hosting Hostinger (ya contratado) | $0 |
| Dominio (ya existente) | $0 |
| Google Places API (resolver 25 Place IDs) | $0.80 |
| OpenAI Embeddings (116 comercios) | $0.001 |
| **Total setup** | **< $1** |

### Costes mensuales recurrentes

| Concepto | Coste/mes |
|----------|-----------|
| Google Places API (sync reseñas cada 3 días) | ~$20 |
| OpenAI Embeddings (búsquedas) | ~$0.10 |
| Hosting Hostinger (ya pagado) | $0 |
| **Total mensual** | **~$20** |

**Con el crédito gratuito de Google ($200/mes): coste real = ~$0.10/mes**

### Coste anual total estimado

| Escenario | Coste/año |
|-----------|-----------|
| Con crédito Google (probable) | ~$1.20 |
| Sin crédito Google | ~$241 |

---

## 9. Riesgos y Mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|--------|-------------|---------|------------|
| 1 | **Dominio no restaurado a tiempo** | Media | Alto | Mantener preview en rocketmaker.app; lanzar allí si se retrasa |
| 2 | **Crédito Google agotado** | Baja | Medio | Reducir frecuencia de sync; cachear agresivamente |
| 3 | **Comercios sin Google Business** | Confirmado (25) | Bajo | Fallback con datos propios; CCA ayuda a crearlos |
| 4 | **Gallego mal procesado por IA** | Baja | Medio | Incluir términos gallegos en embeddings; testing con queries reales |
| 5 | **Hostinger demasiado lento para PHP** | Baja | Medio | El PHP es mínimo (solo API); 90% es HTML estático |
| 6 | **CCA no proporciona productos para Escaparate** | Media | Bajo | Lanzar sin escaparate; añadir después cuando tengan contenido |
| 7 | **Pérdida de SEO en migración** | Media | Alto | Redirects 301 exhaustivos; monitorización diaria primera semana |
| 8 | **Imágenes con copyright** | Baja | Medio | Todas las imágenes vienen del WordPress del CCA (suyas) |

---

## 10. Decisiones que Necesitan Aprobación del Cliente

### Decisiones críticas (bloquean avance)

1. **🔤 Fuente de la firma "A Magdalena"**
   - ¿Dancing Script (Google Font) o proporciona el CCA un SVG/imagen?
   - Recomendación: Dancing Script 700 (rápida, legible)

2. **🌍 Idioma por defecto**
   - Propuesta: gallego (gl) como idioma base, español en `/es/`
   - ¿El CCA está de acuerdo?

3. **📊 Google Places API Key**
   - Necesitamos una API key con billing habilitado
   - ¿La proporcionan ellos o la creamos desde Rocket?

4. **🔄 Frecuencia de sync de reseñas**
   - Recomendación: cada 3 días
   - ¿OK o prefieren diario? (afecta coste si se excede crédito)

### Decisiones importantes (no bloquean pero afectan alcance)

5. **🛍️ Escaparate Boutique: ¿quién sube los productos?**
   - MVP: el CCA envía CSV/JSON, Rocket lo sube
   - Futuro: panel admin para el CCA

6. **📰 Noticias: ¿tienen contenido?**
   - Si no tienen noticias iniciales, la sección se puede lanzar vacía
   - ¿El CCA tiene un blog/redes de donde extraer contenido?

7. **📋 Páginas legales**
   - ¿Tienen textos de Aviso Legal, Política de Privacidad, Cookies?
   - Si no, Rocket los redacta (coste adicional o incluido)

8. **📱 App / PWA futura**
   - ¿Hay interés en convertir la web en Progressive Web App?
   - El stack actual lo permite fácilmente (manifest.json + service worker)

---

## 11. Cronograma Propuesto

```
MARZO 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Semana 2 (10-14): FASE 3 — Identidad Visual
Semana 3 (17-21): FASE 4 — Google Business  
Semana 4 (24-28): FASE 5 — Buscador IA

ABRIL 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Semana 1-2 (31 mar - 11 abr): FASE 6 — Escaparate + Extras
Semana 3 (14-18): FASE 7 — SEO + Migración
Semana 4 (21-25): LANZAMIENTO 🚀

TOTAL: ~7 semanas
```

**Nota:** Las fases 3-5 pueden solaparse parcialmente. La Fase 7 puede empezar en paralelo con la 6 (SEO se integra continuamente).

---

## 12. Stack Técnico Final

```
FRONTEND (estático)
├── HTML5 generado por build.py (Jinja2)
├── CSS custom (modular, sin frameworks)
├── JavaScript vanilla (búsqueda, mapa, horarios, filtros)
├── Leaflet.js (mapa)
├── Font Awesome 6 (iconos)
├── Google Fonts (Raleway, Open Sans, Dancing Script)
└── Imágenes WebP con fallback JPEG

BACKEND (PHP ligero)
├── api/search.php (buscador semántico)
├── api/reviews.php (reseñas cacheadas)
├── sync_reviews.php (cron cada 3 días)
└── MySQL (caché reseñas + productos)

GENERADOR (Python)
├── build.py (genera todo el sitio estático)
├── generate_embeddings.py (pre-cálculo IA)
├── resolve_place_ids.py (Place IDs una vez)
└── migrate_urls.py (redirects 301)

HOSTING
├── Hostinger shared (PHP 8.x, MySQL, SSH)
├── SSL Let's Encrypt (auto)
└── CDN via Hostinger

APIs EXTERNAS
├── Google Places API (New) — reseñas, Place IDs
├── OpenAI Embeddings — búsqueda semántica
└── OpenStreetMap tiles — mapa (gratis)
```

---

*Documento preparado por Rocket Lanzadera Digital para CCA Ferrol Comercio.*  
*Última actualización: 7 de marzo de 2026*
