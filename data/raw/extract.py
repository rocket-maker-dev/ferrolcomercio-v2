#!/usr/bin/env python3
"""
Extractor de datos de ferrolcomercio.es
Parsea el XML export de WordPress y extrae todos los listings/comercios
"""
import xml.etree.ElementTree as ET
import json
import re
import html
from pathlib import Path

XML_FILE = '/Users/polaris/.openclaw/workspace/backups/ferrolcomercio/ferrolcomercio_export_20260218.xml'
OUTPUT_DIR = Path('/Users/polaris/.openclaw/workspace/projects/ferrolcomercio-v2/data')

NS = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}


def parse_php_serialize(s):
    """Parse PHP serialized arrays like a:2:{i:0;s:5:"09:00";i:1;s:5:"15:00";}"""
    if not s or not s.startswith('a:'):
        return s
    result = []
    # Simple extraction of string values
    matches = re.findall(r's:\d+:"([^"]*)"', s)
    return matches


def parse_gallery(s):
    """Parse gallery PHP serialized: a:N:{i:ID;s:N:"URL";}"""
    if not s:
        return []
    urls = re.findall(r's:\d+:"(https?://[^"]+)"', s)
    # Convert absolute URLs to relative paths
    clean = []
    for u in urls:
        u = u.replace('https://ferrolcomercio.es/wp-content/uploads/', 'uploads/')
        u = u.replace('http://ferrolcomercio.es/wp-content/uploads/', 'uploads/')
        u = u.replace('https://ferrolcomercio.es/wp-content/', 'uploads/')
        u = u.replace('http://ferrolcomercio.es/wp-content/', 'uploads/')
        clean.append(u)
    return clean


def clean_url(url):
    """Clean and relativize a URL"""
    if not url:
        return None
    url = url.strip()
    if not url:
        return None
    url = url.replace('https://ferrolcomercio.es/wp-content/uploads/', 'uploads/')
    url = url.replace('http://ferrolcomercio.es/wp-content/uploads/', 'uploads/')
    url = url.replace('https://ferrolcomercio.es/wp-content/', 'uploads/')
    url = url.replace('http://ferrolcomercio.es/wp-content/', 'uploads/')
    return url


def extract_from_content(content_html):
    """Extract phone, email, web from content HTML if not in meta"""
    data = {}
    if not content_html:
        return data
    # Phone: 📞 or tel:
    phone_match = re.search(r'📞\s*([+\d\s\-()]{7,20})', content_html)
    if phone_match:
        data['phone_from_content'] = phone_match.group(1).strip()
    # Rating: ⭐ 4.9
    rating_match = re.search(r'⭐\s*([\d.]+)', content_html)
    if rating_match:
        data['rating_from_content'] = float(rating_match.group(1))
    # Web: href
    web_match = re.search(r'🌐.*?href="([^"]+)"', content_html)
    if web_match:
        data['web_from_content'] = web_match.group(1)
    return data


def parse_opening_hours(meta):
    """Build opening hours dict from _monday_opening_hour etc."""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    days_es = {'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miercoles',
               'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sabado', 'sunday': 'domingo'}
    hours = {}
    for day in days:
        open_key = f'_{day}_opening_hour'
        close_key = f'_{day}_closing_hour'
        open_val = meta.get(open_key)
        close_val = meta.get(close_key)
        if open_val:
            opens = parse_php_serialize(open_val)
            closes = parse_php_serialize(close_val) if close_val else []
            if opens:
                slots = []
                for i, o in enumerate(opens):
                    c = closes[i] if i < len(closes) else None
                    if c:
                        slots.append(f'{o}-{c}')
                    else:
                        slots.append(o)
                hours[days_es[day]] = slots
    return hours if hours else None


def main():
    print(f'Parsing XML: {XML_FILE}')
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    channel = root.find('channel')

    # --- Extract categories ---
    categories = []
    cat_by_slug = {}
    for term in channel.findall('wp:term', NS):
        tax = term.find('wp:term_taxonomy', NS)
        if tax is not None and tax.text == 'listing_category':
            tid = term.find('wp:term_id', NS).text
            slug = term.find('wp:term_slug', NS).text
            name = term.find('wp:term_name', NS).text
            parent_elem = term.find('wp:term_parent', NS)
            parent = parent_elem.text if parent_elem is not None and parent_elem.text else None
            cat_obj = {
                'id': int(tid),
                'slug': slug,
                'nombre': {'es': name, 'gl': None},
                'parent': parent
            }
            categories.append(cat_obj)
            cat_by_slug[slug] = cat_obj
    categories.sort(key=lambda c: c['slug'])

    # --- Extract features/amenities ---
    features = []
    feat_by_slug = {}
    for term in channel.findall('wp:term', NS):
        tax = term.find('wp:term_taxonomy', NS)
        if tax is not None and tax.text == 'listing_feature':
            tid = term.find('wp:term_id', NS).text
            slug = term.find('wp:term_slug', NS).text
            name = term.find('wp:term_name', NS).text
            features.append({'id': int(tid), 'slug': slug, 'nombre': name})
            feat_by_slug[slug] = name

    # --- Extract listings ---
    listings = []
    skipped = 0

    for item in channel.findall('item'):
        post_type_el = item.find('wp:post_type', NS)
        if post_type_el is None or post_type_el.text != 'listing':
            continue

        status_el = item.find('wp:status', NS)
        status = status_el.text if status_el is not None else 'unknown'
        if status not in ('publish', 'draft', 'private'):
            skipped += 1
            continue

        post_id = int(item.find('wp:post_id', NS).text)
        title = item.find('title').text or ''
        slug_el = item.find('wp:post_name', NS)
        slug = slug_el.text if slug_el is not None else ''
        
        content_el = item.find('content:encoded', NS)
        content_html = content_el.text if content_el is not None else ''
        if content_html:
            content_html = content_html.strip()

        post_date_el = item.find('wp:post_date', NS)
        post_date = post_date_el.text if post_date_el is not None else None

        # Categories assigned to this listing
        listing_cats = []
        listing_features = []
        listing_regions = []
        for cat_el in item.findall('category'):
            domain = cat_el.get('domain', '')
            nicename = cat_el.get('nicename', '')
            if domain == 'listing_category':
                listing_cats.append(nicename)
            elif domain == 'listing_feature':
                listing_features.append(nicename)
            elif domain == 'region':
                listing_regions.append(nicename)

        # Meta fields
        meta = {}
        for postmeta in item.findall('wp:postmeta', NS):
            key_el = postmeta.find('wp:meta_key', NS)
            val_el = postmeta.find('wp:meta_value', NS)
            if key_el is not None and val_el is not None:
                k = key_el.text or ''
                v = val_el.text or ''
                meta[k] = v

        # Featured image
        featured_img = None
        thumbnail_id = meta.get('_thumbnail_id')
        # We'll resolve this from attachments later if needed
        # For now get from meta
        
        # Gallery
        gallery_raw = meta.get('_gallery', '')
        gallery_urls = parse_gallery(gallery_raw)

        # Listing logo
        logo_raw = meta.get('_listing_logo', '')
        logo_url = clean_url(logo_raw) if logo_raw else None

        # Opening hours
        opening_hours = parse_opening_hours(meta)

        # Social media
        socials = {}
        for social in ['_facebook', '_instagram', '_twitter', '_linkedin', '_youtube', '_whatsapp']:
            v = meta.get(social, '').strip()
            if v:
                socials[social[1:]] = v

        # Extract from content if no meta
        content_extra = extract_from_content(content_html)

        # Phone
        phone = meta.get('_phone', '').strip() or None
        if not phone and content_extra.get('phone_from_content'):
            phone = content_extra['phone_from_content']

        # Email
        email = meta.get('_email', '').strip() or None

        # Website
        website = meta.get('_website', '').strip() or None
        if not website and content_extra.get('web_from_content'):
            website = content_extra['web_from_content']

        # Rating
        rating = None
        try:
            r = meta.get('_combined_rating') or meta.get('_google_rating')
            if r:
                rating = float(r)
        except:
            pass
        if rating is None and content_extra.get('rating_from_content'):
            rating = content_extra['rating_from_content']

        # Review count
        review_count = None
        try:
            rc = meta.get('_combined_review_count') or meta.get('_google_review_count')
            if rc:
                review_count = int(rc)
        except:
            pass

        # Coordinates
        lat = None
        lng = None
        try:
            lat_s = meta.get('_geolocation_lat', '').strip()
            lng_s = meta.get('_geolocation_long', '').strip()
            if lat_s:
                lat = float(lat_s)
            if lng_s:
                lng = float(lng_s)
        except:
            pass

        # Google Place ID
        place_id = meta.get('_google_place_id', '').strip() or None
        # Also check for place_id in various forms
        if not place_id:
            place_id = meta.get('_place_id', '').strip() or None

        # Address
        address = meta.get('_address', '').strip() or meta.get('_friendly_address', '').strip() or None

        # Featured flag
        featured = meta.get('_featured', '0') == '1' or meta.get('_listing_featured', '0') == '1'

        # Build listing object
        listing = {
            'id': post_id,
            'nombre': {'gl': None, 'es': html.unescape(title)},
            'slug': slug,
            'descripcion': {'gl': None, 'es': html.unescape(content_html) if content_html else None},
            'estado': status,
            'categorias': listing_cats,
            'features': listing_features,
            'region': listing_regions,
            'direccion': address,
            'telefono': phone,
            'email': email,
            'web': website,
            'coordenadas': {'lat': lat, 'lng': lng} if (lat is not None or lng is not None) else None,
            'horarios': opening_hours,
            'google_place_id': place_id,
            'imagenes': gallery_urls,
            'logo': logo_url,
            'rating': rating,
            'num_reviews': review_count,
            'featured': featured,
            'redes_sociales': socials if socials else None,
            'fecha_creacion': post_date,
            '_thumbnail_id': thumbnail_id,
        }
        listings.append(listing)

    print(f'Extracted {len(listings)} listings ({skipped} skipped)')

    # --- Resolve featured images from attachments ---
    attachments = {}
    for item in channel.findall('item'):
        post_type_el = item.find('wp:post_type', NS)
        if post_type_el is None or post_type_el.text != 'attachment':
            continue
        post_id_el = item.find('wp:post_id', NS)
        att_url_el = item.find('wp:attachment_url', NS)
        if post_id_el is not None and att_url_el is not None:
            pid = post_id_el.text
            url = att_url_el.text or ''
            url = clean_url(url)
            attachments[pid] = url

    # Assign featured images
    for listing in listings:
        tid = listing.pop('_thumbnail_id', None)
        if tid and tid in attachments:
            listing['imagen_destacada'] = attachments[tid]
        else:
            listing['imagen_destacada'] = None

    # --- Stats ---
    with_phone = sum(1 for l in listings if l['telefono'])
    with_email = sum(1 for l in listings if l['email'])
    with_web = sum(1 for l in listings if l['web'])
    with_coords = sum(1 for l in listings if l['coordenadas'])
    with_hours = sum(1 for l in listings if l['horarios'])
    with_images = sum(1 for l in listings if l['imagenes'])
    with_featured = sum(1 for l in listings if l['imagen_destacada'])
    published = sum(1 for l in listings if l['estado'] == 'publish')

    print(f'\n📊 ESTADÍSTICAS:')
    print(f'  Total listings: {len(listings)}')
    print(f'  Publicados: {published}')
    print(f'  Con teléfono: {with_phone}')
    print(f'  Con email: {with_email}')
    print(f'  Con web: {with_web}')
    print(f'  Con coordenadas GPS: {with_coords}')
    print(f'  Con horarios: {with_hours}')
    print(f'  Con galería de imágenes: {with_images}')
    print(f'  Con imagen destacada: {with_featured}')
    print(f'  Categorías: {len(categories)}')
    print(f'  Features/amenities: {len(features)}')

    # --- Save outputs ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / 'comercios.json', 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)
    print(f'\n✅ Saved: data/comercios.json ({len(listings)} entries)')

    with open(OUTPUT_DIR / 'categorias.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    print(f'✅ Saved: data/categorias.json ({len(categories)} entries)')

    with open(OUTPUT_DIR / 'features.json', 'w', encoding='utf-8') as f:
        json.dump(features, f, ensure_ascii=False, indent=2)
    print(f'✅ Saved: data/features.json ({len(features)} entries)')

    # Save stats
    stats = {
        'total': len(listings),
        'publicados': published,
        'con_telefono': with_phone,
        'con_email': with_email,
        'con_web': with_web,
        'con_coordenadas': with_coords,
        'con_horarios': with_hours,
        'con_galeria': with_images,
        'con_imagen_destacada': with_featured,
        'categorias': len(categories),
        'features': len(features),
        'datos_faltantes': {
            'sin_telefono': len(listings) - with_phone,
            'sin_email': len(listings) - with_email,
            'sin_web': len(listings) - with_web,
            'sin_coordenadas': len(listings) - with_coords,
            'sin_horarios': len(listings) - with_hours,
            'sin_imagenes': len(listings) - with_images,
        }
    }
    with open(OUTPUT_DIR / 'raw' / 'stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f'✅ Saved: data/raw/stats.json')

    return listings, categories, features


if __name__ == '__main__':
    main()
