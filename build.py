#!/usr/bin/env python3
"""
build.py — Generador estático para ferrolcomercio.es v2
Genera todas las páginas HTML, sitemap.xml y robots.txt en dist/
"""

import json
import os
import re
import shutil
import datetime
import argparse
from pathlib import Path
from urllib.parse import quote

# Jinja2
from jinja2 import Environment, FileSystemLoader

# ──────────────────────────────────────────────────────────────────
# ARGUMENTOS CLI
# ──────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description='Generador estático ferrolcomercio v2')
parser.add_argument('--base-url', default='https://ferrolcomercio.es',
                    help='URL base del sitio (sin trailing slash). Ej: /cca-preview')
args = parser.parse_args()

# ──────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DATA_DIR   = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
TMPL_DIR   = BASE_DIR / "templates"
DIST_DIR   = BASE_DIR / "dist"

# URL base del sitio (sin trailing slash)
SITE_URL = args.base_url
# En desarrollo: cambiar a ruta relativa o vacío para paths relativos
# SITE_URL = ""

# URL base para imágenes del original
IMG_BASE_URL = "https://ferrolcomercio.es/wp-content"  # legacy WP uploads only

LANGS = ["gl", "es"]

# ──────────────────────────────────────────────────────────────────
# ICONOS POR CATEGORÍA
# ──────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────
# CATEGORÍAS PRINCIPALES (8 agrupaciones)
# ──────────────────────────────────────────────────────────────────
MAIN_CATEGORIES = [
    {
        "slug": "moda-textil",
        "nombre": {"es": "Moda e Téxtil", "gl": "Moda e Téxtil"},
        "icono": "fas fa-tshirt",
        "subcategorias": ["textil", "moda", "calzado", "lenceria", "ropa-interior", "papelerias"]
    },
    {
        "slug": "restauracion",
        "nombre": {"es": "Restauración", "gl": "Restauración"},
        "icono": "fas fa-utensils",
        "subcategorias": ["resturantes", "cafeterias", "bares", "confiterias"]
    },
    {
        "slug": "saude-benestar",
        "nombre": {"es": "Saúde e Benestar", "gl": "Saúde e Benestar"},
        "icono": "fas fa-heartbeat",
        "subcategorias": ["clinica-dental", "fisioterapia", "farmacias", "ortopedia", "psicologo"]
    },
    {
        "slug": "beleza-estetica",
        "nombre": {"es": "Beleza e Estética", "gl": "Beleza e Estética"},
        "icono": "fas fa-spa",
        "subcategorias": ["peluquerias", "estilismo", "tatuajes", "perfumeria"]
    },
    {
        "slug": "fogar-deco",
        "nombre": {"es": "Fogar e Decoración", "gl": "Fogar e Decoración"},
        "icono": "fas fa-couch",
        "subcategorias": ["mueblerias", "electrodomesticos", "iluminacion", "artesania", "regalos-y-decoracion"]
    },
    {
        "slug": "cultura-ocio",
        "nombre": {"es": "Cultura e Ocio", "gl": "Cultura e Ocio"},
        "icono": "fas fa-music",
        "subcategorias": ["musica", "librerias", "formacion", "agencia-de-viajes", "deporte"]
    },
    {
        "slug": "servizos",
        "nombre": {"es": "Servizos", "gl": "Servizos"},
        "icono": "fas fa-briefcase",
        "subcategorias": ["imprentas", "copisteria", "seguros", "hospedaje", "servicios"]
    },
    {
        "slug": "alimentacion-agasallos",
        "nombre": {"es": "Alimentación e Agasallos", "gl": "Alimentación e Agasallos"},
        "icono": "fas fa-shopping-bag",
        "subcategorias": ["alimentacion", "joyerias", "merceria", "floristerias", "opticas"]
    }
]

CAT_ICONS = {
    "moda":                 "fas fa-tshirt",
    "textil":               "fas fa-cut",
    "lenceria":             "fas fa-shopping-bag",
    "ropa-interior":        "fas fa-star",
    "calzado":              "fas fa-shoe-prints",
    "resturantes":          "fas fa-utensils",
    "bares":                "fas fa-cocktail",
    "cafeterias":           "fas fa-coffee",
    "confiterias":          "fas fa-birthday-cake",
    "alimentacion":         "fas fa-apple-alt",
    "peluquerias":          "fas fa-cut",
    "perfumeria":           "fas fa-spray-can",
    "farmacias":            "fas fa-pills",
    "clinica-dental":       "fas fa-tooth",
    "fisioterapia":         "fas fa-spa",
    "opticas":              "fas fa-glasses",
    "psicologo":            "fas fa-brain",
    "ortopedia":            "fas fa-wheelchair",
    "joyerias":             "fas fa-gem",
    "librerias":            "fas fa-book",
    "papelerias":           "fas fa-paperclip",
    "musica":               "fas fa-music",
    "deporte":              "fas fa-dumbbell",
    "hospedaje":            "fas fa-hotel",
    "agencia-de-viajes":    "fas fa-plane",
    "seguros":              "fas fa-shield-alt",
    "servicios":            "fas fa-tools",
    "electrodomesticos":    "fas fa-plug",
    "mueblerias":           "fas fa-couch",
    "regalos-y-decoracion": "fas fa-gift",
    "floristerias":         "fas fa-seedling",
    "artesania":            "fas fa-palette",
    "tatuajes":             "fas fa-pen",
    "copisteria":           "fas fa-copy",
    "imprentas":            "fas fa-print",
    "iluminacion":          "fas fa-lightbulb",
    "formacion":            "fas fa-graduation-cap",
    "merceria":             "fas fa-thread",
    "estilismo":            "fas fa-magic",
}

# ──────────────────────────────────────────────────────────────────
# SLUGIFY
# ──────────────────────────────────────────────────────────────────
def slugify(text):
    text = text.lower().strip()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'ñ': 'n', 'ç': 'c', 'ã': 'a', 'õ': 'o',
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

# ──────────────────────────────────────────────────────────────────
# HELPERS JINJA2
# ──────────────────────────────────────────────────────────────────
def striptags_filter(value):
    """Elimina tags HTML."""
    if not value:
        return ""
    return re.sub(r'<[^>]+>', ' ', str(value)).strip()

def truncate_filter(value, length=120, ellipsis='...'):
    """Trunca texto."""
    value = str(value)
    if len(value) <= length:
        return value
    return value[:length].rsplit(' ', 1)[0] + ellipsis

def urlshort_filter(url):
    """Acorta URL para mostrar."""
    if not url:
        return ""
    url = re.sub(r'^https?://(www\.)?', '', url)
    return url[:50] + '...' if len(url) > 50 else url

def tojson_filter(value):
    return json.dumps(value, ensure_ascii=False)

def tojsonstr_filter(value):
    """Returns a JSON-encoded string (with quotes, escaped properly)."""
    return json.dumps(str(value) if value else "", ensure_ascii=False)

def dia_schema_filter(dia):
    """Convierte nombre de día castellano a schema.org."""
    mapping = {
        'lunes':     'Monday',
        'martes':    'Tuesday',
        'miercoles': 'Wednesday',
        'jueves':    'Thursday',
        'viernes':   'Friday',
        'sabado':    'Saturday',
        'domingo':   'Sunday',
    }
    return mapping.get(dia.lower(), dia)

def cat_nombre_filter(cat_slug, categorias, lang):
    """Devuelve el nombre de una categoría dado su slug."""
    for cat in categorias:
        if cat['slug'] == cat_slug:
            return cat['nombre'].get(lang) or cat['nombre'].get('es') or cat_slug
    return cat_slug

# ──────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ──────────────────────────────────────────────────────────────────
def load_data():
    with open(DATA_DIR / "comercios.json", encoding="utf-8") as f:
        comercios = json.load(f)
    with open(DATA_DIR / "categorias.json", encoding="utf-8") as f:
        categorias = json.load(f)
    with open(DATA_DIR / "config.json", encoding="utf-8") as f:
        config = json.load(f)

    # Filtrar solo publicados
    comercios = [c for c in comercios if c.get("estado") == "publish"]

    # Añadir icono a categorías y contar comercios
    cat_counts = {}
    for c in comercios:
        for cat_slug in c.get("categorias", []):
            cat_counts[cat_slug] = cat_counts.get(cat_slug, 0) + 1

    for cat in categorias:
        cat["icon"] = CAT_ICONS.get(cat["slug"], "fas fa-store")
        cat["count"] = cat_counts.get(cat["slug"], 0)

    # Solo categorías con comercios
    categorias_activas = [c for c in categorias if c["count"] > 0]
    # Ordenar por count desc
    categorias_activas.sort(key=lambda c: c["count"], reverse=True)

    # Build main categories with counts
    categorias_principales = []
    for mc in MAIN_CATEGORIES:
        mc_copy = dict(mc)
        # Count unique comercios in all subcategorias
        comercios_in_mc = set()
        for c in comercios:
            for cat_slug in c.get("categorias", []):
                if cat_slug in mc["subcategorias"]:
                    comercios_in_mc.add(c["slug"])
                    break
        mc_copy["count"] = len(comercios_in_mc)
        # Get active subcategorias with their data
        mc_copy["subcategorias_data"] = [
            cat for cat in categorias if cat["slug"] in mc["subcategorias"] and cat.get("count", 0) > 0
        ]
        categorias_principales.append(mc_copy)

    return comercios, categorias, categorias_activas, categorias_principales, config

# ──────────────────────────────────────────────────────────────────
# ENTORNO JINJA2
# ──────────────────────────────────────────────────────────────────
def make_env():
    env = Environment(
        loader=FileSystemLoader(str(TMPL_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["striptags"]  = striptags_filter
    env.filters["truncate"]   = truncate_filter
    env.filters["urlshort"]   = urlshort_filter
    env.filters["tojson"]     = tojson_filter
    env.filters["tojsonstr"]  = tojsonstr_filter
    env.filters["dia_schema"] = dia_schema_filter
    env.filters["cat_nombre"] = cat_nombre_filter
    return env

# ──────────────────────────────────────────────────────────────────
# CONTEXTO BASE
# ──────────────────────────────────────────────────────────────────
def base_ctx(lang, config, comercios, categorias_activas,
             meta_title, meta_description, canonical_url,
             current_page="", og_image=None, use_map=False, use_search=False):
    year = datetime.datetime.now().year
    return {
        "lang": lang,
        "config": config,
        "base_url": SITE_URL,
        "img_base_url": IMG_BASE_URL,
        "assets_url": SITE_URL + "/assets",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "canonical_url": canonical_url,
        "url_gl": canonical_url.replace(f"/{lang}/", "/gl/"),
        "url_es": canonical_url.replace(f"/{lang}/", "/es/"),
        "og_image": og_image or f"{SITE_URL}/assets/images/header-ferrolcomercio.png",
        "og_type": "website",
        "current_page": current_page,
        "use_map": use_map,
        "use_search": use_search,
        "year": year,
        "total_comercios": len(comercios),
        "total_categorias": len(categorias_activas),
    }

# ──────────────────────────────────────────────────────────────────
# DÍA DE HOY
# ──────────────────────────────────────────────────────────────────
def get_dia_hoy():
    dias = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']
    return dias[datetime.datetime.now().weekday()]

# ──────────────────────────────────────────────────────────────────
# COMERCIOS → DATOS GEO (para mapa)
# ──────────────────────────────────────────────────────────────────
def comercios_to_geo(comercios_list, categorias, lang):
    result = []
    for c in comercios_list:
        coords = c.get("coordenadas")
        if coords:
            nombre = c["nombre"].get(lang) or c["nombre"].get("es") or ""
            cat_slug = c["categorias"][0] if c.get("categorias") else None
            cat_nombre = cat_nombre_filter(cat_slug, categorias, lang) if cat_slug else ""
            result.append({
                "slug": c["slug"],
                "nombre": nombre,
                "categoria": cat_nombre,
                "direccion": c.get("direccion", ""),
                "lat": coords["lat"],
                "lng": coords["lng"],
            })
    return result

# ──────────────────────────────────────────────────────────────────
# WRITE HTML
# ──────────────────────────────────────────────────────────────────
def write_html(path, html):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")

# ──────────────────────────────────────────────────────────────────
# GENERAR HOME
# ──────────────────────────────────────────────────────────────────
def gen_home(env, lang, comercios, categorias, categorias_activas, categorias_principales, config):
    tmpl = env.get_template("home.html")
    canonical = f"{SITE_URL}/{lang}/"

    # Comercios destacados: los featured primero, luego con mejor rating
    featured = [c for c in comercios if c.get("featured")]
    rest = [c for c in comercios if not c.get("featured")]
    rest.sort(key=lambda c: c.get("rating") or 0, reverse=True)
    destacados = (featured + rest)[:9]

    titles = {
        "gl": "CCA Ferrol — Magdalena | Directorio de Comercios",
        "es": "CCA Ferrol — Magdalena | Directorio de Comercios",
    }
    descs = {
        "gl": "Descobre os mellores comercios do barrio de A Magdalena en Ferrol. Directorio completo con horarios, teléfonos e localización.",
        "es": "Descubre los mejores comercios del barrio de A Magdalena en Ferrol. Directorio completo con horarios, teléfonos y localización.",
    }

    ctx = base_ctx(lang, config, comercios, categorias_activas,
                   titles[lang], descs[lang], canonical,
                   current_page="home", use_map=True, use_search=True)
    ctx.update({
        "categorias": categorias_activas,
        "categorias_principales": categorias_principales,
        "comercios_destacados": destacados,
        "comercios_geo": comercios_to_geo(comercios, categorias, lang),
    })

    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "index.html"
    write_html(out, html)
    print(f"  → {lang}/index.html")
    return canonical

# ──────────────────────────────────────────────────────────────────
# GENERAR FICHA COMERCIO
# ──────────────────────────────────────────────────────────────────
def gen_ficha(env, lang, comercio, categorias, categorias_activas, config):
    tmpl = env.get_template("ficha.html")
    slug = comercio["slug"]
    canonical = f"{SITE_URL}/{lang}/comercio/{slug}/"

    nombre = comercio["nombre"].get(lang) or comercio["nombre"].get("es") or slug
    desc_html = (comercio["descripcion"].get(lang)
                 or comercio["descripcion"].get("es")
                 or comercio["descripcion"].get("gl") or "")
    desc_plain = striptags_filter(desc_html)
    meta_desc = truncate_filter(desc_plain, 155) if desc_plain else f"{nombre} — {comercio.get('direccion', 'Ferrol')}"

    # Categoría principal
    cat_slug = comercio["categorias"][0] if comercio.get("categorias") else None
    cat_nombre_str = cat_nombre_filter(cat_slug, categorias, lang) if cat_slug else ""

    # Nota de idioma
    has_lang = bool(comercio["descripcion"].get(lang))
    other_lang = "es" if lang == "gl" else "gl"
    has_other = bool(comercio["descripcion"].get(other_lang))
    lang_notice = None
    if not has_lang and has_other:
        if lang == "gl":
            lang_notice = f'Este contido está dispoñible en <a href="{SITE_URL}/es/comercio/{slug}/">español</a>.'
        else:
            lang_notice = f'Este contenido está disponible en <a href="{SITE_URL}/gl/comercio/{slug}/">galego</a>.'

    # Imagen OG
    og_image = None
    if comercio.get("imagen_destacada"):
        og_image = f"{IMG_BASE_URL}/{comercio['imagen_destacada']}"

    title = f"{nombre} | CCA Ferrol Comercio"
    if len(title) > 60:
        title = nombre[:55] + "… | CCA"

    # Build Schema.org JSON-LD as Python dict (safe JSON serialization)
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": canonical,
        "name": nombre,
        "description": meta_desc,
        "url": canonical,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": comercio.get("direccion", ""),
            "addressLocality": "Ferrol",
            "addressRegion": "A Coruña",
            "addressCountry": "ES",
        },
        "containedInPlace": {
            "@type": "ShoppingCenter",
            "name": "CCA Ferrol Comercio",
            "url": f"{SITE_URL}/{lang}/",
        },
    }
    if comercio.get("imagen_destacada"):
        schema["image"] = f"{IMG_BASE_URL}/{comercio['imagen_destacada']}"
    if comercio.get("telefono"):
        schema["telephone"] = comercio["telefono"]
    if comercio.get("email"):
        schema["email"] = comercio["email"]
    if comercio.get("web"):
        schema["sameAs"] = [comercio["web"]]
    if comercio.get("coordenadas"):
        schema["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": comercio["coordenadas"]["lat"],
            "longitude": comercio["coordenadas"]["lng"],
        }
    if comercio.get("rating"):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(comercio["rating"]),
            "bestRating": "5",
            "reviewCount": str(comercio.get("num_reviews", 1)),
        }
    # Opening hours
    dias_schema_map = {
        'lunes': 'Monday', 'martes': 'Tuesday', 'miercoles': 'Wednesday',
        'jueves': 'Thursday', 'viernes': 'Friday', 'sabado': 'Saturday', 'domingo': 'Sunday',
    }
    if comercio.get("horarios"):
        ohs = []
        for dia, franjas in comercio["horarios"].items():
            for franja in (franjas or []):
                parts = franja.split('-')
                if len(parts) == 2:
                    ohs.append({
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": dias_schema_map.get(dia, dia),
                        "opens": parts[0],
                        "closes": parts[1],
                    })
        if ohs:
            schema["openingHoursSpecification"] = ohs

    # Breadcrumb schema
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio" if lang == "es" else "Inicio", "item": f"{SITE_URL}/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": cat_nombre_str, "item": f"{SITE_URL}/{lang}/categoria/{comercio['categorias'][0]}/"} if comercio.get("categorias") else {"@type": "ListItem", "position": 2, "name": cat_nombre_str},
            {"@type": "ListItem", "position": 3, "name": nombre},
        ]
    }
    schema_combined = json.dumps(schema, ensure_ascii=False, indent=2) + "\n</script>\n<script type=\"application/ld+json\">\n" + json.dumps(breadcrumb, ensure_ascii=False, indent=2)

    ctx = base_ctx(lang, config, [], categorias_activas,
                   title, meta_desc, canonical,
                   og_image=og_image, use_map=True)
    ctx.update({
        "comercio": comercio,
        "cat_nombre": cat_nombre_str,
        "dia_hoy": get_dia_hoy(),
        "lang_notice": lang_notice,
        "categorias": categorias,
        "schema_json": schema_combined,
        "page_type": "ficha",
    })

    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "comercio" / slug / "index.html"
    write_html(out, html)
    return canonical

# ──────────────────────────────────────────────────────────────────
# GENERAR PÁGINA CATEGORÍA
# ──────────────────────────────────────────────────────────────────
def gen_categoria(env, lang, categoria, comercios_cat, categorias, categorias_activas, config):
    tmpl = env.get_template("categoria.html")
    cat_slug = categoria["slug"]
    canonical = f"{SITE_URL}/{lang}/categoria/{cat_slug}/"

    cat_nombre_str = categoria["nombre"].get(lang) or categoria["nombre"].get("es") or cat_slug
    title = f"{cat_nombre_str} en Ferrol | CCA Ferrol Comercio"
    if len(title) > 60:
        title = f"{cat_nombre_str} | CCA Ferrol"

    if lang == "gl":
        desc = f"Comercios de {cat_nombre_str} no barrio de A Magdalena en Ferrol. {len(comercios_cat)} establecementos."
    else:
        desc = f"Comercios de {cat_nombre_str} en el barrio de A Magdalena en Ferrol. {len(comercios_cat)} establecimientos."
    if len(desc) > 155:
        desc = desc[:152] + "..."

    geo = [c for c in comercios_to_geo(comercios_cat, categorias, lang) if c]

    ctx = base_ctx(lang, config, comercios_cat, categorias_activas,
                   title, desc, canonical, use_map=bool(geo))
    ctx.update({
        "categoria": categoria,
        "comercios": comercios_cat,
        "todas_categorias": categorias_activas,
        "comercios_geo": geo,
    })

    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "categoria" / cat_slug / "index.html"
    write_html(out, html)
    return canonical

# ──────────────────────────────────────────────────────────────────
# GENERAR PÁGINA CATEGORÍA PRINCIPAL (8 agrupaciones)
# ──────────────────────────────────────────────────────────────────
def gen_categoria_principal(env, lang, cat_principal, comercios_all, categorias, categorias_activas, config):
    tmpl = env.get_template("categoria_principal.html")
    cat_slug = cat_principal["slug"]
    canonical = f"{SITE_URL}/{lang}/categoria/{cat_slug}/"

    # Collect all comercios in any subcategoria of this main cat
    sub_slugs = set(cat_principal["subcategorias"])
    comercios_cat = []
    seen = set()
    for c in comercios_all:
        for cs in c.get("categorias", []):
            if cs in sub_slugs and c["slug"] not in seen:
                comercios_cat.append(c)
                seen.add(c["slug"])
                break

    cat_nombre_str = cat_principal["nombre"].get(lang) or cat_principal["nombre"].get("es") or cat_slug
    title = f"{cat_nombre_str} en Ferrol | CCA Ferrol Comercio"
    if len(title) > 60:
        title = f"{cat_nombre_str} | CCA Ferrol"

    if lang == "gl":
        desc = f"Comercios de {cat_nombre_str} no barrio de A Magdalena en Ferrol. {len(comercios_cat)} establecementos."
    else:
        desc = f"Comercios de {cat_nombre_str} en el barrio de A Magdalena en Ferrol. {len(comercios_cat)} establecimientos."
    if len(desc) > 155:
        desc = desc[:152] + "..."

    geo = [c for c in comercios_to_geo(comercios_cat, categorias, lang) if c]

    # Subcategorias activas (with comercios)
    subcategorias_activas = cat_principal.get("subcategorias_data", [])

    ctx = base_ctx(lang, config, comercios_cat, categorias_activas,
                   title, desc, canonical, use_map=bool(geo))
    ctx.update({
        "cat_principal": cat_principal,
        "comercios": comercios_cat,
        "subcategorias_activas": subcategorias_activas,
        "categorias": categorias,
        "comercios_geo": geo,
    })

    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "categoria" / cat_slug / "index.html"
    write_html(out, html)
    return canonical


# ──────────────────────────────────────────────────────────────────
# GENERAR PÁGINA TODOS LOS COMERCIOS
# ──────────────────────────────────────────────────────────────────
def gen_comercios_all(env, lang, comercios, categorias, categorias_activas, config):
    """Genera dist/{lang}/comercios/index.html con todos los comercios."""
    # Reusar template de categoría con una 'categoría' fake
    tmpl = env.get_template("categoria.html")
    canonical = f"{SITE_URL}/{lang}/comercios/"

    if lang == "gl":
        title = "Todos os Comercios | CCA Ferrol Comercio"
        desc = f"Directorio completo dos {len(comercios)} comercios do barrio de A Magdalena en Ferrol."
        cat_fake = {"slug": "comercios", "nombre": {"gl": "Todos os comercios", "es": "Todos los comercios"}, "icon": "fas fa-store", "count": len(comercios)}
    else:
        title = "Todos los Comercios | CCA Ferrol Comercio"
        desc = f"Directorio completo de los {len(comercios)} comercios del barrio de A Magdalena en Ferrol."
        cat_fake = {"slug": "comercios", "nombre": {"gl": "Todos os comercios", "es": "Todos los comercios"}, "icon": "fas fa-store", "count": len(comercios)}

    geo = comercios_to_geo(comercios, categorias, lang)

    ctx = base_ctx(lang, config, comercios, categorias_activas,
                   title, desc, canonical, current_page="comercios", use_map=bool(geo))
    ctx.update({
        "categoria": cat_fake,
        "comercios": sorted(comercios, key=lambda c: c.get("nombre", {}).get(lang) or c.get("nombre", {}).get("es") or ""),
        "todas_categorias": categorias_activas,
        "comercios_geo": geo,
    })

    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "comercios" / "index.html"
    write_html(out, html)
    print(f"  → {lang}/comercios/index.html")
    return canonical

# ──────────────────────────────────────────────────────────────────
# GENERAR PÁGINAS ESTÁTICAS
# ──────────────────────────────────────────────────────────────────
STATIC_PAGES = {
    "asociados": {
        "gl": {
            "title": "Asociados | CCA Ferrol Comercio",
            "desc": "Comercios asociados ao Centro Comercial Aberto de A Magdalena en Ferrol.",
            "page_title": "Asociados da CCA",
            "page_subtitle": "Comercios que forman parte do Centro Comercial Aberto",
            "body": """
<div style="max-width:720px;">
  <h2>Os nosos asociados</h2>
  <p>A CCA Ferrol Comercio agrupa aos comercios do barrio de A Magdalena en Ferrol. Xuntos traballamos para dinamizar o comercio local e ofrecer a mellor experiencia de compra na nosa cidade.</p>
  <p>Se es un comerciante da zona e queres formar parte da nosa asociación, non dubides en poñerte en contacto connosco.</p>
  <div style="margin-top:2rem;">
    <a href="BASEURL/gl/contacto/" class="btn btn--primary">Contactar coa CCA</a>
    <a href="BASEURL/gl/comercios/" class="btn btn--secondary" style="margin-left:.75rem;">Ver comercios</a>
  </div>
</div>""",
        },
        "es": {
            "title": "Asociados | CCA Ferrol Comercio",
            "desc": "Comercios asociados al Centro Comercial Abierto de A Magdalena en Ferrol.",
            "page_title": "Asociados de la CCA",
            "page_subtitle": "Comercios que forman parte del Centro Comercial Abierto",
            "body": """
<div style="max-width:720px;">
  <h2>Nuestros asociados</h2>
  <p>La CCA Ferrol Comercio agrupa a los comercios del barrio de A Magdalena en Ferrol. Juntos trabajamos para dinamizar el comercio local y ofrecer la mejor experiencia de compra en nuestra ciudad.</p>
  <p>Si eres un comerciante de la zona y quieres formar parte de nuestra asociación, no dudes en ponerte en contacto con nosotros.</p>
  <div style="margin-top:2rem;">
    <a href="BASEURL/es/contacto/" class="btn btn--primary">Contactar con la CCA</a>
    <a href="BASEURL/es/comercios/" class="btn btn--secondary" style="margin-left:.75rem;">Ver comercios</a>
  </div>
</div>""",
        },
    },
    "contacto": {
        "gl": {
            "title": "Contacto | CCA Ferrol Comercio",
            "desc": "Contacta coa CCA Ferrol Comercio. Asociación de comerciantes do barrio de A Magdalena en Ferrol.",
            "page_title": "Contacto",
            "page_subtitle": "Estamos aquí para axudarte",
            "body": """
<div style="display:grid; grid-template-columns:1fr; gap:3rem;">
  <div class="contact-form">
    <h2>Envíanos unha mensaxe</h2>
    <p style="color:var(--color-text-muted); margin-bottom:1.5rem;">Cubre o formulario e poñerémonos en contacto contigo o antes posible.</p>
    <form action="#" method="post">
      <div class="form-group">
        <label for="contact-name">Nome</label>
        <input type="text" id="contact-name" name="name" required placeholder="O teu nome">
      </div>
      <div class="form-group">
        <label for="contact-email">Email</label>
        <input type="email" id="contact-email" name="email" required placeholder="email@exemplo.com">
      </div>
      <div class="form-group">
        <label for="contact-subject">Asunto</label>
        <input type="text" id="contact-subject" name="subject" placeholder="Asunto da mensaxe">
      </div>
      <div class="form-group">
        <label for="contact-message">Mensaxe</label>
        <textarea id="contact-message" name="message" required placeholder="Escribe a túa mensaxe..."></textarea>
      </div>
      <button type="submit" class="btn btn--primary btn--lg">Enviar mensaxe</button>
    </form>
  </div>
</div>""",
        },
        "es": {
            "title": "Contacto | CCA Ferrol Comercio",
            "desc": "Contacta con la CCA Ferrol Comercio. Asociación de comerciantes del barrio de A Magdalena en Ferrol.",
            "page_title": "Contacto",
            "page_subtitle": "Estamos aquí para ayudarte",
            "body": """
<div style="display:grid; grid-template-columns:1fr; gap:3rem;">
  <div class="contact-form">
    <h2>Envíanos un mensaje</h2>
    <p style="color:var(--color-text-muted); margin-bottom:1.5rem;">Rellena el formulario y nos pondremos en contacto contigo lo antes posible.</p>
    <form action="#" method="post">
      <div class="form-group">
        <label for="contact-name">Nombre</label>
        <input type="text" id="contact-name" name="name" required placeholder="Tu nombre">
      </div>
      <div class="form-group">
        <label for="contact-email">Email</label>
        <input type="email" id="contact-email" name="email" required placeholder="email@ejemplo.com">
      </div>
      <div class="form-group">
        <label for="contact-subject">Asunto</label>
        <input type="text" id="contact-subject" name="subject" placeholder="Asunto del mensaje">
      </div>
      <div class="form-group">
        <label for="contact-message">Mensaje</label>
        <textarea id="contact-message" name="message" required placeholder="Escribe tu mensaje..."></textarea>
      </div>
      <button type="submit" class="btn btn--primary btn--lg">Enviar mensaje</button>
    </form>
  </div>
</div>""",
        },
    },
    "noticias": {
        "gl": {
            "title": "Noticias | CCA Ferrol Comercio",
            "desc": "Últimas noticias e novidades do Centro Comercial Aberto de A Magdalena en Ferrol.",
            "page_title": "Noticias",
            "page_subtitle": "Últimas novidades da CCA Ferrol Comercio",
            "body": """
<div style="max-width:720px;">
  <div style="background:var(--color-primary-light); border-radius:var(--radius); padding:3rem; text-align:center;">
    <i class="fas fa-newspaper" style="font-size:3rem; color:var(--color-primary); margin-bottom:1rem; display:block;" aria-hidden="true"></i>
    <h2 style="margin-bottom:.75rem;">Proximamente</h2>
    <p style="color:var(--color-text-muted);">Estamos traballando no noso blog de noticias. Moi pronto poderás estar ao día de todas as novidades do comercio en A Magdalena.</p>
  </div>
</div>""",
        },
        "es": {
            "title": "Noticias | CCA Ferrol Comercio",
            "desc": "Últimas noticias y novedades del Centro Comercial Abierto de A Magdalena en Ferrol.",
            "page_title": "Noticias",
            "page_subtitle": "Últimas novedades de la CCA Ferrol Comercio",
            "body": """
<div style="max-width:720px;">
  <div style="background:var(--color-primary-light); border-radius:var(--radius); padding:3rem; text-align:center;">
    <i class="fas fa-newspaper" style="font-size:3rem; color:var(--color-primary); margin-bottom:1rem; display:block;" aria-hidden="true"></i>
    <h2 style="margin-bottom:.75rem;">Próximamente</h2>
    <p style="color:var(--color-text-muted);">Estamos trabajando en nuestro blog de noticias. Muy pronto podrás estar al día de todas las novedades del comercio en A Magdalena.</p>
  </div>
</div>""",
        },
    },
}


# ──────────────────────────────────────────────────────────────────
# PÁGINAS INSTITUCIONALES
# ──────────────────────────────────────────────────────────────────
INSTITUTIONAL_PAGES = [
    {
        "template": "sobre-nos.html",
        "output_gl": "gl/sobre-nos/index.html",
        "output_es": "es/sobre-nosotros/index.html",
        "slug_gl": "sobre-nos",
        "slug_es": "sobre-nosotros",
        "current_page": "sobre-nos",
        "meta": {
            "gl": {
                "title": "Quen Somos — CCA Ferrol A Magdalena | Comercio Local dende 1990",
                "desc": "Coñece a CCA Ferrol A Magdalena, asociación de comerciantes do barrio histórico de A Magdalena en Ferrol. +150 socios, +30 anos de historia.",
            },
            "es": {
                "title": "Quiénes Somos — CCA Ferrol A Magdalena | Comercio Local desde 1990",
                "desc": "Conoce la CCA Ferrol A Magdalena, asociación de comerciantes del barrio histórico de A Magdalena en Ferrol. +150 socios, +30 años de historia.",
            },
        },
    },
    {
        "template": "fai-parte.html",
        "output_gl": "gl/fai-parte/index.html",
        "output_es": "es/hazte-socio/index.html",
        "slug_gl": "fai-parte",
        "slug_es": "hazte-socio",
        "current_page": "fai-parte",
        "meta": {
            "gl": {
                "title": "Únete ao CCA Ferrol | Asociación Comerciantes A Magdalena",
                "desc": "Fai parte do CCA Ferrol A Magdalena. Visibilidade dixital, campañas, parking gratuíto e máis beneficios para o teu negocio en Ferrol.",
            },
            "es": {
                "title": "Únete al CCA Ferrol | Asociación Comerciantes A Magdalena",
                "desc": "Hazte socio del CCA Ferrol A Magdalena. Visibilidad digital, campañas, parking gratuito y más beneficios para tu negocio en Ferrol.",
            },
        },
    },
    {
        "template": "eventos.html",
        "output_gl": "gl/eventos/index.html",
        "output_es": "es/eventos/index.html",
        "slug_gl": "eventos",
        "slug_es": "eventos",
        "current_page": "eventos",
        "meta": {
            "gl": {
                "title": "Eventos e Campañas | CCA Ferrol A Magdalena",
                "desc": "Descobre os eventos e campañas do barrio de A Magdalena: Fashion Night, Nadal, San Valentín, Black Friday e moito máis.",
            },
            "es": {
                "title": "Eventos y Campañas | CCA Ferrol A Magdalena",
                "desc": "Descubre los eventos y campañas del barrio de A Magdalena: Fashion Night, Navidad, San Valentín, Black Friday y mucho más.",
            },
        },
    },
    {
        "template": "prensa.html",
        "output_gl": "gl/prensa/index.html",
        "output_es": "es/prensa/index.html",
        "slug_gl": "prensa",
        "slug_es": "prensa",
        "current_page": "prensa",
        "meta": {
            "gl": {
                "title": "Sala de Prensa | CCA Ferrol A Magdalena",
                "desc": "Kit de prensa, notas de prensa e recursos para medios de comunicación sobre a CCA Ferrol A Magdalena.",
            },
            "es": {
                "title": "Sala de Prensa | CCA Ferrol A Magdalena",
                "desc": "Kit de prensa, notas de prensa y recursos para medios de comunicación sobre la CCA Ferrol A Magdalena.",
            },
        },
    },
]


def gen_institutional_pages(env, categorias_activas, config, comercios):
    """Genera las páginas institucionales (sobre-nos, fai-parte, eventos, prensa)."""
    urls = []
    for page in INSTITUTIONAL_PAGES:
        tmpl = env.get_template(page["template"])
        for lang in LANGS:
            slug = page[f"slug_{lang}"]
            output = page[f"output_{lang}"]
            meta = page["meta"][lang]
            canonical = f"{SITE_URL}/{lang}/{slug}/"

            # Build alternate URLs
            url_gl = f"{SITE_URL}/gl/{page['slug_gl']}/"
            url_es = f"{SITE_URL}/es/{page['slug_es']}/"

            ctx = base_ctx(lang, config, comercios, categorias_activas,
                           meta["title"], meta["desc"], canonical,
                           current_page=page["current_page"])
            # Override url_gl/url_es for cross-language links
            ctx["url_gl"] = url_gl
            ctx["url_es"] = url_es

            html = tmpl.render(**ctx)
            out = DIST_DIR / output
            write_html(out, html)

        urls.append({
            "gl": f"{SITE_URL}/gl/{page['slug_gl']}/",
            "es": f"{SITE_URL}/es/{page['slug_es']}/",
            "priority": "0.7",
        })
        print(f"  → {page['template'].replace('.html','')}/ (gl + es)")

    return urls


def gen_static_pages(env, categorias_activas, config, comercios):
    """Genera las páginas estáticas (sobre-nos, contacto, asociados, noticias)."""
    tmpl = env.get_template("static.html")
    urls = []

    for slug, content in STATIC_PAGES.items():
        for lang in LANGS:
            data = content[lang]
            canonical = f"{SITE_URL}/{lang}/{slug}/"

            body = data["body"].replace("BASEURL", SITE_URL)

            ctx = base_ctx(lang, config, comercios, categorias_activas,
                           data["title"], data["desc"], canonical,
                           current_page=slug)
            ctx.update({
                "page_title": data["page_title"],
                "page_subtitle": data.get("page_subtitle", ""),
                "page_body": body,
            })

            html = tmpl.render(**ctx)
            out = DIST_DIR / lang / slug / "index.html"
            write_html(out, html)

        urls.append({
            "gl": f"{SITE_URL}/gl/{slug}/",
            "es": f"{SITE_URL}/es/{slug}/",
            "priority": "0.5",
        })
        print(f"  → {slug}/ (gl + es)")

    return urls


# ──────────────────────────────────────────────────────────────────
# GENERAR 404
# ──────────────────────────────────────────────────────────────────
def gen_404(env, lang, categorias_activas, config, comercios):
    tmpl = env.get_template("404.html")
    canonical = f"{SITE_URL}/{lang}/404.html"

    if lang == "gl":
        title = "Páxina non atopada (404) | CCA Ferrol Comercio"
        desc = "A páxina que buscas non existe. Volve ao inicio do directorio de comercios de Ferrol."
    else:
        title = "Página no encontrada (404) | CCA Ferrol Comercio"
        desc = "La página que buscas no existe. Vuelve al inicio del directorio de comercios de Ferrol."

    ctx = base_ctx(lang, config, comercios, categorias_activas,
                   title, desc, canonical)
    html = tmpl.render(**ctx)
    out = DIST_DIR / lang / "404.html"
    write_html(out, html)
    print(f"  → {lang}/404.html")

# ──────────────────────────────────────────────────────────────────
# SITEMAP
# ──────────────────────────────────────────────────────────────────
def gen_sitemap(url_list):
    """Genera sitemap.xml con hreflang alternates."""
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')

    for entry in url_list:
        url_gl = entry["gl"]
        url_es = entry["es"]
        priority = entry.get("priority", "0.8")
        lines.append("  <url>")
        lines.append(f"    <loc>{url_gl}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="gl" href="{url_gl}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{url_es}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_gl}"/>')
        lines.append("  </url>")
        if url_es != url_gl:
            lines.append("  <url>")
            lines.append(f"    <loc>{url_es}</loc>")
            lines.append(f"    <lastmod>{today}</lastmod>")
            lines.append(f"    <priority>{priority}</priority>")
            lines.append(f'    <xhtml:link rel="alternate" hreflang="gl" href="{url_gl}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{url_es}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_gl}"/>')
            lines.append("  </url>")

    lines.append("</urlset>")
    sitemap_path = DIST_DIR / "sitemap.xml"
    sitemap_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → sitemap.xml ({len(url_list)} grupos de URLs)")

# ──────────────────────────────────────────────────────────────────
# ROBOTS.TXT
# ──────────────────────────────────────────────────────────────────
def gen_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (DIST_DIR / "robots.txt").write_text(content)
    print("  → robots.txt")

# ──────────────────────────────────────────────────────────────────
# COPIAR ASSETS
# ──────────────────────────────────────────────────────────────────
def copy_assets():
    dst = DIST_DIR / "assets"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ASSETS_DIR, dst)
    print(f"  → assets/ copiados")

# ──────────────────────────────────────────────────────────────────
# REDIRECT INDEX RAÍZ
# ──────────────────────────────────────────────────────────────────
def gen_root_redirect():
    """Redirige / → /gl/ por defecto."""
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={SITE_URL}/gl/">
  <link rel="canonical" href="{SITE_URL}/gl/">
  <title>CCA Ferrol Comercio</title>
</head>
<body>
  <p>Redirixindo... <a href="{SITE_URL}/gl/">CCA Ferrol Comercio</a></p>
</body>
</html>"""
    (DIST_DIR / "index.html").write_text(html, encoding="utf-8")
    print("  → index.html (redirect → /gl/)")

# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────
def main():
    print("🏗️  Ferrolcomercio.es v2 — Build")
    print("=" * 50)

    # Limpiar dist
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Cargar datos
    print("\n📦 Cargando datos...")
    comercios, categorias, categorias_activas, categorias_principales, config = load_data()
    print(f"   {len(comercios)} comercios | {len(categorias_activas)} categorías activas | {len(categorias_principales)} categorías principales")

    # Entorno Jinja2
    env = make_env()

    # URLs para sitemap
    sitemap_urls = []

    # ── HOMES ──────────────────────────────────────────────────────
    print("\n🏠 Generando homes...")
    for lang in LANGS:
        url = gen_home(env, lang, comercios, categorias, categorias_activas, categorias_principales, config)

    sitemap_urls.append({
        "gl": f"{SITE_URL}/gl/",
        "es": f"{SITE_URL}/es/",
        "priority": "1.0",
    })

    # ── TODOS LOS COMERCIOS ─────────────────────────────────────────
    print("\n🏪 Generando página de todos los comercios...")
    for lang in LANGS:
        gen_comercios_all(env, lang, comercios, categorias, categorias_activas, config)
    sitemap_urls.append({
        "gl": f"{SITE_URL}/gl/comercios/",
        "es": f"{SITE_URL}/es/comercios/",
        "priority": "0.9",
    })

    # ── FICHAS ─────────────────────────────────────────────────────
    print(f"\n📋 Generando fichas ({len(comercios)} comercios × {len(LANGS)} idiomas)...")
    for comercio in comercios:
        slug = comercio["slug"]
        for lang in LANGS:
            gen_ficha(env, lang, comercio, categorias, categorias_activas, config)
        sitemap_urls.append({
            "gl": f"{SITE_URL}/gl/comercio/{slug}/",
            "es": f"{SITE_URL}/es/comercio/{slug}/",
            "priority": "0.8",
        })
    print(f"   {len(comercios)} fichas × {len(LANGS)} idiomas = {len(comercios)*len(LANGS)} páginas")

    # ── CATEGORÍAS PRINCIPALES ──────────────────────────────────────
    print(f"\n🏷️  Generando páginas de categorías principales ({len(categorias_principales)})...")
    for mc in categorias_principales:
        for lang in LANGS:
            gen_categoria_principal(env, lang, mc, comercios, categorias, categorias_activas, config)
        sitemap_urls.append({
            "gl": f"{SITE_URL}/gl/categoria/{mc['slug']}/",
            "es": f"{SITE_URL}/es/categoria/{mc['slug']}/",
            "priority": "0.8",
        })
    print(f"   {len(categorias_principales)} categorías principales × {len(LANGS)} idiomas generadas")

    # ── SUBCATEGORÍAS ──────────────────────────────────────────────
    print(f"\n🏷️  Generando páginas de subcategoría ({len(categorias_activas)} categorías)...")
    for cat in categorias_activas:
        # Comercios de esta categoría
        comercios_cat = [c for c in comercios if cat["slug"] in c.get("categorias", [])]
        for lang in LANGS:
            gen_categoria(env, lang, cat, comercios_cat, categorias, categorias_activas, config)
        sitemap_urls.append({
            "gl": f"{SITE_URL}/gl/categoria/{cat['slug']}/",
            "es": f"{SITE_URL}/es/categoria/{cat['slug']}/",
            "priority": "0.7",
        })
    print(f"   {len(categorias_activas)} categorías × {len(LANGS)} idiomas generadas")

    # ── PÁGINAS INSTITUCIONALES ─────────────────────────────────────
    print("\n🏛️  Generando páginas institucionales...")
    inst_urls = gen_institutional_pages(env, categorias_activas, config, comercios)
    sitemap_urls.extend(inst_urls)

    # ── PÁGINAS ESTÁTICAS ──────────────────────────────────────────
    print("\n📄 Generando páginas estáticas...")
    static_urls = gen_static_pages(env, categorias_activas, config, comercios)
    sitemap_urls.extend(static_urls)

    # ── 404 ────────────────────────────────────────────────────────
    print("\n❌ Generando páginas 404...")
    for lang in LANGS:
        gen_404(env, lang, categorias_activas, config, comercios)

    # ── ASSETS ─────────────────────────────────────────────────────
    print("\n📁 Copiando assets...")
    copy_assets()

    # ── ROOT REDIRECT ───────────────────────────────────────────────
    print("\n🔀 Generando redirect raíz...")
    gen_root_redirect()

    # ── SITEMAP & ROBOTS ───────────────────────────────────────────
    print("\n🗺️  Generando sitemap.xml y robots.txt...")
    gen_sitemap(sitemap_urls)
    gen_robots()

    # ── RESUMEN ────────────────────────────────────────────────────
    total_html = sum(1 for _ in DIST_DIR.rglob("*.html"))
    total_bytes = sum(f.stat().st_size for f in DIST_DIR.rglob("*") if f.is_file())
    print("\n" + "=" * 50)
    print(f"✅ Build completado!")
    print(f"   📄 {total_html} páginas HTML generadas")
    print(f"   🗺️  {len(sitemap_urls)} grupos URL en sitemap")
    print(f"   💾 {total_bytes/1024/1024:.1f} MB total en dist/")
    print(f"   📂 dist/ → {DIST_DIR}")
    print("=" * 50)

if __name__ == "__main__":
    main()
