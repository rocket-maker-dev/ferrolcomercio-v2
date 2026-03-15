<?php
/**
 * ferrol-reviews.php — Proxy para Google Places API (reseñas y detalles)
 * Endpoints:
 *   GET ?action=reviews&place_id=ChIJxxx  → hasta 5 reseñas
 *   GET ?action=details&place_id=ChIJxxx  → rating, totalReviews, opening_hours
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

// ── Config ──────────────────────────────────────────────────────────────────
define('GOOGLE_API_KEY', 'AIzaSyAr_HTQJMRqnhdAF7VHj-KmM9nqy53eAAc');
define('PLACES_URL', 'https://maps.googleapis.com/maps/api/place/details/json');
define('CACHE_DIR', __DIR__ . '/../cache/reviews');
define('CACHE_TTL', 86400); // 24h cache
define('LOG_FILE', '/home/u297969817/logs/ferrol-reviews.log');

function rv_log($msg) {
    @file_put_contents(LOG_FILE, date('Y-m-d H:i:s') . " $msg\n", FILE_APPEND);
}

function fetch_place_details($place_id, $fields) {
    $url = PLACES_URL . '?' . http_build_query([
        'place_id' => $place_id,
        'fields'   => $fields,
        'key'      => GOOGLE_API_KEY,
        'language'  => 'es'
    ]);

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
        CURLOPT_SSL_VERIFYPEER => false
    ]);
    $resp = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    curl_close($ch);

    if ($err) { rv_log("CURL error: $err"); return null; }
    if ($code !== 200) { rv_log("HTTP $code for $place_id"); return null; }

    $data = json_decode($resp, true);
    if (($data['status'] ?? '') !== 'OK') {
        rv_log("API status: " . ($data['status'] ?? 'unknown') . " for $place_id");
        return null;
    }
    return $data['result'] ?? null;
}

function get_cached($key) {
    $file = CACHE_DIR . '/' . md5($key) . '.json';
    if (!file_exists($file)) return null;
    if (time() - filemtime($file) > CACHE_TTL) return null;
    return json_decode(file_get_contents($file), true);
}

function set_cached($key, $data) {
    if (!is_dir(CACHE_DIR)) @mkdir(CACHE_DIR, 0755, true);
    $file = CACHE_DIR . '/' . md5($key) . '.json';
    @file_put_contents($file, json_encode($data, JSON_UNESCAPED_UNICODE));
}

// ── Routing ─────────────────────────────────────────────────────────────────
$action   = $_GET['action'] ?? '';
$place_id = trim($_GET['place_id'] ?? '');

if (empty($place_id) || !preg_match('/^ChIJ[A-Za-z0-9_-]+$/', $place_id)) {
    echo json_encode(['error' => 'place_id inválido ou ausente']);
    exit;
}

switch ($action) {
    case 'reviews':  handle_reviews($place_id);  break;
    case 'details':  handle_details($place_id);  break;
    default:
        echo json_encode(['error' => 'Acción non válida. Usa: reviews, details']);
}

// ── Reviews ─────────────────────────────────────────────────────────────────
function handle_reviews($place_id) {
    $cacheKey = "reviews:$place_id";
    $cached = get_cached($cacheKey);
    if ($cached) {
        $cached['cached'] = true;
        echo json_encode($cached, JSON_UNESCAPED_UNICODE);
        return;
    }

    $result = fetch_place_details($place_id, 'reviews,rating,user_ratings_total,name');
    if (!$result) {
        echo json_encode(['error' => 'Non se puideron obter as reseñas', 'reviews' => []]);
        return;
    }

    $reviews = [];
    foreach (($result['reviews'] ?? []) as $r) {
        $reviews[] = [
            'author'      => $r['author_name'] ?? '',
            'avatar'      => $r['profile_photo_url'] ?? '',
            'rating'      => $r['rating'] ?? 0,
            'text'        => $r['text'] ?? '',
            'time'        => $r['relative_time_description'] ?? '',
            'timestamp'   => $r['time'] ?? 0,
            'language'    => $r['language'] ?? 'es'
        ];
    }

    // Sort by most recent
    usort($reviews, function($a, $b) { return $b['timestamp'] - $a['timestamp']; });
    $reviews = array_slice($reviews, 0, 5);

    $out = [
        'place_id'     => $place_id,
        'name'         => $result['name'] ?? '',
        'rating'       => $result['rating'] ?? null,
        'totalReviews' => $result['user_ratings_total'] ?? 0,
        'reviews'      => $reviews,
        'cached'       => false
    ];

    set_cached($cacheKey, $out);
    echo json_encode($out, JSON_UNESCAPED_UNICODE);
    rv_log("REVIEWS OK: $place_id — " . count($reviews) . " reviews");
}

// ── Details ─────────────────────────────────────────────────────────────────
function handle_details($place_id) {
    $cacheKey = "details:$place_id";
    $cached = get_cached($cacheKey);
    if ($cached) {
        $cached['cached'] = true;
        echo json_encode($cached, JSON_UNESCAPED_UNICODE);
        return;
    }

    $result = fetch_place_details($place_id,
        'name,rating,user_ratings_total,opening_hours,formatted_phone_number,website,url,business_status'
    );
    if (!$result) {
        echo json_encode(['error' => 'Non se puideron obter os detalles']);
        return;
    }

    $hours = [];
    if (!empty($result['opening_hours']['weekday_text'])) {
        $hours = $result['opening_hours']['weekday_text'];
    }

    $out = [
        'place_id'       => $place_id,
        'name'           => $result['name'] ?? '',
        'rating'         => $result['rating'] ?? null,
        'totalReviews'   => $result['user_ratings_total'] ?? 0,
        'opening_hours'  => $hours,
        'is_open'        => $result['opening_hours']['open_now'] ?? null,
        'phone'          => $result['formatted_phone_number'] ?? '',
        'website'        => $result['website'] ?? '',
        'maps_url'       => $result['url'] ?? '',
        'business_status'=> $result['business_status'] ?? '',
        'cached'         => false
    ];

    set_cached($cacheKey, $out);
    echo json_encode($out, JSON_UNESCAPED_UNICODE);
    rv_log("DETAILS OK: $place_id");
}
