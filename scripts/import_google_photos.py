#!/usr/bin/env python3
"""
Script de importación de fotos de Google Business para ferrolcomercio.es v2
Descarga hasta 5 fotos por comercio desde Google Places API
Actualiza data/comercios.json con las nuevas rutas de imagen
"""

import json
import os
import time
import urllib.request
import urllib.parse
import hashlib
from pathlib import Path

# Config
API_KEY = "AIzaSyAr_HTQJMRqnhdAF7VHj-KmM9nqy53eAAc"
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "comercios.json"
IMAGES_DIR = BASE_DIR / "assets" / "images" / "comercios"
MAX_PHOTOS = 5
PHOTO_MAX_WIDTH = 800
DELAY = 0.3  # segundos entre requests

# Crear directorio si no existe
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def get_place_photos(place_id):
    """Obtiene referencias de fotos de Google Places API"""
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos,name&key={API_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        if data.get("status") == "OK":
            return data.get("result", {}).get("photos", [])
    except Exception as e:
        print(f"    Error obteniendo fotos: {e}")
    return []

def download_photo(photo_reference, filename):
    """Descarga una foto de Google Places y la guarda localmente"""
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={PHOTO_MAX_WIDTH}&photoreference={photo_reference}&key={API_KEY}"
    filepath = IMAGES_DIR / filename
    
    if filepath.exists():
        return str(filepath.relative_to(BASE_DIR / "assets"))
    
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            # Google redirige a la imagen real
            image_data = resp.read()
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        size_kb = len(image_data) // 1024
        print(f"    ✅ {filename} ({size_kb}KB)")
        return f"images/comercios/{filename}"
    except Exception as e:
        print(f"    ❌ Error descargando {filename}: {e}")
        return None

def main():
    # Cargar datos
    with open(DATA_FILE) as f:
        comercios = json.load(f)
    
    con_place_id = [c for c in comercios if c.get("google_place_id")]
    print(f"📸 Importando fotos de Google Business")
    print(f"   Comercios con place_id: {len(con_place_id)}")
    print(f"   Destino: {IMAGES_DIR}\n")
    
    updated = 0
    errors = 0
    skipped = 0
    
    for i, comercio in enumerate(con_place_id):
        nombre = comercio.get("nombre", "")
        if isinstance(nombre, dict):
            nombre = nombre.get("es") or nombre.get("gl") or "?"
        
        place_id = comercio["google_place_id"]
        slug = comercio.get("slug", place_id)
        
        # Comprobar si ya tiene imágenes locales descargadas
        existing = comercio.get("imagenes", [])
        already_downloaded = any(
            str(img).startswith("images/comercios/") 
            for img in existing if isinstance(img, str)
        ) if existing else False
        
        if already_downloaded:
            skipped += 1
            print(f"[{i+1:3d}/{len(con_place_id)}] ⏭️  {nombre[:50]} — ya importado")
            continue
        
        print(f"[{i+1:3d}/{len(con_place_id)}] 📷 {nombre[:50]}")
        
        # Obtener referencias de fotos
        photos = get_place_photos(place_id)
        time.sleep(DELAY)
        
        if not photos:
            print(f"    ⚠️  Sin fotos en Google Business")
            errors += 1
            continue
        
        # Descargar hasta MAX_PHOTOS fotos
        nuevas_imagenes = []
        for j, photo in enumerate(photos[:MAX_PHOTOS]):
            photo_ref = photo.get("photo_reference", "") or photo.get("photoreference", "")
            if not photo_ref:
                continue
            
            # Nombre de archivo: slug-1.jpg, slug-2.jpg, etc.
            filename = f"{slug}-{j+1}.jpg"
            local_path = download_photo(photo_ref, filename)
            
            if local_path:
                nuevas_imagenes.append(local_path)
            
            time.sleep(DELAY)
        
        if nuevas_imagenes:
            # Encontrar el índice en el array original de comercios
            idx = next((k for k, c in enumerate(comercios) if c.get("slug") == comercio.get("slug")), None)
            if idx is not None:
                comercios[idx]["imagenes"] = nuevas_imagenes
                comercios[idx]["imagen_destacada"] = nuevas_imagenes[0]
                updated += 1
                print(f"    ✅ {len(nuevas_imagenes)} fotos guardadas")
        else:
            errors += 1
    
    # Guardar JSON actualizado
    with open(DATA_FILE, 'w', ensure_ascii=False) as f:
        json.dump(comercios, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ Completado:")
    print(f"   Actualizados: {updated} comercios")
    print(f"   Omitidos (ya tenían fotos): {skipped}")
    print(f"   Sin fotos en Google: {errors}")
    print(f"   JSON actualizado: {DATA_FILE}")

if __name__ == "__main__":
    main()
