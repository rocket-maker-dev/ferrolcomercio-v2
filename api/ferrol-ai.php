<?php
/**
 * ferrol-ai.php — Backend IA para el buscador de CCA Ferrol Comercio
 * Endpoints: search, chat, suggest
 */
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }

// ── Config ──────────────────────────────────────────────────────────────────
define('GEMINI_KEY', 'AIzaSyALI9fUhF-PzpQ7yaRq2stiAv9_BlFQeII');
define('GEMINI_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent');
define('MAX_TOKENS', 1024);
// Try multiple paths for comercios.json
$_jsonPaths = [
    __DIR__ . '/../data/comercios.json',
    __DIR__ . '/data/comercios.json',
    '/home/u297969817/domains/ferrolcomercio.org/public_html/data/comercios.json',
    '/home/u297969817/domains/rocketmaker.app/public_html/cca-preview/data/comercios.json'
];
$_jsonPath = '';
foreach ($_jsonPaths as $_p) { if (file_exists($_p)) { $_jsonPath = $_p; break; } }
define('COMERCIOS_JSON', $_jsonPath ?: $_jsonPaths[0]);
define('LOG_FILE', '/home/u297969817/logs/ferrol-ai.log');

// ── Helpers ─────────────────────────────────────────────────────────────────
function ai_log($msg) {
    @file_put_contents(LOG_FILE, date('Y-m-d H:i:s') . " $msg\n", FILE_APPEND);
}

function load_comercios() {
    static $cache = null;
    if ($cache !== null) return $cache;
    $raw = file_get_contents(COMERCIOS_JSON);
    if (!$raw) { ai_log("ERROR: no se pudo leer comercios.json"); return []; }
    $cache = json_decode($raw, true) ?: [];
    return $cache;
}

function build_directory_context($comercios) {
    $lines = [];
    foreach ($comercios as $c) {
        $nombre = $c['nombre']['gl'] ?? $c['nombre']['es'] ?? '—';
        $cats = implode(', ', $c['categorias'] ?? []);
        $dir = $c['direccion'] ?? '';
        $tel = $c['telefono'] ?? '';
        $desc_raw = $c['descripcion']['gl'] ?? $c['descripcion']['es'] ?? '';
        $desc = mb_substr(strip_tags($desc_raw), 0, 120);
        
        // Horarios compactos
        $horario = '';
        if (!empty($c['horarios'])) {
            $h = $c['horarios'];
            $first = reset($h);
            if ($first) $horario = implode(', ', (array)$first);
        }
        
        $lines[] = "{$c['id']} | {$nombre} | {$cats} | {$dir} | {$tel} | {$horario} | {$desc}";
    }
    return implode("\n", $lines);
}

function call_gemini($system, $messages) {
    // Build Gemini contents array: system instruction + conversation
    $contents = [];
    foreach ($messages as $m) {
        $role = ($m['role'] === 'assistant') ? 'model' : 'user';
        $contents[] = ['role' => $role, 'parts' => [['text' => $m['content']]]];
    }

    $payload = [
        'system_instruction' => ['parts' => [['text' => $system]]],
        'contents' => $contents,
        'generationConfig' => [
            'maxOutputTokens' => MAX_TOKENS,
            'temperature' => 0.3,
        ]
    ];

    $url = GEMINI_URL . '?key=' . GEMINI_KEY;
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($payload),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json']
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) { ai_log("CURL error: $error"); return null; }
    if ($httpCode !== 200) { ai_log("Gemini API error $httpCode: " . substr($response, 0, 500)); return null; }

    $data = json_decode($response, true);
    return $data['candidates'][0]['content']['parts'][0]['text'] ?? null;
}

function get_system_prompt($lang, $directory) {
    $idioma = $lang === 'gl' ? 'galego' : 'español';
    return <<<PROMPT
Eres o asistente intelixente do CCA Ferrol Comercio, o centro comercial aberto do barrio da Magdalena de Ferrol (Galicia).
Axudas aos usuarios a atopar comercios, produtos e servizos no directorio.

Responde SEMPRE en {$idioma}.

DIRECTORIO DE COMERCIOS (ID | Nome | Categoría | Dirección | Teléfono | Horario | Descrición):
{$directory}

INSTRUCIÓNS ESTRITAS (DEBES SEGUIR):
1. Identifica os comercios máis relevantes para a consulta do usuario
2. A TÚA RESPOSTA COMPLETA debe ser UN OBXECTO JSON VÁLIDO e NADA MÁIS
3. Formato EXACTO (sen texto antes nin despois do JSON):
{"resposta": "texto natural aquí", "ids": [1234, 5678]}
4. Se non hai comercios relevantes, suxire categorías e devolve "ids": []
5. Menciona horarios e teléfonos cando sexa útil dentro de "resposta"
6. Máximo 5 comercios
7. NON uses markdown, NON uses bloques de código, SOLO o JSON puro
8. Os IDs deben ser números enteiros existentes no directorio
PROMPT;
}

function get_chat_system_prompt($lang, $directory) {
    $idioma = $lang === 'gl' ? 'galego' : 'español';
    return <<<PROMPT
Eres o asistente conversacional do CCA Ferrol Comercio, o centro comercial aberto do barrio da Magdalena de Ferrol (Galicia).

Responde SEMPRE en {$idioma}. Sé amable, cercano e útil.

DIRECTORIO DE COMERCIOS (ID | Nome | Categoría | Dirección | Teléfono | Horario | Descrición):
{$directory}

INSTRUCIÓNS ESTRITAS (DEBES SEGUIR):
1. Mantén unha conversa natural e amable
2. A TÚA RESPOSTA COMPLETA debe ser UN OBXECTO JSON VÁLIDO e NADA MÁIS
3. Formato EXACTO (sen texto antes nin despois do JSON):
{"resposta": "texto conversacional aquí", "ids": [1234, 5678]}
4. Se o usuario saúda ou fai charla, responde amablemente con "ids": []
5. Se preguntan por horarios, prezos, localización: responde co que saibas
6. Se non sabes algo específico, recomenda contactar co comercio
7. NON uses markdown, NON uses bloques de código, SOLO o JSON puro
PROMPT;
}

function parse_ai_response($result) {
    // Normalize: replace actual newlines inside JSON strings with \n escape
    // This fixes Claude returning literal newlines in JSON values
    $clean = $result;
    
    // Try direct JSON parse
    $parsed = json_decode($clean, true);
    if (!$parsed) {
        // Fix literal newlines: replace newlines within string values
        $clean = preg_replace('/\n/', '\\n', $clean);
        $clean = preg_replace('/\r/', '\\r', $clean);
        $parsed = json_decode($clean, true);
    }
    
    if ($parsed && isset($parsed['resposta'])) {
        // Check if resposta itself is JSON (double-encoded)
        $inner = json_decode($parsed['resposta'], true);
        if ($inner && isset($inner['resposta'])) {
            return $inner;
        }
        // Unescape \n back to actual newlines for display
        $parsed['resposta'] = str_replace('\\n', "\n", $parsed['resposta']);
        return $parsed;
    }
    
    // Try to extract the resposta and ids manually with regex
    $resposta = '';
    $ids = [];
    
    // Extract resposta value (handles multiline)
    if (preg_match('/"resposta"\s*:\s*"((?:[^"\\\\]|\\\\.)*)"/s', $result, $m)) {
        $resposta = stripcslashes($m[1]);
    }
    
    // Extract ids array
    if (preg_match('/"ids"\s*:\s*\[([^\]]*)\]/', $result, $m)) {
        preg_match_all('/(\d+)/', $m[1], $idMatches);
        if (!empty($idMatches[1])) {
            $ids = array_map('intval', $idMatches[1]);
        }
    }
    
    if ($resposta) {
        return ['resposta' => $resposta, 'ids' => $ids];
    }
    
    // Last resort: extract IDs from text
    if (preg_match_all('/\b(\d{4})\b/', $result, $idMatches)) {
        $ids = array_map('intval', array_unique($idMatches[1]));
    }
    
    // Clean up text for display
    $text = $result;
    $text = preg_replace('/```json\s*/i', '', $text);
    $text = preg_replace('/```\s*/', '', $text);
    $text = trim($text);
    
    ai_log("PARSE FALLBACK: " . substr($result, 0, 300));
    return ['resposta' => $text, 'ids' => $ids];
}

// ── Endpoints ───────────────────────────────────────────────────────────────
$action = $_GET['action'] ?? '';

switch ($action) {
    case 'search':
        handle_search();
        break;
    case 'chat':
        handle_chat();
        break;
    case 'suggest':
        handle_suggest();
        break;
    default:
        echo json_encode(['error' => 'Acción non válida. Usa: search, chat, suggest']);
}

// ── Search ──────────────────────────────────────────────────────────────────
function handle_search() {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode(['error' => 'Method POST required']);
        return;
    }
    
    $body = json_decode(file_get_contents('php://input'), true);
    $query = trim($body['query'] ?? '');
    $lang = $body['lang'] ?? 'gl';
    
    if (empty($query)) {
        echo json_encode(['error' => 'Query vacía']);
        return;
    }
    
    ai_log("SEARCH: '$query' [lang=$lang]");
    
    $comercios = load_comercios();
    $directory = build_directory_context($comercios);
    $system = get_system_prompt($lang, $directory);
    
    $result = call_gemini($system, [
        ['role' => 'user', 'content' => $query]
    ]);
    
    if (!$result) {
        echo json_encode(['error' => 'Erro ao procesar a consulta', 'comercios' => [], 'resposta' => '']);
        return;
    }
    
    // Parse JSON response from Claude
    $parsed = parse_ai_response($result);
    
    // Map IDs to full comercio objects
    $ids = $parsed['ids'] ?? [];
    $matched = [];
    $comerciosById = [];
    foreach ($comercios as $c) $comerciosById[$c['id']] = $c;
    
    foreach ($ids as $id) {
        if (isset($comerciosById[$id])) {
            $c = $comerciosById[$id];
            $matched[] = [
                'id' => $c['id'],
                'nombre' => $c['nombre'][$lang] ?? $c['nombre']['es'] ?? $c['nombre']['gl'] ?? '',
                'slug' => $c['slug'],
                'categorias' => $c['categorias'] ?? [],
                'direccion' => $c['direccion'] ?? '',
                'telefono' => $c['telefono'] ?? '',
                'web' => $c['web'] ?? '',
                'rating' => $c['rating'] ?? null,
                'imagen' => $c['imagen_destacada'] ?? '',
                'horarios' => $c['horarios'] ?? []
            ];
        }
    }
    
    echo json_encode([
        'resposta' => $parsed['resposta'] ?? '',
        'comercios' => $matched,
        'total' => count($matched)
    ], JSON_UNESCAPED_UNICODE);
    
    ai_log("SEARCH OK: " . count($matched) . " results");
}

// ── Chat ────────────────────────────────────────────────────────────────────
function handle_chat() {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode(['error' => 'Method POST required']);
        return;
    }
    
    $body = json_decode(file_get_contents('php://input'), true);
    $messages = $body['messages'] ?? [];
    $lang = $body['lang'] ?? 'gl';
    
    if (empty($messages)) {
        echo json_encode(['error' => 'Mensaxes vacías']);
        return;
    }
    
    ai_log("CHAT: " . count($messages) . " messages [lang=$lang]");
    
    $comercios = load_comercios();
    $directory = build_directory_context($comercios);
    $system = get_chat_system_prompt($lang, $directory);
    
    // Limit history to last 10 messages
    if (count($messages) > 10) {
        $messages = array_slice($messages, -10);
    }
    
    $result = call_gemini($system, $messages);
    
    if (!$result) {
        $fallback = $lang === 'gl' 
            ? 'Desculpa, tiven un problema ao procesar a túa mensaxe. Podes intentalo de novo?'
            : 'Disculpa, tuve un problema al procesar tu mensaje. ¿Puedes intentarlo de nuevo?';
        echo json_encode(['resposta' => $fallback, 'comercios' => []]);
        return;
    }
    
    // Parse JSON response
    $parsed = parse_ai_response($result);
    
    // Map IDs
    $ids = $parsed['ids'] ?? [];
    $matched = [];
    $comerciosById = [];
    foreach ($comercios as $c) $comerciosById[$c['id']] = $c;
    
    foreach ($ids as $id) {
        if (isset($comerciosById[$id])) {
            $c = $comerciosById[$id];
            $matched[] = [
                'id' => $c['id'],
                'nombre' => $c['nombre'][$lang] ?? $c['nombre']['es'] ?? $c['nombre']['gl'] ?? '',
                'slug' => $c['slug'],
                'categorias' => $c['categorias'] ?? [],
                'direccion' => $c['direccion'] ?? '',
                'telefono' => $c['telefono'] ?? '',
                'imagen' => $c['imagen_destacada'] ?? ''
            ];
        }
    }
    
    echo json_encode([
        'resposta' => $parsed['resposta'] ?? '',
        'comercios' => $matched
    ], JSON_UNESCAPED_UNICODE);
    
    ai_log("CHAT OK: " . count($matched) . " comercios mencionados");
}

// ── Suggest (sin IA, búsqueda rápida de texto) ─────────────────────────────
function handle_suggest() {
    $q = mb_strtolower(trim($_GET['q'] ?? ''));
    $lang = $_GET['lang'] ?? 'gl';
    
    if (mb_strlen($q) < 2) {
        echo json_encode(['suggestions' => []]);
        return;
    }
    
    $comercios = load_comercios();
    $suggestions = [];
    $seen = [];
    
    // Category name mapping
    $catNames = [
        'moda' => ['gl' => 'Moda e complementos', 'es' => 'Moda y complementos'],
        'resturantes' => ['gl' => 'Restaurantes', 'es' => 'Restaurantes'],
        'bares' => ['gl' => 'Bares', 'es' => 'Bares'],
        'cafeterias' => ['gl' => 'Cafeterías', 'es' => 'Cafeterías'],
        'peluquerias' => ['gl' => 'Peiteados', 'es' => 'Peluquerías'],
        'farmacias' => ['gl' => 'Farmacias', 'es' => 'Farmacias'],
        'calzado' => ['gl' => 'Calzado', 'es' => 'Calzado'],
        'joyerias' => ['gl' => 'Xoierías', 'es' => 'Joyerías'],
        'opticas' => ['gl' => 'Ópticas', 'es' => 'Ópticas'],
        'floristerias' => ['gl' => 'Florerías', 'es' => 'Floristerías'],
        'alimentacion' => ['gl' => 'Alimentación', 'es' => 'Alimentación'],
        'librerias' => ['gl' => 'Librarías', 'es' => 'Librerías'],
        'papelerias' => ['gl' => 'Papelerías', 'es' => 'Papelerías'],
        'clinica-dental' => ['gl' => 'Clínicas dentais', 'es' => 'Clínicas dentales'],
        'hosteleria' => ['gl' => 'Hostelería', 'es' => 'Hostelería'],
        'deporte' => ['gl' => 'Deporte', 'es' => 'Deporte'],
        'perfumeria' => ['gl' => 'Perfumería', 'es' => 'Perfumería'],
        'merceria' => ['gl' => 'Mercería', 'es' => 'Mercería'],
        'electrodomesticos' => ['gl' => 'Electrodomésticos', 'es' => 'Electrodomésticos'],
        'musica' => ['gl' => 'Música', 'es' => 'Música'],
        'seguros' => ['gl' => 'Seguros', 'es' => 'Seguros'],
        'artesania' => ['gl' => 'Artesanía', 'es' => 'Artesanía'],
        'fisioterapia' => ['gl' => 'Fisioterapia', 'es' => 'Fisioterapia'],
        'formacion' => ['gl' => 'Formación', 'es' => 'Formación'],
        'ortopedia' => ['gl' => 'Ortopedia', 'es' => 'Ortopedia'],
        'lenceria' => ['gl' => 'Lencería', 'es' => 'Lencería'],
        'confiterias' => ['gl' => 'Confiterías', 'es' => 'Confiterías'],
        'regalos-y-decoracion' => ['gl' => 'Agasallos e decoración', 'es' => 'Regalos y decoración'],
        'iluminacion' => ['gl' => 'Iluminación', 'es' => 'Iluminación'],
        'mueblerias' => ['gl' => 'Mobiliario', 'es' => 'Mueblerías'],
        'imprentas' => ['gl' => 'Imprentas', 'es' => 'Imprentas'],
        'textil' => ['gl' => 'Téxtil', 'es' => 'Textil'],
        'agencia-de-viajes' => ['gl' => 'Axencia de viaxes', 'es' => 'Agencia de viajes'],
        'hospedaje' => ['gl' => 'Hospedaxe', 'es' => 'Hospedaje'],
        'tatuajes' => ['gl' => 'Tatuaxes', 'es' => 'Tatuajes'],
        'psicologo' => ['gl' => 'Psicoloxía', 'es' => 'Psicología'],
        'estilismo' => ['gl' => 'Estilismo', 'es' => 'Estilismo'],
        'copisteria' => ['gl' => 'Copistería', 'es' => 'Copistería'],
    ];
    
    // Match categories
    foreach ($catNames as $slug => $names) {
        $name = $names[$lang] ?? $names['es'];
        if (mb_strpos(mb_strtolower($name), $q) !== false) {
            $key = mb_strtolower($name);
            if (!isset($seen[$key])) {
                $suggestions[] = ['type' => 'category', 'text' => $name, 'slug' => $slug];
                $seen[$key] = true;
            }
        }
    }
    
    // Match comercio names
    foreach ($comercios as $c) {
        $nombre = $c['nombre'][$lang] ?? $c['nombre']['es'] ?? '';
        if ($nombre && mb_strpos(mb_strtolower($nombre), $q) !== false) {
            $key = mb_strtolower($nombre);
            if (!isset($seen[$key]) && count($suggestions) < 8) {
                $suggestions[] = ['type' => 'comercio', 'text' => $nombre, 'slug' => $c['slug']];
                $seen[$key] = true;
            }
        }
    }
    
    // Limit to 8 suggestions
    $suggestions = array_slice($suggestions, 0, 8);
    
    echo json_encode(['suggestions' => $suggestions], JSON_UNESCAPED_UNICODE);
}
