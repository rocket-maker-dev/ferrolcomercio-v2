# ferrolcomercio-v2 — Datos extraídos

**Fecha extracción:** 2026-02-24  
**Fuente:** Backup WordPress de ferrolcomercio.es (exportado 2026-02-18)

---

## 📊 Resumen de datos extraídos

### Comercios / Listings
| Campo | Valor |
|-------|-------|
| **Total comercios** | 97 |
| **Publicados** | 97 |
| **Con teléfono** | 84 / 97 |
| **Sin email** | 97 / 97 (⚠️ ninguno tiene email en meta) |
| **Con web** | 61 / 97 |
| **Con coordenadas GPS** | 91 / 97 |
| **Con horarios** | 82 / 97 |
| **Con galería de imágenes** | 84 / 97 |
| **Con imagen destacada** | 84 / 97 |

### Taxonomías
| Tipo | Cantidad |
|------|----------|
| **Categorías** | 39 (listing_category) |
| **Features/amenities** | 16 (listing_feature) |

### Imágenes
| Campo | Valor |
|-------|-------| 
| **Total imágenes referenciadas** | 371 |
| **Encontradas en bk_uploads.zip** | 371 / 371 ✅ |
| **Total archivos en uploads** | 11.853 archivos |

---

## 📁 Estructura de archivos

```
ferrolcomercio-v2/
├── data/
│   ├── comercios.json          ← 97 comercios con todos sus datos
│   ├── categorias.json         ← 39 categorías de listing_category
│   ├── features.json           ← 16 amenities/características
│   ├── config.json             ← Configuración del sitio (colores, logo, mapa)
│   └── raw/
│       ├── extract.py          ← Script de extracción Python
│       ├── stats.json          ← Estadísticas detalladas
│       ├── image_inventory.json← Inventario completo de imágenes
│       ├── uploads_inventory_full.txt  ← Todos los archivos en bk_uploads.zip
│       └── listing_images_2025_2026.txt ← Imágenes 2025-2026 (828 originales)
├── assets/
│   ├── css/
│   │   ├── listeo-style.css    ← CSS principal del theme Listeo (828KB)
│   │   ├── icons.css           ← Iconos del theme (111KB)
│   │   ├── custom.css.php      ← CSS dinámico con colores configurables
│   │   ├── bootstrap-grid.css  ← Grid system
│   │   └── all.css             ← FontAwesome completo
│   ├── fonts/
│   │   └── *.woff, *.woff2     ← 14 archivos de fuentes web
│   └── images/
│       ├── logo.png            ← Logo actual (2025)
│       ├── logo-original.png   ← Logo original (2019)
│       ├── header-ferrolcomercio.png
│       ├── header-ferrolcomercio-bolsa.png
│       └── header-ferrolcomercio-shopping.png
└── README.md                   ← Este archivo
```

---

## 🎨 Configuración visual

- **Color principal:** `#0663ac` (azul CCA Ferrol)
- **Logo actual:** `uploads/2025/11/cca-ferrol-comercio-color.png`
- **Theme origen:** Listeo (WordPress Theme)
- **Idioma principal:** Galego (gl-ES)

---

## 📝 Estructura del JSON de comercios

Cada entrada en `comercios.json` tiene esta estructura:

```json
{
  "id": 1211,
  "nombre": {"gl": null, "es": "Clínica Dental Vitaldent"},
  "slug": "clinica-dental-vitaldent",
  "descripcion": {"gl": null, "es": "<p>...HTML...</p>"},
  "estado": "publish",
  "categorias": ["clinica-dental"],
  "features": ["parking"],
  "region": ["ferrol"],
  "direccion": "R. Real, 78, 15402 Ferrol, A Coruña, España",
  "telefono": "+34 881 24 66 30",
  "email": null,
  "web": "https://...",
  "coordenadas": {"lat": 43.48397, "lng": -8.233311},
  "horarios": {
    "lunes": ["09:00-15:00", "16:00-20:00"],
    "viernes": ["09:00-15:00", "16:00-20:00"]
  },
  "google_place_id": null,
  "imagenes": ["uploads/2026/01/clinica-dental-vitaldent-1.jpg", "..."],
  "logo": null,
  "rating": 4.9,
  "num_reviews": 311,
  "featured": false,
  "redes_sociales": {"facebook": "...", "instagram": "..."},
  "fecha_creacion": "2026-01-24 00:30:56",
  "imagen_destacada": "uploads/2026/01/clinica-dental-vitaldent-1.jpg"
}
```

---

## ⚠️ Datos faltantes / Pendiente

| Campo | Estado |
|-------|--------|
| **Emails** | ❌ Ningún comercio tiene email en metadatos |
| **Google Place ID** | ❌ No encontrado en los metadatos del XML |
| **Traducción Galego** | ⏳ Todo en español, `gl` → `null` (pendiente traducción) |
| **6 comercios sin tel** | Ver stats.json |
| **6 comercios sin coords** | Ver stats.json |
| **13 listings sin galería** | Ver stats.json |

---

## 🔄 Siguiente paso (FASE 2)

Con estos datos estructurados, el siguiente paso es:
1. **Extraer imágenes** del `bk_uploads.zip` (842MB) y organizarlas en `assets/comercios/`
2. **Traducir al galego** los nombres y descripciones con IA
3. **Generar HTML** — páginas estáticas del directorio
4. **Configurar el mapa** con Leaflet/OSM usando las coordenadas GPS

---

## 📦 Fuentes de datos originales

| Archivo | Tamaño | Contenido |
|---------|--------|-----------|
| `ferrolcomercio_export_20260218.xml` | 6.5MB | WordPress XML export (1.178 items) |
| `ferrolcomercio_db_20260218.sql` | 24MB | Base de datos MySQL completa |
| `bk_themes.zip` | 36MB | Themes (incluye Listeo) |
| `bk_uploads.zip` | 842MB | 11.853 archivos de media |
| `bk_plugins.zip` | 128MB | Plugins WordPress |
