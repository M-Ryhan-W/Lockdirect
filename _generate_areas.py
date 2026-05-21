#!/usr/bin/env python3
"""Generate LockDirect area landing pages from a shared template.

Each page is a self-contained HTML file with real street names, an
OpenStreetMap embed centred on the area, and localised copy.
Re-run after editing AREAS or TEMPLATE to regenerate.
"""

from pathlib import Path
from string import Template

ROOT = Path(__file__).parent
AREAS_DIR = ROOT / "areas"
AREAS_DIR.mkdir(exist_ok=True)

AREAS = [
    {"slug": "manchester", "name": "Manchester", "name_short": "Manchester",
     "postcodes": "M1–M9, M14, M20", "postcode_list": ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M14","M20"],
     "lat": 53.4808, "lng": -2.2426, "eta": 18,
     "streets": ["Deansgate","King Street","Oldham Street","Tib Street","Stevenson Square","Portland Street","Cross Street","Mosley Street"],
     "lede": "City centre and inner suburbs covered round the clock — Deansgate to Ancoats, Castlefield to the Northern Quarter.",
     "intel": "Manchester city centre is our busiest patch. Most common callouts are flat lockouts in M1/M2 apartment blocks (often UPVC mechanism failure) and car lockouts around Spinningfields and the Northern Quarter. Friday and Saturday nights are by far the busiest, with most M1 callouts between 11pm and 3am."},

    {"slug": "salford", "name": "Salford", "name_short": "Salford",
     "postcodes": "M3, M5, M6, M7, M27, M30", "postcode_list": ["M3","M5","M6","M7","M27","M28","M30"],
     "lat": 53.4875, "lng": -2.2902, "eta": 22,
     "streets": ["Chapel Street","The Crescent","Liverpool Road","Trinity Way","Adelphi Street","Frederick Road","Cross Lane","Hope Street"],
     "lede": "From Salford Quays to Pendleton, Eccles to Worsley — our engineers know every cut-through.",
     "intel": "Salford spans a huge area — Quays in the south to Pendleton, Eccles and Worsley further out. Quays callouts are mostly modern apartment buildings with electronic access (where the issue is usually a flat fob, not the door itself). Inner Salford runs more traditional UPVC and timber door work."},

    {"slug": "stockport", "name": "Stockport", "name_short": "Stockport",
     "postcodes": "SK1–SK8, SK12, SK14, SK16", "postcode_list": ["SK1","SK2","SK3","SK4","SK5","SK6","SK7","SK8","SK12","SK14","SK16"],
     "lat": 53.4106, "lng": -2.1575, "eta": 22,
     "streets": ["Wellington Road","Princes Street","Petersgate","Underbank","Middle Hillgate","Higher Hillgate","St Petersgate","Greek Street"],
     "lede": "From Edgeley to Bramhall, Heaton Moor to Cheadle Hulme — three engineers live in SK.",
     "intel": "Stockport is heavy on UPVC door failures — particularly on the 1990s-2000s housing stock around Heaton Moor, Heaton Mersey and Edgeley. Our SK-resident engineers carry universal multipoint replacements that fit most of the doors fitted in that era."},

    {"slug": "oldham", "name": "Oldham", "name_short": "Oldham",
     "postcodes": "OL1–OL9", "postcode_list": ["OL1","OL2","OL3","OL4","OL5","OL6","OL7","OL8","OL9"],
     "lat": 53.5408, "lng": -2.1114, "eta": 26,
     "streets": ["Yorkshire Street","High Street","Manchester Street","Union Street","Mumps","Henshaw Street","King Street","George Street"],
     "lede": "Yorkshire Street to Royton, Lees to Chadderton — the whole borough covered, day and night.",
     "intel": "Oldham housing leans more terraced and inter-war than the south Manchester suburbs — more mortice locks and traditional cylinders alongside the usual UPVC. Town-centre callouts cluster around Yorkshire Street and the bus station; residential callouts spread across Werneth, Royton, Chadderton and Lees."},

    {"slug": "rochdale", "name": "Rochdale", "name_short": "Rochdale",
     "postcodes": "OL11, OL12, OL15, OL16", "postcode_list": ["OL11","OL12","OL15","OL16"],
     "lat": 53.6097, "lng": -2.1561, "eta": 32,
     "streets": ["Yorkshire Street","Drake Street","Spotland Road","Manchester Road","Edenfield Road","Whitworth Road","Bury Road","Halifax Road"],
     "lede": "Town centre to Littleborough, Whitworth to Heywood — Rochdale-wide cover, 24/7.",
     "intel": "Rochdale is geographically large with a mix of urban centre and outlying villages (Wardle, Littleborough, Milnrow). Response times in the centre are quick; outlying postcodes can take a little longer at peak times. Common jobs run heavy on stone-built terraced housing with traditional cylinder locks."},

    {"slug": "bury", "name": "Bury", "name_short": "Bury",
     "postcodes": "BL8, BL9, M25, M26, M45", "postcode_list": ["BL8","BL9","M25","M26","M45"],
     "lat": 53.5933, "lng": -2.2978, "eta": 26,
     "streets": ["The Rock","Bolton Street","Manchester Road","Bell Lane","Walmersley Road","Knowsley Street","Market Street","Crostons Road"],
     "lede": "From the Market to Prestwich, Whitefield to Ramsbottom — Bury and the Irwell valley covered.",
     "intel": "Bury combines a busy market town centre with sprawling residential areas across Whitefield, Prestwich, Radcliffe and Ramsbottom. Our engineers see a lot of UPVC repair in the newer estates around Limefield and Holcombe Brook, and a mix of traditional locks in older Prestwich and Sedgley Park properties."},

    {"slug": "bolton", "name": "Bolton", "name_short": "Bolton",
     "postcodes": "BL1–BL7", "postcode_list": ["BL1","BL2","BL3","BL4","BL5","BL6","BL7"],
     "lat": 53.5786, "lng": -2.4282, "eta": 34,
     "streets": ["Bradshawgate","Deansgate","Knowsley Street","Newport Street","Crook Street","Bradford Street","Chorley Old Road","Manchester Road"],
     "lede": "Town centre to Horwich, Westhoughton to Bromley Cross — Bolton-wide network on call.",
     "intel": "Bolton's geography stretches from a dense town centre out to commuter villages on the West Pennine Moors. Our engineers respond fastest to town-centre postcodes (BL1, BL2, BL3); BL6 and BL7 can take a little longer at peak times."},

    {"slug": "wigan", "name": "Wigan", "name_short": "Wigan",
     "postcodes": "WN1–WN6", "postcode_list": ["WN1","WN2","WN3","WN4","WN5","WN6"],
     "lat": 53.5450, "lng": -2.6326, "eta": 38,
     "streets": ["Standishgate","Wallgate","Market Street","Mesnes Street","King Street","Library Street","Hallgate","Dorning Street"],
     "lede": "From the Pier to Ashton-in-Makerfield, Standish to Hindley — Wigan borough covered round the clock.",
     "intel": "Wigan is our furthest-west patch and has its own dedicated dispatch. Town centre and direct surrounding wards (Standish, Pemberton, Worsley Mesnes) see fastest response; outer postcodes (WN5, WN6) can take longer. Common jobs trend toward UPVC mechanism failure on early-2000s housing stock."},

    {"slug": "altrincham", "name": "Altrincham", "name_short": "Altrincham",
     "postcodes": "WA14, WA15", "postcode_list": ["WA14","WA15"],
     "lat": 53.3838, "lng": -2.3550, "eta": 24,
     "streets": ["Stamford New Road","George Street","Greenwood Street","Railway Street","Goose Green","The Downs","Oxford Road","Ashley Road"],
     "lede": "Market Hall to Bowdon, Hale to Timperley — the Trafford-Cheshire fringe served day and night.",
     "intel": "Altrincham and Hale lean toward higher-spec residential — period properties around The Downs and Bowdon, plus modern flats around the redeveloped Stamford Quarter. Lots of British Standard cylinder work and end-of-tenancy lock changes for the rental stock."},

    {"slug": "sale", "name": "Sale", "name_short": "Sale",
     "postcodes": "M33", "postcode_list": ["M33"],
     "lat": 53.4239, "lng": -2.3219, "eta": 22,
     "streets": ["School Road","Cross Street","Northenden Road","Marsland Road","Tatton Road","Springfield Road","Washway Road","Brooklands Road"],
     "lede": "From the Metrolink to Brooklands, Ashton on Mersey to Sale Moor — every M33 postcode covered.",
     "intel": "Sale is a mid-sized commuter town with mostly semi-detached and terraced housing built between 1900 and 1960. Cylinder change is the most common scheduled job (lots of new homeowners) and UPVC repair the most common emergency."},

    {"slug": "didsbury", "name": "Didsbury", "name_short": "Didsbury",
     "postcodes": "M19, M20, M21", "postcode_list": ["M19","M20","M21"],
     "lat": 53.4163, "lng": -2.2300, "eta": 18,
     "streets": ["Wilmslow Road","Barlow Moor Road","Burton Road","School Lane","Lapwing Lane","Palatine Road","Parrs Wood Road","Fog Lane"],
     "lede": "Didsbury Village to West Didsbury, Burton Road to Parrs Wood — south Manchester's most-called area.",
     "intel": "Didsbury has a heavy student and young-professional flat population, which means a constant stream of weekend lockouts. The conversions of large Victorian houses into multiple flats also throws up unusual lock setups — we're used to most of them."},

    {"slug": "chorlton", "name": "Chorlton", "name_short": "Chorlton",
     "postcodes": "M16, M21", "postcode_list": ["M16","M21"],
     "lat": 53.4429, "lng": -2.2715, "eta": 20,
     "streets": ["Wilbraham Road","Beech Road","Manchester Road","Barlow Moor Road","Albany Road","High Lane","Keppel Road","Sandy Lane"],
     "lede": "Beech Road to Chorlton Park, Whalley Range to Stretford fringe — M21 and beyond.",
     "intel": "Chorlton's Edwardian and Victorian terraces dominate — wide variety of original mortice locks, modern night latches and UPVC retrofits. Steady stream of break-in repairs in M21 and Whalley Range, plus a lot of HMO end-of-tenancy lock changes."},

    {"slug": "withington", "name": "Withington", "name_short": "Withington",
     "postcodes": "M14, M19, M20", "postcode_list": ["M14","M19","M20"],
     "lat": 53.4364, "lng": -2.2350, "eta": 20,
     "streets": ["Wilmslow Road","Burton Road","Old Moat Lane","Copson Street","Davenport Avenue","Whitchurch Road","Mauldeth Road","Princess Road"],
     "lede": "Wilmslow Road corridor, Burton Road shops, all the way down to Mauldeth — Withington covered fast.",
     "intel": "Withington is dominated by student flats and shared houses, so weekend lockouts are by far the most common job. We're used to dealing with letting-agent-managed properties and absent landlords — call us and we'll handle the comms with whoever needs to authorise."},

    {"slug": "prestwich", "name": "Prestwich", "name_short": "Prestwich",
     "postcodes": "M25, M45", "postcode_list": ["M25","M45"],
     "lat": 53.5375, "lng": -2.2849, "eta": 24,
     "streets": ["Bury New Road","Heys Road","Fairfax Road","Heaton Park Road","Bishops Road","Park Lane","Sedgley Park Road","Scholes Lane"],
     "lede": "From the Village to Heaton Park, Sedgley Park to Whitefield border — Prestwich M25 round the clock.",
     "intel": "Prestwich's mix of solid 1930s semi-detached and newer Sedgley Park stock means a balance of British Standard cylinder upgrades and UPVC mechanism repair. The Village has a higher concentration of flat lockouts on weekend evenings."},

    {"slug": "eccles", "name": "Eccles", "name_short": "Eccles",
     "postcodes": "M30, M44", "postcode_list": ["M30","M44"],
     "lat": 53.4842, "lng": -2.3403, "eta": 24,
     "streets": ["Church Street","Liverpool Road","Bridgewater Street","Half Edge Lane","Monton Road","Wellington Road","Barton Lane","Park Road"],
     "lede": "Eccles Cross to Monton, Patricroft to Winton — M30 covered by the closest engineer.",
     "intel": "Eccles has a mix of older terraced housing and post-war stock, plus a chunk of new-build around the regenerated centre. Most calls are residential lockouts and lock change-ups after house moves."},

    {"slug": "cheadle", "name": "Cheadle", "name_short": "Cheadle",
     "postcodes": "SK7, SK8", "postcode_list": ["SK7","SK8"],
     "lat": 53.4015, "lng": -2.2200, "eta": 20,
     "streets": ["High Street","Stockport Road","Wilmslow Road","Manchester Road","Schools Hill","Ashfield Road","Brown Lane","Mill Lane"],
     "lede": "Cheadle Village to Cheadle Hulme, Heald Green to Gatley — SK8 closely covered.",
     "intel": "Cheadle and Cheadle Hulme run a higher concentration of larger detached and semi-detached homes than further north. Lots of high-spec lock work — anti-snap British Standard upgrades, multipoint mechanism replacement, alarm/CCTV-linked entry."},

    {"slug": "ashton", "name": "Ashton-under-Lyne", "name_short": "Ashton",
     "postcodes": "OL6, OL7", "postcode_list": ["OL6","OL7"],
     "lat": 53.4901, "lng": -2.0978, "eta": 28,
     "streets": ["Old Street","Stamford Street","Henry Square","Market Avenue","Penny Meadow","Wellington Road","Crickets Lane","Albion Way"],
     "lede": "Stamford Street to Ashton Moss, Hurst to Hartshead — OL6 and OL7 covered day and night.",
     "intel": "Ashton-under-Lyne is the heart of Tameside and our engineers see a balanced mix of residential lockouts, UPVC repair, and commercial work around the town centre. Market Avenue and the IKEA retail area generate a steady stream of car lockouts."},

    {"slug": "hyde", "name": "Hyde", "name_short": "Hyde",
     "postcodes": "SK13, SK14", "postcode_list": ["SK13","SK14"],
     "lat": 53.4505, "lng": -2.0820, "eta": 28,
     "streets": ["Market Street","Clarendon Square","Lumn Road","Throstle Bank Street","Mottram Road","Talbot Road","Greenfield Street","Manchester Road"],
     "lede": "Town centre to Gee Cross, Newton to Werneth Low — SK14 by the nearest engineer.",
     "intel": "Hyde sits at the edge of our coverage but we have a regular Tameside-based engineer who lives locally. Mix of housing types — Victorian terrace on the Stockport Road and post-war semi out toward Gee Cross."},
]

def streets_html(streets):
    return "\n".join(
        f'        <div class="street"><span class="street__dot"></span>{s}</div>'
        for s in streets
    )

def postcodes_html(codes):
    return "\n".join(f'            <span class="postcode-pill">{c}</span>' for c in codes)

def bbox(lat, lng):
    d_lat = 0.020
    d_lng = 0.032
    return f"{lng - d_lng}%2C{lat - d_lat}%2C{lng + d_lng}%2C{lat + d_lat}"


TEMPLATE_STR = r'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#E11D2A">
<title>Locksmith $name — 24/7 Emergency · From £79 | LockDirect</title>
<meta name="description" content="Locked out in $name? LockDirect dispatches DBS-checked locksmiths across $postcodes. $eta-min average response. No call-out fee. Call 07760 587095.">
<meta property="og:title" content="Locksmith $name — 24/7 | LockDirect">
<meta property="og:description" content="$name locksmith dispatch. $eta-min average response. Call 07760 587095.">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "LockDirect $name",
  "telephone": "+447760587095",
  "priceRange": "££",
  "address": {"@type": "PostalAddress","addressLocality": "$name","addressRegion": "Greater Manchester","addressCountry": "GB"},
  "geo": {"@type":"GeoCoordinates","latitude":$lat,"longitude":$lng},
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification","dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens": "00:00","closes": "23:59"}]
}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root {
  --red: #E11D2A; --red-bright: #FF2A3A; --red-glow: rgba(225,29,42,0.14); --red-soft: #FEF2F3;
  --green: #16A34A; --green-bright: #22C55E; --whatsapp: #25D366; --whatsapp-dark: #1FB55C;
  --ink: #0A0E1A; --ink-soft: #1E2433; --text: #475569; --text-soft: #64748B; --text-muted: #94A3B8;
  --bg: #FFFFFF; --bg-soft: #F8FAFC; --bg-mid: #F1F5F9; --border: #E2E8F0; --border-strong: #CBD5E1;
  --container: 1240px;
  --r-md: 16px; --r-lg: 22px; --r-xl: 30px; --r-2xl: 40px; --r-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(15,23,42,0.05);
  --shadow-md: 0 4px 14px rgba(15,23,42,0.07);
  --shadow-lg: 0 14px 36px rgba(15,23,42,0.09);
  --shadow-red: 0 12px 34px rgba(225,29,42,0.38);
  --shadow-green: 0 12px 34px rgba(37,211,102,0.35);
  --font-display: 'Bricolage Grotesque', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { font-family: var(--font-body); color: var(--ink); background: var(--bg); line-height: 1.55; -webkit-font-smoothing: antialiased; overflow-x: hidden; }
@media (max-width: 1023px) { body { padding-bottom: 84px; } }
a { color: inherit; text-decoration: none; }
button { font: inherit; cursor: pointer; border: 0; background: none; }
svg { display: block; }

.container { max-width: var(--container); margin: 0 auto; padding: 0 24px; }
@media (min-width: 768px) { .container { padding: 0 32px; } }

.nav { position: sticky; top: 0; z-index: 50; background: rgba(255,255,255,0.92); backdrop-filter: saturate(180%) blur(14px); -webkit-backdrop-filter: saturate(180%) blur(14px); border-bottom: 1px solid rgba(226,232,240,0.7); }
.nav__inner { max-width: var(--container); margin: 0 auto; padding: 14px 24px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
@media (min-width: 768px) { .nav__inner { padding: 18px 32px; } }
.brand { display: flex; align-items: center; gap: 12px; }
.brand__logo { height: 44px; width: auto; display: block; }

.brand__text { display: flex; flex-direction: column; line-height: 1.05; }
.brand__name { font-family: var(--font-display); font-weight: 800; font-size: 22px; letter-spacing: -0.02em; }
.brand__sub { font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-muted); font-weight: 600; margin-top: 2px; }

.btn { display: inline-flex; align-items: center; justify-content: center; gap: 10px; padding: 14px 24px; border-radius: var(--r-full); font-weight: 700; font-size: 15px; letter-spacing: -0.01em; white-space: nowrap; transition: transform 0.2s var(--ease-out), box-shadow 0.2s var(--ease-out); }
.btn svg { width: 18px; height: 18px; }
.btn--primary { background: linear-gradient(135deg, var(--red), var(--red-bright)); color: white; box-shadow: var(--shadow-red); }
.btn--primary:hover { transform: translateY(-1px); }
.btn--whatsapp { background: linear-gradient(135deg, var(--whatsapp-dark), var(--whatsapp)); color: white; box-shadow: var(--shadow-green); }
.btn--ghost { background: var(--bg-mid); color: var(--ink); }
.btn--large { padding: 18px 32px; font-size: 17px; }
.btn--xl { padding: 22px 40px; font-size: 19px; }

.breadcrumb { padding: 14px 0 0; }
.breadcrumb__inner { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-soft); flex-wrap: wrap; }
.breadcrumb a { color: var(--text-soft); }
.breadcrumb a:hover { color: var(--ink); }
.breadcrumb__sep { color: var(--border-strong); }
.breadcrumb__current { color: var(--ink); font-weight: 600; }

.area-hero { padding: 32px 0 56px; position: relative; overflow: hidden; }
@media (min-width: 768px) { .area-hero { padding: 48px 0 72px; } }
.area-hero__bg { position: absolute; inset: 0; z-index: -1; background: radial-gradient(ellipse 60% 50% at 50% 0%, var(--red-glow), transparent 60%); }
.area-hero__grid { display: grid; grid-template-columns: 1fr; gap: 36px; align-items: center; }
@media (min-width: 1024px) { .area-hero__grid { grid-template-columns: 1.05fr 1fr; gap: 64px; } }

.live-status { display: inline-flex; align-items: center; gap: 10px; padding: 7px 16px 7px 12px; background: white; border: 1px solid var(--border); border-radius: var(--r-full); font-size: 13px; font-weight: 600; color: var(--ink-soft); margin-bottom: 22px; box-shadow: var(--shadow-sm); }
.live-dot { width: 9px; height: 9px; border-radius: 50%; background: var(--green-bright); position: relative; }
.live-dot::after { content: ''; position: absolute; inset: -4px; border-radius: 50%; background: var(--green-bright); opacity: 0.4; animation: live-pulse 2.4s var(--ease-out) infinite; }
@keyframes live-pulse { 0% { transform: scale(0.7); opacity: 0.5; } 100% { transform: scale(2.4); opacity: 0; } }
.live-status .sep { color: var(--border-strong); margin: 0 4px; }
.live-status .accent { color: var(--green); }

.area-hero h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(40px, 7vw, 80px); line-height: 0.98; letter-spacing: -0.035em; margin-bottom: 22px; font-variation-settings: "opsz" 96; }
.area-hero h1 .accent { color: var(--red); }
.area-hero__sub { font-size: clamp(16px, 2.2vw, 19px); color: var(--text); max-width: 560px; margin-bottom: 32px; }

.area-hero__ctas { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; }
@media (max-width: 480px) { .area-hero__ctas .btn { flex: 1; min-width: 0; } }

.area-hero__trust { display: flex; flex-wrap: wrap; gap: 14px 22px; }
.trust-item { display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: var(--ink-soft); }
.trust-item svg { width: 16px; height: 16px; color: var(--green); }

/* Stats card */
.stats-card { background: var(--ink); color: white; border-radius: var(--r-2xl); padding: 32px 28px; position: relative; overflow: hidden; box-shadow: var(--shadow-lg); }
.stats-card::before { content: ''; position: absolute; top: -40%; right: -20%; width: 460px; height: 460px; background: radial-gradient(circle, rgba(225,29,42,0.2), transparent 60%); }
.stats-card__inner { position: relative; }
.stats-card__head { font-size: 12px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 6px; }
.stats-card__title { font-family: var(--font-display); font-weight: 700; font-size: 22px; letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 24px; }
.stats-card__grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-bottom: 20px; }
.stat { padding: 16px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--r-md); }
.stat__num { font-family: var(--font-display); font-weight: 700; font-size: 26px; letter-spacing: -0.025em; color: white; line-height: 1; }
.stat__num small { font-size: 14px; color: rgba(255,255,255,0.5); }
.stat__label { font-size: 11px; color: rgba(255,255,255,0.55); margin-top: 4px; letter-spacing: 0.04em; font-weight: 600; text-transform: uppercase; }
.postcodes { display: flex; flex-wrap: wrap; gap: 6px; padding-top: 22px; border-top: 1px dashed rgba(255,255,255,0.12); }
.postcode-pill { padding: 5px 11px; background: rgba(255,255,255,0.08); border-radius: var(--r-full); font-size: 12px; font-weight: 700; color: white; }

/* Map section */
.map-section { padding: 48px 0 64px; }
.map-wrap { position: relative; border-radius: var(--r-2xl); overflow: hidden; border: 2px solid var(--red); box-shadow: var(--shadow-lg); background: var(--bg-mid); }
.map-wrap iframe { display: block; width: 100%; height: 360px; border: 0; }
@media (min-width: 768px) { .map-wrap iframe { height: 460px; } }
.map-wrap__caption { position: absolute; bottom: 20px; left: 20px; display: flex; align-items: center; gap: 10px; padding: 10px 14px 10px 12px; background: rgba(10,14,26,0.92); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); color: white; border-radius: var(--r-full); font-weight: 600; font-size: 13px; box-shadow: var(--shadow-md); }
.map-wrap__caption .live-dot { background: var(--green-bright); }
.map-wrap__caption .accent { color: var(--green-bright); font-weight: 700; }
.map-wrap__credit { position: absolute; top: 14px; right: 14px; padding: 6px 12px; background: rgba(255,255,255,0.94); border-radius: var(--r-full); font-size: 11px; font-weight: 700; letter-spacing: 0.06em; color: var(--ink); }

.section { padding: 56px 0; }
@media (min-width: 768px) { .section { padding: 88px 0; } }
.section--soft { background: var(--bg-soft); }
.kicker { display: inline-block; font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--red); margin-bottom: 14px; }
.h2 { font-family: var(--font-display); font-weight: 800; font-size: clamp(28px, 4vw, 44px); line-height: 1.05; letter-spacing: -0.03em; color: var(--ink); font-variation-settings: "opsz" 64; }
.section__head { max-width: 720px; margin-bottom: 36px; }
.section__head p { margin-top: 14px; font-size: clamp(15px, 1.8vw, 18px); color: var(--text); }

/* Streets */
.streets-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; max-width: 760px; }
@media (min-width: 768px) { .streets-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; } }
.street { display: flex; align-items: center; gap: 10px; padding: 14px 18px; background: white; border: 1.5px solid var(--border); border-radius: var(--r-md); font-weight: 600; font-size: 15px; color: var(--ink); }
.street__dot { width: 8px; height: 8px; border-radius: 50%; background: var(--red); flex-shrink: 0; }
.streets-note { margin-top: 18px; font-size: 14px; color: var(--text-soft); max-width: 600px; }

/* Services compact */
.services-mini { display: grid; grid-template-columns: 1fr; gap: 14px; }
@media (min-width: 640px) { .services-mini { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .services-mini { grid-template-columns: repeat(3, 1fr); } }
.svc-mini { padding: 24px; background: white; border: 1.5px solid var(--border); border-radius: var(--r-xl); display: flex; flex-direction: column; gap: 12px; transition: all 0.3s var(--ease-out); }
.svc-mini:hover { border-color: var(--red); transform: translateY(-2px); }
.svc-mini__icon { width: 42px; height: 42px; border-radius: 11px; background: var(--red-soft); color: var(--red); display: grid; place-items: center; }
.svc-mini__icon svg { width: 22px; height: 22px; }
.svc-mini__title { font-family: var(--font-display); font-weight: 700; font-size: 19px; letter-spacing: -0.02em; line-height: 1.15; }
.svc-mini__text { font-size: 14px; color: var(--text); line-height: 1.5; }

/* Pricing band */
.pricing { background: var(--ink); color: white; padding: 28px 0; position: relative; overflow: hidden; }
.pricing__inner { display: grid; grid-template-columns: 1fr; gap: 22px; align-items: center; }
@media (min-width: 900px) { .pricing__inner { grid-template-columns: auto 1fr; gap: 48px; } }
.pricing__head { font-family: var(--font-display); font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.pricing__head .accent { color: var(--red-bright); }
.pricing__grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px 24px; }
@media (min-width: 768px) { .pricing__grid { grid-template-columns: repeat(4, auto); justify-content: end; } }
.pricing__item-label { font-size: 12px; color: rgba(255,255,255,0.55); letter-spacing: 0.04em; display: block; }
.pricing__item-price { font-family: var(--font-display); font-weight: 700; font-size: 22px; letter-spacing: -0.02em; color: white; }
.pricing__item-price .from { font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.6); margin-right: 2px; }

/* Mid CTA */
.mid-cta { background: var(--ink); color: white; padding: 48px 0; position: relative; overflow: hidden; }
.mid-cta::before { content: ''; position: absolute; top: -50%; left: 20%; width: 600px; height: 600px; background: radial-gradient(circle, var(--red-glow), transparent 60%); }
.mid-cta__inner { position: relative; display: grid; grid-template-columns: 1fr; gap: 24px; align-items: center; text-align: center; }
@media (min-width: 768px) { .mid-cta__inner { grid-template-columns: 1fr auto; text-align: left; gap: 32px; } }
.mid-cta h3 { font-family: var(--font-display); font-weight: 700; font-size: clamp(24px, 3vw, 32px); letter-spacing: -0.025em; line-height: 1.1; }
.mid-cta h3 .accent { color: var(--red-bright); }
.mid-cta__ctas { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

/* Prose */
.prose { max-width: 720px; }
.prose h3 { font-family: var(--font-display); font-weight: 700; font-size: 22px; letter-spacing: -0.02em; margin: 28px 0 12px; }
.prose p { font-size: 15.5px; color: var(--text); line-height: 1.7; margin-bottom: 14px; }
.prose strong { color: var(--ink); font-weight: 700; }

/* Final CTA */
.final-cta { position: relative; padding: 72px 0; background: var(--ink); color: white; overflow: hidden; text-align: center; }
.final-cta::before { content: ''; position: absolute; top: -30%; left: 50%; transform: translateX(-50%); width: 1000px; height: 700px; background: radial-gradient(ellipse, var(--red-glow), transparent 60%); }
.final-cta__inner { position: relative; max-width: 720px; margin: 0 auto; padding: 0 24px; }
.final-cta h2 { font-family: var(--font-display); font-weight: 800; font-size: clamp(32px, 6vw, 60px); line-height: 1.0; letter-spacing: -0.035em; margin: 16px 0 22px; }
.final-cta h2 .accent { color: var(--red-bright); }
.final-cta__phone { font-family: var(--font-display); font-weight: 800; font-size: clamp(34px, 7vw, 64px); letter-spacing: -0.04em; display: inline-block; margin: 18px 0 28px; color: white; }
.final-cta__buttons { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

.sticky-mobile { position: fixed; bottom: 0; left: 0; right: 0; z-index: 40; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 12px 14px calc(12px + env(safe-area-inset-bottom)); background: rgba(255,255,255,0.95); backdrop-filter: saturate(180%) blur(14px); -webkit-backdrop-filter: saturate(180%) blur(14px); border-top: 1px solid var(--border); }
@media (min-width: 1024px) { .sticky-mobile { display: none; } }
.sticky-mobile .btn { padding: 14px 12px; font-size: 15px; }

.footer-mini { background: var(--bg-soft); border-top: 1px solid var(--border); padding: 28px 0; text-align: center; font-size: 13px; color: var(--text-soft); }
.footer-mini a { color: var(--ink-soft); margin: 0 8px; }
.footer-mini a:hover { color: var(--red); }
.footer-mini__row + .footer-mini__row { margin-top: 8px; }
</style>
</head>

<body>

<header class="nav">
  <div class="nav__inner">
    <a href="../index.html" class="brand">
      <img src="../assets/lockdirect-logo.png" alt="LockDirect" class="brand__logo">
      <div class="brand__text">
        <span class="brand__sub">$name_short · 24/7</span>
      </div>
    </a>
    <a href="tel:07760587095" class="btn btn--primary">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
      Call Now
    </a>
  </div>
</header>

<nav class="breadcrumb container" aria-label="Breadcrumb">
  <div class="breadcrumb__inner">
    <a href="../index.html">Home</a>
    <span class="breadcrumb__sep">/</span>
    <a href="../index.html#areas">Areas</a>
    <span class="breadcrumb__sep">/</span>
    <span class="breadcrumb__current">$name</span>
  </div>
</nav>

<section class="area-hero">
  <div class="area-hero__bg"></div>
  <div class="container">
    <div class="area-hero__grid">
      <div>
        <div class="live-status">
          <span class="live-dot"></span>
          <span class="accent">Live in $name_short</span>
          <span class="sep">·</span>
          $eta min average response
        </div>

        <h1>Locksmith <span class="accent">$name.</span></h1>
        <p class="area-hero__sub">$lede</p>

        <div class="area-hero__ctas">
          <a href="tel:07760587095" class="btn btn--primary btn--large">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Call 07760 587095
          </a>
          <a href="https://wa.me/447760587095?text=Hi%20LockDirect%2C%20I%27m%20in%20$name_short" class="btn btn--whatsapp btn--large" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.95 7.95 0 0 0-6.9 11.93L4 20l4.15-1.09a7.94 7.94 0 0 0 3.9 1h.01a7.95 7.95 0 0 0 7.95-7.94 7.9 7.9 0 0 0-2.41-5.65z"/></svg>
            WhatsApp
          </a>
        </div>

        <div class="area-hero__trust">
          <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>DBS Checked</div>
          <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>24/7 in $name_short</div>
          <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>12 Mo Guarantee</div>
          <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>No call-out fee</div>
        </div>
      </div>

      <div class="stats-card">
        <div class="stats-card__inner">
          <div class="stats-card__head">$name_short Coverage</div>
          <div class="stats-card__title">Live network in your postcode</div>
          <div class="stats-card__grid">
            <div class="stat"><div class="stat__num">$eta<small>m</small></div><div class="stat__label">Avg response</div></div>
            <div class="stat"><div class="stat__num">3</div><div class="stat__label">Active engineers</div></div>
            <div class="stat"><div class="stat__num">£79<small>+</small></div><div class="stat__label">From, no fee</div></div>
            <div class="stat"><div class="stat__num">98<small>%</small></div><div class="stat__label">First-call fixed</div></div>
          </div>
          <div class="postcodes">
$postcodes_html
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Map -->
<section class="map-section">
  <div class="container">
    <div class="map-wrap">
      <div class="map-wrap__credit">$name_short Coverage</div>
      <iframe loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=$bbox&amp;layer=mapnik&amp;marker=$lat%2C$lng" title="Map of $name service area"></iframe>
      <div class="map-wrap__caption">
        <span class="live-dot"></span>
        <span class="accent">Live</span>
        ·
        Engineers active in $name_short
      </div>
    </div>
  </div>
</section>

<!-- Streets -->
<section class="section section--soft">
  <div class="container">
    <div class="section__head">
      <span class="kicker">Streets we cover</span>
      <h2 class="h2">Working across $name.</h2>
      <p>Just a handful of the streets our $name_short engineers were called to in the last month. Postcodes covered: $postcodes.</p>
    </div>
    <div class="streets-grid">
$streets_html
    </div>
    <p class="streets-note">…and every other street in $postcodes. If your postcode starts with the right prefix, we're nearby.</p>
  </div>
</section>

<!-- Mid CTA -->
<section class="mid-cta">
  <div class="container">
    <div class="mid-cta__inner">
      <h3>Locked out in $name <span class="accent">right now?</span></h3>
      <div class="mid-cta__ctas">
        <a href="tel:07760587095" class="btn btn--primary btn--large">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call 07760 587095
        </a>
        <a href="https://wa.me/447760587095" class="btn btn--whatsapp btn--large" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.95 7.95 0 0 0-6.9 11.93L4 20l4.15-1.09a7.94 7.94 0 0 0 3.9 1h.01a7.95 7.95 0 0 0 7.95-7.94 7.9 7.9 0 0 0-2.41-5.65z"/></svg>
          WhatsApp
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Services -->
<section class="section">
  <div class="container">
    <div class="section__head">
      <span class="kicker">Services in $name_short</span>
      <h2 class="h2">What we're called for most.</h2>
    </div>
    <div class="services-mini">
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-7h-6v7H4a1 1 0 0 1-1-1z"/></svg></div>
        <h3 class="svc-mini__title">House Lockouts</h3>
        <p class="svc-mini__text">Lost keys, broken lock, can't get in. Most $name_short lockouts opened without damage in under 10 minutes.</p>
      </article>
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 16H9m10 0h1a1 1 0 0 0 1-1v-3.34a3 3 0 0 0-.36-1.43l-1.16-2.16A4 4 0 0 0 15.96 6H8.04a4 4 0 0 0-3.52 2.07L3.36 10.23A3 3 0 0 0 3 11.66V15a1 1 0 0 0 1 1h1"/><circle cx="7" cy="16" r="2"/><circle cx="17" cy="16" r="2"/></svg></div>
        <h3 class="svc-mini__title">Car &amp; Van Unlocks</h3>
        <p class="svc-mini__text">Auto-specialist tools. All makes and models. Most opened in under 10 minutes on-site, no damage.</p>
      </article>
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 3v18"/></svg></div>
        <h3 class="svc-mini__title">UPVC Door Repair</h3>
        <p class="svc-mini__text">Dropped doors, seized gearboxes. Most $name_short mechanisms replaced same-day, door rarely needs to be.</p>
      </article>
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg></div>
        <h3 class="svc-mini__title">Lock Changes</h3>
        <p class="svc-mini__text">British Standard upgrades for moving in, or end-of-tenancy changeovers for landlords across $postcodes.</p>
      </article>
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
        <h3 class="svc-mini__title">Burglary Repair</h3>
        <p class="svc-mini__text">Board-up, full lock replacement and insurance-ready paperwork for break-ins anywhere in $name_short.</p>
      </article>
      <article class="svc-mini">
        <div class="svc-mini__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l8-4v18M19 21V11l-6-4"/></svg></div>
        <h3 class="svc-mini__title">Commercial</h3>
        <p class="svc-mini__text">Shops, offices, industrial units. Master suites, access control, end-of-lease changes.</p>
      </article>
    </div>
  </div>
</section>

<!-- Pricing -->
<section class="pricing">
  <div class="container">
    <div class="pricing__inner">
      <div class="pricing__head">Pricing in $name_short. <span class="accent">No surprises.</span></div>
      <div class="pricing__grid">
        <div><span class="pricing__item-label">House lockout</span><span class="pricing__item-price"><span class="from">from</span>£79</span></div>
        <div><span class="pricing__item-label">Car lockout</span><span class="pricing__item-price"><span class="from">from</span>£89</span></div>
        <div><span class="pricing__item-label">Lock change</span><span class="pricing__item-price"><span class="from">from</span>£99</span></div>
        <div><span class="pricing__item-label">UPVC fix</span><span class="pricing__item-price"><span class="from">from</span>£89</span></div>
      </div>
    </div>
  </div>
</section>

<!-- Local intel -->
<section class="section section--soft">
  <div class="container">
    <div class="prose">
      <span class="kicker">About our $name_short service</span>
      <h2 class="h2" style="margin-bottom:24px;">A locksmith network built around $name.</h2>
      <p>$intel</p>
      <h3>Pricing in $name_short</h3>
      <p>Pricing in $postcodes is the same as the rest of Greater Manchester. <strong>House lockouts from £79</strong>, <strong>car lockouts from £89</strong>, <strong>full lock changes from £99</strong>. No call-out fee. No premium for evenings within our standard 24/7 service.</p>
      <h3>If you're locked out right now</h3>
      <p>Check the obvious — second door, ground-floor window left on the latch, key still in from the inside. Don't try to force the door, especially UPVC — repairs cost five times what a clean lockout would. <strong>Call us on 07760 587095</strong> and we'll talk you through the options. Phone advice is free either way.</p>
    </div>
  </div>
</section>

<!-- Final CTA -->
<section class="final-cta">
  <div class="final-cta__inner">
    <div class="live-status" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.15);color:rgba(255,255,255,0.85);">
      <span class="live-dot"></span>
      <span class="accent">Live in $name_short</span>
      <span class="sep">·</span>
      Dispatching now
    </div>
    <h2>$name locksmith.<br><span class="accent">One call away.</span></h2>
    <a href="tel:07760587095" class="final-cta__phone">07760 587095</a>
    <div class="final-cta__buttons">
      <a href="tel:07760587095" class="btn btn--primary btn--xl">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        Call Now
      </a>
      <a href="https://wa.me/447760587095" class="btn btn--whatsapp btn--xl" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.95 7.95 0 0 0-6.9 11.93L4 20l4.15-1.09a7.94 7.94 0 0 0 3.9 1h.01a7.95 7.95 0 0 0 7.95-7.94 7.9 7.9 0 0 0-2.41-5.65z"/></svg>
        WhatsApp
      </a>
    </div>
  </div>
</section>

<footer class="footer-mini">
  <div class="container">
    <div class="footer-mini__row">
      <a href="../index.html">Home</a><a href="../index.html#services">Services</a><a href="../index.html#areas">All Areas</a><a href="../index.html#faq">FAQ</a><a href="../privacy.html">Privacy</a><a href="../terms.html">Terms</a>
    </div>
    <div class="footer-mini__row" style="margin-top:14px;">© 2026 LockDirect Dispatch Ltd. · Locksmith $name</div>
  </div>
</footer>

<div class="sticky-mobile">
  <a href="tel:07760587095" class="btn btn--primary">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    Call Now
  </a>
  <a href="https://wa.me/447760587095" class="btn btn--whatsapp" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.6 6.32A7.85 7.85 0 0 0 12.05 4a7.95 7.95 0 0 0-6.9 11.93L4 20l4.15-1.09a7.94 7.94 0 0 0 3.9 1h.01a7.95 7.95 0 0 0 7.95-7.94 7.9 7.9 0 0 0-2.41-5.65z"/></svg>
    WhatsApp
  </a>
</div>

</body>
</html>
'''

template = Template(TEMPLATE_STR)

for area in AREAS:
    rendered = template.substitute(
        slug=area["slug"],
        name=area["name"],
        name_short=area["name_short"],
        postcodes=area["postcodes"],
        postcodes_html=postcodes_html(area["postcode_list"]),
        lat=area["lat"],
        lng=area["lng"],
        bbox=bbox(area["lat"], area["lng"]),
        streets_html=streets_html(area["streets"]),
        eta=area["eta"],
        lede=area["lede"],
        intel=area["intel"],
    )
    out_path = AREAS_DIR / f"{area['slug']}.html"
    out_path.write_text(rendered, encoding="utf-8")
    print(f"✓ {out_path.relative_to(ROOT)}")

print(f"\nGenerated {len(AREAS)} area pages.")
