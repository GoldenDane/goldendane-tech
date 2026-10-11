"""Build da/index.html from index.html.

The Danish page shares the English page's markup, styles (assets/site.css) and
script (assets/site.js); only the words differ. Edit index.html, then run
`python3 tools/build_da.py`. Every English snippet below must appear in
index.html exactly as many times as stated, or the build stops and tells you
which text changed, so the two languages can't drift apart silently.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "index.html").read_text(encoding="utf-8")

FAQ = [
    ("Vi er ikke en AI-virksomhed. Er det her for os?",
     "Ja, det er netop dem, det er til. I behøver ikke data scientists eller nyt software. Hvis jeres team gentager de samme ordrer, mails, dokumenter eller procesopgaver hver uge, kan vi som regel sige i ét opkald på 30 minutter, om det kan betale sig at automatisere."),
    ("Hvad sker der i det gratis opkald på 30 minutter?",
     "I viser os én arbejdsgang, der tager tid fra jeres team. Vi stiller nogle spørgsmål om mængder, systemer og data og siger ærligt, om AI kan hjælpe, hvordan et pilotprojekt ville se ud, og hvad det ville kræve. Ingen slides og ingen forpligtelser."),
    ("Hvad koster et pilotprojekt?",
     "Et pilotprojekt har en fast pris, der aftales på forhånd, og er afgrænset til én arbejdsgang og to til tre ugers arbejde. Vi giver jer prisen efter det gratis opkald, når vi kender problemets størrelse, og I beslutter, om I vil gå videre."),
    ("Hvad sker der med vores data?",
     "Vi underskriver en databehandleraftale, før vi rører noget, holder behandlingen inden for EU, hvor det er muligt, sletter arbejdskopier, når projektet slutter, og bruger aldrig jeres data til at træne modeller for andre kunder."),
    ("Kan vi ikke bare bruge ChatGPT eller Copilot?",
     "Til én persons enkeltopgaver ofte jo. Men et chatvindue læser ikke jeres indbakke, indtaster ikke ordrer i jeres ERP og kører ikke af sig selv, og ingen måler, om svarene er rigtige. Vi bygger systemet omkring modellen: koblet på jeres værktøjer, testet på jeres data, dækket af en databehandleraftale og vedligeholdt af os. Hvis en chatassistent er alt, I har brug for, siger vi det i første opkald."),
    ("Hvad er et Process X-ray helt præcist?",
     "En analyse på to uger til fast pris af den aktivitetslog, et af jeres forretningssystemer allerede gemmer. Vi kalder det et X-ray, fordi det viser, hvad der sker inde i en proces, uden at ændre noget. I får et kort over, hvordan sagerne reelt flyder, hvor tiden går tabt, hvem der er overbelastet, og hvilke forbedringer der bedst kan betale sig først. Vi skal kun bruge ét udtræk med fire kolonner: sags-ID, trin, tidsstempel og person eller team. Vi har aldrig brug for adgang til jeres systemer."),
    ("Erstatter det vores styresystem?",
     "Nej. I industrielle processer sidder AI'en oven på jeres eksisterende PID- og SCADA-styring og foreslår eller sætter bedre setpunkter inden for grænser, I selv fastsætter. Den testes først i simulering på jeres historiske data, og jeres operatører kan altid overstyre den."),
    ("I er en ung virksomhed. Hvorfor skal vi stole på jer?",
     "Godt spørgsmål. Derfor starter vi med et lille pilotprojekt til fast pris og viser målte resultater, før I forpligter jer til mere. I arbejder direkte med de to ingeniører, der bygger jeres system, alt er dækket af en skriftlig aftale, og I kan tjekke vores registrering på virk.dk."),
]

TITLE = "GoldenDane · AI, der tager det gentagne papirarbejde fra jeres team"
DESC = ("GoldenDane ApS er en københavnsk virksomhed inden for anvendt AI. Vi automatiserer ordreindtastning, "
        "kundemails og dokumentgennemgang i de systemer, I allerede bruger, og dokumenterer nøjagtigheden på jeres "
        "egne data, før jeres team stoler på den. Pilotprojekter til fast pris og databehandleraftale før data.")
OG_DESC = ("Ordrer, kundemails og dokumenter håndteret af AI, der arbejder i jeres systemer og testes på jeres data først. "
           "Pilotprojekter til fast pris fra en registreret dansk virksomhed.")

org = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "GoldenDane", "legalName": "GoldenDane ApS",
       "url": "https://goldenda.com/da/", "logo": "https://goldenda.com/assets/brand/goldendane-mark.png",
       "image": "https://goldenda.com/og-image.png", "email": "hello@goldenda.com", "telephone": "+45 50 39 84 24",
       "taxID": "46351789", "inLanguage": "da",
       "address": {"@type": "PostalAddress", "addressLocality": "København", "addressCountry": "DK"}, "areaServed": "DK",
       "founder": [{"@type": "Person", "name": "Soheil Ghoreishi", "jobTitle": "Medstifter og CEO"},
                   {"@type": "Person", "name": "Vadim Ionas", "jobTitle": "Medstifter og CTO"}],
       "description": "Anvendt AI til driftsteams: automatisering af ordreindtastning, kundemails og dokumentgennemgang, Process X-rays og procesoptimering."}
faq = {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

HEAD = f"""<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="https://goldenda.com/da/">
<link rel="alternate" hreflang="en" href="https://goldenda.com/">
<link rel="alternate" hreflang="da" href="https://goldenda.com/da/">
<link rel="alternate" hreflang="x-default" href="https://goldenda.com/">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{OG_DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://goldenda.com/da/">
<meta property="og:site_name" content="GoldenDane">
<meta property="og:locale" content="da_DK">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:image" content="https://goldenda.com/og-image-da.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10181A">
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<link rel="preload" href="../assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/fonts.css">
<script type="application/ld+json">
{json.dumps(org, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="../assets/site.css">
</head>"""

head_start = src.index('<html lang="en">')
head_end = src.index("</head>") + len("</head>")
out = src[:head_start] + HEAD + src[head_end:]

# (English, Danish, expected count)
R = [
    # navigation and chrome
    ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Spring til indhold</a>', 1),
    ('aria-label="GoldenDane, back to top"', 'aria-label="GoldenDane, til toppen"', 1),
    ('aria-label="Main"', 'aria-label="Hovedmenu"', 1),
    ('<li><a href="#services">Services</a></li>\n        <li><a href="#xray">Process X-ray</a></li>\n        <li><a href="#how">How we work</a></li>\n        <li><a href="#team">Team</a></li>\n        <li><a href="#faq">FAQ</a></li>',
     '<li><a href="#services">Ydelser</a></li>\n        <li><a href="#xray">Process X-ray</a></li>\n        <li><a href="#how">Sådan arbejder vi</a></li>\n        <li><a href="#team">Team</a></li>\n        <li><a href="#faq">Spørgsmål</a></li>', 1),
    ('<a class="lang" href="da/" hreflang="da" lang="da" aria-label="Dansk version"><svg class="flag" viewBox="0 0 37 28" aria-hidden="true"><rect width="37" height="28" fill="#C8102E"/><path d="M12 0h4v28h-4zM0 12h37v4H0z" fill="#fff"/></svg><span class="lang-l">Dansk</span><span class="lang-s">DA</span></a>',
     '<a class="lang" href="../" hreflang="en" lang="en" aria-label="English version"><svg class="flag" viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><clipPath id="uk-a"><path d="M0 0v30h60V0z"/></clipPath><clipPath id="uk-b"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#uk-a)"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#uk-b)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg><span class="lang-l">English</span><span class="lang-s">EN</span></a>', 1),
    ('<span class="long">Book a call</span><span class="short">Contact</span>', '<span class="long">Book et opkald</span><span class="short">Kontakt</span>', 1),
    ('aria-label="Open menu"', 'aria-label="Åbn menu"', 1),

    # hero
    ('<div class="eyebrow">Applied AI for operations teams · Copenhagen</div>', '<div class="eyebrow">Anvendt AI til driftsteams · København</div>', 1),
    ('We automate the admin your team still does <em>by hand.</em>', 'Vi automatiserer det papirarbejde, jeres team stadig laver <em>i hånden.</em>', 1),
    ('Orders typed into the ERP. The same customer emails, every day. Contracts read line by line. GoldenDane builds AI that does the first pass inside the systems you already use, and proves its accuracy on your own data before anyone relies on it.',
     'Ordrer, der tastes ind i ERP-systemet. De samme kundemails hver dag. Kontrakter, der læses linje for linje. GoldenDane bygger AI, der tager første gennemgang inde i de systemer, I allerede bruger, og dokumenterer nøjagtigheden på jeres egne data, før nogen stoler på den.', 1),
    ('Book a free 30-min call <span class="arr"', 'Book et gratis opkald på 30 min. <span class="arr"', 1),
    ('<a class="btn btn-ghost" href="process-xray.html">See a sample report</a>', '<a class="btn btn-ghost" href="../process-xray.html" hreflang="en">Se en eksempelrapport</a>', 1),
    ('You talk directly to <b>Soheil and Vadim</b>, the two DTU engineers who scope, build and support your system.',
     'I taler direkte med <b>Soheil og Vadim</b>, de to DTU-ingeniører, der afgrænser, bygger og supporterer jeres system.', 1),

    # hero mock
    ('aria-label="Examples of what GoldenDane systems do"', 'aria-label="Eksempler på, hvad GoldenDanes systemer gør"', 1),
    ('aria-label="Example workflows"', 'aria-label="Eksempler på arbejdsgange"', 1),
    ('>Order intake<span', '>Ordremodtagelse<span', 1),
    ('>Customer email<span', '>Kundemail<span', 1),
    ('>Tender review<span', '>Udbudsgennemgang<span', 1),
    ('Order inbox → ERP', 'Ordreindbakke → ERP', 1),
    ('Email from Purchasing, customer #2041', 'Mail fra Indkøb, kunde #2041', 1),
    ('PDF order · read in 9 s', 'PDF-ordre · læst på 9 s', 1),
    ('Oak board 22×145, 3.0 m<span class="sku">SKU 10-2215 · price list B</span></span><span class="q">240 pcs</span>',
     'Egebræt 22×145, 3,0 m<span class="sku">SKU 10-2215 · prisliste B</span></span><span class="q">240 stk.</span>', 1),
    ('Deck screws A4 5×60<span class="sku">SKU 33-0560 · box of 200</span></span><span class="q">12 box</span>',
     'Terrasseskruer A4 5×60<span class="sku">SKU 33-0560 · æske à 200</span></span><span class="q">12 æsker</span>', 1),
    ('Galvanised post anchor<span class="sku">SKU 41-0090 · stock 64</span></span><span class="q">80 pcs</span>',
     'Galvaniseret stolpesko<span class="sku">SKU 41-0090 · lager 64</span></span><span class="q">80 stk.</span>', 1),
    ('<span class="tag ok">Matched</span>', '<span class="tag ok">Matchet</span>', 3),
    ('<span class="tag check">Check</span>', '<span class="tag check">Tjek</span>', 2),
    ('Flagged for a person', 'Markeret til en person', 1),
    ('80 anchors ordered, 64 in stock. Split the delivery or offer the 41-0095 alternative?',
     '80 stolpesko bestilt, 64 på lager. Del leverancen op eller tilbyd alternativet 41-0095?', 1),
    ('↳ Stock: warehouse 1 · Customer terms: partial delivery allowed', '↳ Lager: lager 1 · Kundevilkår: dellevering tilladt', 1),
    ('<b>3</b> lines · <b>1</b> needs a human · delivery Thu 15 Oct', '<b>3</b> linjer · <b>1</b> kræver en person · levering tor. 15. okt.', 1),
    ('<span class="approve">Post to ERP</span>', '<span class="approve">Send til ERP</span>', 1),
    ('Customer service · shared inbox', 'Kundeservice · fælles indbakke', 1),
    ('New email · order #10482', 'Ny mail · ordre #10482', 1),
    ('Topic: delivery + returns', 'Emne: levering + returnering', 1),
    ('“Hi, my order hasn\'t arrived yet. If it comes after the weekend, can I still return it?”',
     '“Hej, min ordre er ikke kommet endnu. Hvis den kommer efter weekenden, kan jeg så stadig returnere den?”', 1),
    ('<span class="req-id">Draft reply</span><span class="tag ok">Sources found</span>', '<span class="req-id">Svarudkast</span><span class="tag ok">Kilder fundet</span>', 1),
    ('Hi Anna, your order left our warehouse on 6 October and is out for delivery today. And yes: you can return it within 30 days of delivery, free of charge.',
     'Hej Anna. Din ordre forlod vores lager den 6. oktober og er ude til levering i dag. Og ja: du kan returnere den gratis inden for 30 dage efter levering.', 1),
    ('↳ Order system #10482 · Returns policy §2', '↳ Ordresystem #10482 · Returpolitik §2', 1),
    ('<span class="req-id">Same queue</span><span class="tag ok">11 drafted</span>', '<span class="req-id">Samme kø</span><span class="tag ok">11 udkast</span>', 1),
    ('11 more delivery-status emails drafted and waiting for a quick review.', '11 mails mere om leveringsstatus har fået et svarudkast og venter på et hurtigt kig.', 1),
    ('Drafted in <b>4 s</b> · in your house style', 'Udkast på <b>4 s</b> · i jeres egen tone', 1),
    ('<span class="approve">Approve &amp; send</span>', '<span class="approve">Godkend og send</span>', 1),
    ('Tender review · harbour bridge', 'Udbudsgennemgang · havnebro', 1),
    ('Tender package (7 files)', 'Udbudsmateriale (7 filer)', 1),
    ('412 pages · read in 6 min', '412 sider · læst på 6 min', 1),
    ('REQ-014 · Structural', 'REQ-014 · Konstruktion', 1),
    ('Fatigue design for steel components per EN 1993-1-9, detail category ≥ 71.', 'Udmattelsesdimensionering af stålkomponenter efter EN 1993-1-9, kærvklasse ≥ 71.', 1),
    ('↳ Specification B, p. 87 §4.3.2', '↳ Specifikation B, s. 87 §4.3.2', 1),
    ('REQ-022 · Documentation', 'REQ-022 · Dokumentation', 1),
    ('As-built BIM model due within 30 days. Conflicts with Appendix 2 (60 days).', 'Som udført-BIM-model skal afleveres inden for 30 dage. Modstrider Bilag 2 (60 dage).', 1),
    ('↳ Contract, p. 12 · Appendix 2, p. 3', '↳ Kontrakt, s. 12 · Bilag 2, s. 3', 1),
    ('<b>143</b> requirements · <b>2</b> need a human', '<b>143</b> krav · <b>2</b> kræver en person', 1),
    ('<span class="approve">Review &amp; approve</span>', '<span class="approve">Gennemgå og godkend</span>', 1),
    ('Illustrations of our systems · not client data', 'Illustrationer af vores systemer · ikke kundedata', 1),

    # trust bar
    ('aria-label="Why you can trust us"', 'aria-label="Hvorfor I kan stole på os"', 1),
    ('<h3>Registered Danish company</h3>', '<h3>Registreret dansk virksomhed</h3>', 1),
    ('Verify on virk.dk&nbsp;↗', 'Tjek os på virk.dk&nbsp;↗', 1),
    ('<h3>GDPR before anything else</h3>\n      <p>Data processing agreement signed before we see any data. EU processing where possible.</p>',
     '<h3>GDPR før alt andet</h3>\n      <p>Databehandleraftale underskrevet, før vi ser data. Behandling i EU, hvor det er muligt.</p>', 1),
    ('<h3>Fixed price, no lock-in</h3>\n      <p>Pilots are priced up front. You decide what happens after you\'ve seen the results.</p>',
     '<h3>Fast pris, ingen binding</h3>\n      <p>Pilotprojekter prissættes på forhånd. I beslutter, hvad der skal ske, når I har set resultaterne.</p>', 1),
    ('<h3>Measured, not promised</h3>\n      <p>We report accuracy on your own data before go-live, and keep measuring after.</p>',
     '<h3>Målt, ikke lovet</h3>\n      <p>Vi rapporterer nøjagtigheden på jeres egne data, før løsningen går i drift, og bliver ved med at måle bagefter.</p>', 1),

    # services
    ('<div class="eyebrow">What we do</div>\n      <h2>We take the repetitive work. Your team keeps the final say.</h2>\n      <p class="lede">These are the three kinds of work we automate most. Each runs inside the systems you already use, flags anything it isn\'t sure about, and links every answer to where it came from.</p>',
     '<div class="eyebrow">Det gør vi</div>\n      <h2>Vi tager det gentagne arbejde. Jeres team har stadig det sidste ord.</h2>\n      <p class="lede">Det er de tre typer arbejde, vi oftest automatiserer. Hver løsning kører i de systemer, I allerede bruger, markerer alt, den er i tvivl om, og viser, hvor hvert svar kommer fra.</p>', 1),
    ('01 · Orders and invoices</div>\n        <h3>From inbox to ERP, without retyping.</h3>',
     '01 · Ordrer og fakturaer</div>\n        <h3>Fra indbakke til ERP, uden at taste igen.</h3>', 1),
    ('<li><span>Reads orders, quotes and invoices from email and PDF.</span></li>\n          <li><span>Matches customers, items and prices against your own master data.</span></li>\n          <li><span>Posts clean orders to your ERP and sends the exceptions to a person.</span></li>',
     '<li><span>Læser ordrer, tilbud og fakturaer fra mail og PDF.</span></li>\n          <li><span>Matcher kunder, varer og priser med jeres egne stamdata.</span></li>\n          <li><span>Lægger rene ordrer i jeres ERP og sender undtagelserne til en person.</span></li>', 1),
    ('<p class="for"><b>For</b> order desks, wholesalers, brands and finance teams.</p>', '<p class="for"><b>Til</b> ordrekontorer, grossister, brands og økonomiafdelinger.</p>', 1),
    ('02 · Customer emails</div>\n        <h3>Replies drafted from your own policies.</h3>',
     '02 · Kundemails</div>\n        <h3>Svarudkast ud fra jeres egne regler.</h3>', 1),
    ('<li><span>Sorts incoming email by topic and urgency.</span></li>\n          <li><span>Drafts answers using your order data, policies and tone of voice.</span></li>\n          <li><span>Nothing is sent until someone on your team approves it.</span></li>',
     '<li><span>Sorterer indgående mails efter emne og hast.</span></li>\n          <li><span>Skriver svarudkast ud fra jeres ordredata, regler og tone.</span></li>\n          <li><span>Intet bliver sendt, før en fra jeres team har godkendt det.</span></li>', 1),
    ('<p class="for"><b>For</b> customer service, webshops, travel, utilities and property managers.</p>', '<p class="for"><b>Til</b> kundeservice, webshops, rejsebranchen, forsyning og ejendomsadministration.</p>', 1),
    ('03 · Documents and contracts</div>\n        <h3>Hundreds of pages, checked in minutes.</h3>',
     '03 · Dokumenter og kontrakter</div>\n        <h3>Hundredvis af sider, tjekket på minutter.</h3>', 1),
    ('<li><span>Contracts, tenders, policies, specifications and compliance files.</span></li>\n          <li><span>Key terms, requirements and deviations, each linked to the exact clause or page.</span></li>\n          <li><span>Conflicts and gaps flagged for your expert to decide.</span></li>',
     '<li><span>Kontrakter, udbud, politikker, specifikationer og compliance-dokumenter.</span></li>\n          <li><span>Nøglevilkår, krav og afvigelser, hver med henvisning til den præcise klausul eller side.</span></li>\n          <li><span>Konflikter og huller markeres, så jeres fagfolk kan beslutte.</span></li>', 1),
    ('<p class="for"><b>For</b> law firms, brokers, accountants, engineering and construction.</p>', '<p class="for"><b>Til</b> advokatfirmaer, forsikringsmæglere, revisorer, rådgivende ingeniører og byggeri.</p>', 1),
    ('<div class="eyebrow">Not sure where to start?</div>\n        <h3>Begin with a two-week Process X-ray.</h3>\n        <p>We analyse one export from your ERP, ticketing or case system and show you where work really waits, loops and piles up. No system access, fixed price.</p>\n        <p><a class="link" href="#xray">How the X-ray works →</a></p>',
     '<div class="eyebrow">I tvivl om, hvor I skal starte?</div>\n        <h3>Start med et Process X-ray på to uger.</h3>\n        <p>Vi analyserer ét udtræk fra jeres ERP-, ticket- eller sagssystem og viser, hvor arbejdet faktisk venter, går i ring og hober sig op. Ingen systemadgang, fast pris.</p>\n        <p><a class="link" href="#xray">Sådan virker et X-ray →</a></p>', 1),
    ('<div class="eyebrow">Also: industrial processes</div>\n          <h3>AI on top of your control system, not instead of it.</h3>\n          <p>Setpoint optimisation, soft sensors and early warnings for district heating, water, and process manufacturing. Tested in simulation on your history first.</p>',
     '<div class="eyebrow">Også: industrielle processer</div>\n          <h3>AI oven på jeres styresystem, ikke i stedet for det.</h3>\n          <p>Setpunktsoptimering, softsensorer og tidlige advarsler til fjernvarme, vand og procesindustri. Testet i simulering på jeres historiske data først.</p>', 1),
    ('aria-label="Illustration: a fixed setpoint stays high all day, while an AI-optimised setpoint follows demand and runs lower most of the time."',
     'aria-label="Illustration: et fast setpunkt ligger højt hele dagen, mens et AI-optimeret setpunkt følger behovet og ligger lavere det meste af tiden."', 1),
    ('— fixed setpoint · <span style="color:var(--gold-ink)">— AI-optimised</span>', '— fast setpunkt · <span style="color:var(--gold-ink)">— AI-optimeret</span>', 1),

    # who we help
    ('<div class="eyebrow">Who we help</div>\n      <h2>If your team retypes, copies or answers the same thing every week, we can probably help.</h2>\n      <p class="lede">You don\'t need to be technical, and you don\'t need new software. These are the teams we build for.</p>',
     '<div class="eyebrow">Hvem vi hjælper</div>\n      <h2>Hvis jeres team taster, kopierer eller besvarer det samme hver uge, kan vi sandsynligvis hjælpe.</h2>\n      <p class="lede">I behøver ikke være tekniske, og I behøver ikke nyt software. Det er de teams, vi bygger til.</p>', 1),
    ('<h3>Order desks · wholesale and brands</h3><p>Orders and invoices entered automatically. Your team checks the exceptions.</p>',
     '<h3>Ordrekontorer · grossister og brands</h3><p>Ordrer og fakturaer indtastes automatisk. Jeres team tjekker undtagelserne.</p>', 1),
    ('<h3>Customer service</h3><p>"Where\'s my order" and returns answered in draft from your own data.</p>',
     '<h3>Kundeservice</h3><p>“Hvor er min ordre?” og returneringer besvaret i udkast ud fra jeres egne data.</p>', 1),
    ('<h3>Law firms and legal teams</h3><p>Key terms and deviations, each linked to the exact clause.</p>',
     '<h3>Advokatfirmaer og juridiske afdelinger</h3><p>Nøglevilkår og afvigelser, hver med henvisning til den præcise klausul.</p>', 1),
    ('<h3>Insurance and pension brokers</h3><p>Quotes and policy wordings compared side by side, with sources.</p>',
     '<h3>Forsikrings- og pensionsmæglere</h3><p>Tilbud og forsikringsbetingelser sammenlignet side om side, med kilder.</p>', 1),
    ('<h3>Property managers and estate agents</h3><p>Tenant emails, leases and move-out paperwork sorted and drafted.</p>',
     '<h3>Ejendomsadministratorer og ejendomsmæglere</h3><p>Lejermails, lejekontrakter og fraflytningspapirer sorteret og skrevet i udkast.</p>', 1),
    ('<h3>Accounting and finance teams</h3><p>Receipts and invoices extracted and checked, reminders drafted.</p>',
     '<h3>Regnskab og økonomi</h3><p>Bilag og fakturaer aflæst og tjekket, rykkere skrevet i udkast.</p>', 1),
    ('<h3>Engineering and construction</h3><p>Requirements lists and conflict checks from tenders in minutes.</p>',
     '<h3>Rådgivende ingeniører og byggeri</h3><p>Kravlister og konflikttjek fra udbud på minutter.</p>', 1),
    ('<h3>Case handling · insurers, municipalities, unemployment funds</h3><p>A Process X-ray shows where cases wait. Then we fix it.</p>',
     '<h3>Sagsbehandling · forsikring, kommuner, a-kasser</h3><p>Et Process X-ray viser, hvor sagerne venter. Så løser vi det.</p>', 1),
    ('Don\'t see your team? <a class="link" href="#contact">Tell us which task eats your week</a> and we\'ll say honestly whether we can help.',
     'Kan I ikke se jeres team? <a class="link" href="#contact">Fortæl os, hvilken opgave der æder jeres uge</a>, så siger vi ærligt, om vi kan hjælpe.', 1),

    # worked example
    ('<div class="eyebrow">A worked example</div>\n      <h2>Mette is a bid manager, not a copy-paste machine.</h2>\n      <p class="lede">Mette works at a 60-person engineering consultancy. A new tender lands every week, and each one runs to hundreds of pages. Here\'s her Monday before and after.</p>',
     '<div class="eyebrow">Et konkret eksempel</div>\n      <h2>Mette er tilbudsansvarlig, ikke en copy-paste-maskine.</h2>\n      <p class="lede">Mette arbejder i et rådgivende ingeniørfirma med 60 ansatte. Der lander et nyt udbud hver uge, og hvert udbud fylder hundredvis af sider. Her er hendes mandag før og efter.</p>', 1),
    ('<h3>Before</h3><span class="day-label">By hand</span>', '<h3>Før</h3><span class="day-label">I hånden</span>', 1),
    ('Downloads seven files, 412 pages in total. Opens a blank spreadsheet.', 'Downloader syv filer, 412 sider i alt. Åbner et tomt regneark.', 1),
    ('A senior engineer joins to read the technical specification line by line.', 'En senioringeniør hjælper med at læse den tekniske specifikation linje for linje.', 1),
    ('Finds a deadline in an appendix that contradicts the contract. Starts that section again.', 'Finder en frist i et bilag, der modsiger kontrakten. Starter forfra på det afsnit.', 1),
    ('The requirements list is "mostly done". Nobody is sure what was missed.', 'Kravlisten er “næsten færdig”. Ingen ved med sikkerhed, hvad der er overset.', 1),
    ('<span>Time spent by two people</span><strong>~14 hours</strong>', '<span>Tid brugt af to personer</span><strong>~14 timer</strong>', 1),
    ('<h3>With GoldenDane</h3><span class="day-label">AI drafts, people decide</span>', '<h3>Med GoldenDane</h3><span class="day-label">AI laver udkastet, mennesker beslutter</span>', 1),
    ('Drops the tender package into the review tool.', 'Lægger udbudsmaterialet i gennemgangsværktøjet.', 1),
    ('Gets 143 requirements, each linked to the exact page and paragraph.', 'Får 143 krav, hver med henvisning til den præcise side og det præcise afsnit.', 1),
    ('Two conflicts are flagged for a human, including the appendix deadline.', 'To konflikter markeres til en person, herunder fristen i bilaget.', 1),
    ('The engineer reviews only the flagged items. The list is approved and exported.', 'Ingeniøren gennemgår kun de markerede punkter. Listen godkendes og eksporteres.', 1),
    ('<span>Time spent by two people</span><strong>~2 hours</strong>', '<span>Tid brugt af to personer</span><strong>~2 timer</strong>', 1),
    ('Mette is an illustrative example of the workflows we build for, not a client. Savings depend on your documents and team, which is exactly why we measure them in a short pilot before you commit to anything.',
     'Mette er et illustrativt eksempel på de arbejdsgange, vi bygger til, ikke en kunde. Besparelsen afhænger af jeres dokumenter og team, og netop derfor måler vi den i et kort pilotprojekt, før I forpligter jer til noget.', 1),

    # process x-ray
    ('<div class="eyebrow">Process X-ray · tested on real data</div>\n      <h2>Your systems already know where the time goes. We show you.</h2>\n      <p class="lede">A Process X-ray is a two-week analysis of the activity log your business systems already keep. Like an X-ray, it shows what\'s inside without opening anything up: no new software and no access to your systems, just one data export.</p>',
     '<div class="eyebrow">Process X-ray · testet på rigtige data</div>\n      <h2>Jeres systemer ved allerede, hvor tiden går. Vi viser jer det.</h2>\n      <p class="lede">Et Process X-ray er en analyse på to uger af den aktivitetslog, jeres forretningssystemer allerede gemmer. Ligesom et røntgenbillede viser det, hvad der foregår indeni, uden at åbne noget: intet nyt software og ingen adgang til jeres systemer, kun ét dataudtræk.</p>', 1),
    ('<dt>You send</dt><dd>One export from your ERP, ticketing, order or claims system, with four columns: <code>case ID</code> <code>step</code> <code>timestamp</code> <code>person or team</code></dd>',
     '<dt>I sender</dt><dd>Ét udtræk fra jeres ERP-, ticket-, ordre- eller skadesystem med fire kolonner: <code>sags-ID</code> <code>trin</code> <code>tidsstempel</code> <code>person eller team</code></dd>', 1),
    ('<dt>We take</dt><dd>Two weeks, at a fixed price agreed up front. We sign a data processing agreement before you send anything.</dd>',
     '<dt>Vi bruger</dt><dd>To uger til en fast pris, aftalt på forhånd. Vi underskriver en databehandleraftale, før I sender noget.</dd>', 1),
    ('<dt>You get</dt><dd>Your real process map, where the time goes, the bottlenecks and the fixes worth making first, with estimated impact, plus a walkthrough with your team.</dd>',
     '<dt>I får</dt><dd>Jeres faktiske proceskort: hvor tiden går, flaskehalsene og de forbedringer, der bedst kan betale sig først, med estimeret effekt, plus en gennemgang med jeres team.</dd>', 1),
    ('Here\'s what an X-ray found in 4,580 real support tickets from a public dataset:', 'Her er, hvad et X-ray fandt i 4.580 rigtige supportsager fra et offentligt datasæt:', 1),
    ('<b>Where 40 days of ticket time actually went</b><span>4,580 tickets · 2010–2014</span>', '<b>Hvor 40 dages sagstid reelt gik hen</b><span>4.580 sager · 2010–2014</span>', 1),
    ('aria-label="Share of all elapsed ticket time"', 'aria-label="Andel af den samlede sagstid"', 1),
    ('<span>Waiting window after the fix</span>', '<span>Ventevindue efter løsningen</span>', 1),
    ('<span>Hands-on handling</span>', '<span>Aktiv behandling</span>', 1),
    ('<span>Queue before pickup</span>', '<span>Kø, før sagen tages</span>', 1),
    ('<span>Parked in "Wait" status</span>', '<span>Parkeret i status “Wait”</span>', 1),
    ('<span>Escalated to development</span>', '<span>Eskaleret til udvikling</span>', 1),
    ('<span class="pct">72%</span>', '<span class="pct">72 %</span>', 1),
    ('<span class="pct">11%</span>', '<span class="pct">11 %</span>', 1),
    ('<span class="pct">9%</span>', '<span class="pct">9 %</span>', 1),
    ('<span class="pct">8%</span>', '<span class="pct">8 %</span>', 1),
    ('<span class="pct">1%</span>', '<span class="pct">1 %</span>', 1),
    ('Tickets took 40 days to close but only 6 to fix. Most of the difference was a fixed confirmation window, not work. Public data from an Italian software company\'s IT help desk; findings are associations, not proof of cause.',
     'Sagerne tog 40 dage at lukke, men kun 6 at løse. Det meste af forskellen var et fast bekræftelsesvindue, ikke arbejde. Offentlige data fra et italiensk softwarefirmas IT-helpdesk; resultaterne viser sammenhænge, ikke årsager.', 1),
    ('<span class="big">18.0</span><h3>days to fix if nobody picks it up within 3 days</h3><p>Tickets picked up within a day were fixed in 1.2 days. The queue, not the work, made the difference.</p>',
     '<span class="big">18,0</span><h3>dage til løsning, hvis ingen tager sagen inden for 3 dage</h3><p>Sager, der blev taget inden for en dag, blev løst på 1,2 dage. Det var køen, ikke arbejdet, der gjorde forskellen.</p>', 1),
    ('<span class="big">18.4</span><h3>days to fix after two or more handovers</h3><p>Tickets solved by the first person took 1 day. Every hand-off multiplied the time.</p>',
     '<span class="big">18,4</span><h3>dage til løsning efter to eller flere overdragelser</h3><p>Sager, der blev løst af den første person, tog 1 dag. Hver overdragelse gangede tiden op.</p>', 1),
    ('<span class="big">49%</span><h3>of all handovers went through one person</h3><p>A bottleneck in busy weeks, and a risk whenever they\'re away.</p>',
     '<span class="big">49 %</span><h3>af alle overdragelser gik gennem én person</h3><p>En flaskehals i travle uger og en risiko, når personen er væk.</p>', 1),
    ('<a class="btn btn-primary" href="process-xray.html">Read the full sample report <span class="arr" aria-hidden="true">→</span></a>',
     '<a class="btn btn-primary" href="../process-xray.html" hreflang="en">Læs hele eksempelrapporten (på engelsk) <span class="arr" aria-hidden="true">→</span></a>', 1),
    ('data-topic="Process X-ray">Ask about an X-ray of your process</a>', 'data-topic="Process X-ray">Spørg om et X-ray af jeres proces</a>', 1),

    # how we work
    ('<div class="eyebrow">How we work</div>\n      <h2>Prove it small. Then build it properly.</h2>\n      <p class="lede">You never pay for a big project on faith. Every engagement starts with one workflow and a number we can measure.</p>',
     '<div class="eyebrow">Sådan arbejder vi</div>\n      <h2>Bevis det i det små. Byg det så ordentligt.</h2>\n      <p class="lede">I betaler aldrig for et stort projekt i blinde. Hvert forløb starter med én arbejdsgang og et tal, vi kan måle.</p>', 1),
    ('<span class="when">30 min · free</span></div>\n        <h3>Discover</h3>\n        <p>You show us the workflow that eats your team\'s week. We ask how often it happens, who does it and which systems hold the data.</p>\n        <div class="out">You get an honest view of whether AI can help, and roughly how much.</div>',
     '<span class="when">30 min · gratis</span></div>\n        <h3>Afdæk</h3>\n        <p>I viser os den arbejdsgang, der æder jeres teams uge. Vi spørger, hvor ofte den forekommer, hvem der udfører den, og hvilke systemer der har dataene.</p>\n        <div class="out">I får en ærlig vurdering af, om AI kan hjælpe, og cirka hvor meget.</div>', 1),
    ('<span class="when">2–3 weeks · fixed price</span></div>\n        <h3>Prove</h3>\n        <p>We build a working prototype on your real documents or process data and measure its accuracy against your team\'s own results.</p>\n        <div class="out">You get a working prototype, an accuracy report and the time saved.</div>',
     '<span class="when">2–3 uger · fast pris</span></div>\n        <h3>Bevis</h3>\n        <p>Vi bygger en fungerende prototype på jeres rigtige dokumenter eller procesdata og måler nøjagtigheden op mod jeres teams egne resultater.</p>\n        <div class="out">I får en fungerende prototype, en nøjagtighedsrapport og den sparede tid.</div>', 1),
    ('<span class="when">When the numbers hold up</span></div>\n        <h3>Deploy</h3>\n        <p>We connect it to your systems, add access control, monitoring and approval steps, and train your team.</p>\n        <div class="out">You get a system in daily use, with support and ongoing improvement.</div>',
     '<span class="when">Når tallene holder</span></div>\n        <h3>Implementér</h3>\n        <p>Vi kobler løsningen på jeres systemer, tilføjer adgangsstyring, overvågning og godkendelsestrin og træner jeres team.</p>\n        <div class="out">I får et system i daglig brug, med support og løbende forbedringer.</div>', 1),
    ('From the first call to measured results: about a month.', 'Fra første opkald til målte resultater: cirka en måned.', 1),

    # why not chatgpt
    ('<div class="eyebrow">Why not just use ChatGPT?</div>\n      <h2>A chat window helps one person. We build a system your whole team can rely on.</h2>\n      <p class="lede">ChatGPT and Copilot are great for one-off tasks, and we use the same kind of models. The difference is everything around the model: where it runs, how it\'s tested, and who is responsible for it.</p>',
     '<div class="eyebrow">Hvorfor ikke bare bruge ChatGPT?</div>\n      <h2>Et chatvindue hjælper én person. Vi bygger et system, hele jeres team kan stole på.</h2>\n      <p class="lede">ChatGPT og Copilot er gode til enkeltopgaver, og vi bruger den samme slags modeller. Forskellen er alt det omkring modellen: hvor den kører, hvordan den testes, og hvem der har ansvaret.</p>', 1),
    ('aria-label="A chat assistant compared with a GoldenDane system"', 'aria-label="En chatassistent sammenlignet med et GoldenDane-system"', 1),
    ('<span role="columnheader">A chat assistant</span><span role="columnheader">A GoldenDane system</span>', '<span role="columnheader">En chatassistent</span><span role="columnheader">Et GoldenDane-system</span>', 1),
    ('<b role="rowheader">Where it works</b><span role="cell">In a chat window. Someone pastes the email or PDF in and copies the answer out.</span><span role="cell">Inside your inbox, ERP or case system. Work flows in and out without copy-paste.</span>',
     '<b role="rowheader">Hvor den arbejder</b><span role="cell">I et chatvindue. Nogen indsætter mailen eller PDF\'en og kopierer svaret ud.</span><span role="cell">Inde i jeres indbakke, ERP- eller sagssystem. Arbejdet flyder ind og ud uden copy-paste.</span>', 1),
    ('<b role="rowheader">Who runs it</b><span role="cell">A person, every time, when they remember to.</span><span role="cell">It runs by itself all day. Your team only handles what it flags.</span>',
     '<b role="rowheader">Hvem der kører den</b><span role="cell">En person, hver gang, når vedkommende husker det.</span><span role="cell">Den kører af sig selv hele dagen. Jeres team håndterer kun det, den markerer.</span>', 1),
    ('<b role="rowheader">How you know it\'s right</b><span role="cell">Only if someone checks every answer.</span><span role="cell">We measure accuracy on your own data before go-live, and keep measuring after.</span>',
     '<b role="rowheader">Hvordan I ved, den har ret</b><span role="cell">Kun hvis nogen tjekker hvert svar.</span><span role="cell">Vi måler nøjagtigheden på jeres egne data, før løsningen går i drift, og bliver ved med at måle bagefter.</span>', 1),
    ('<b role="rowheader">Your data</b><span role="cell">Depends on which account and settings each employee happens to use.</span><span role="cell">A signed data processing agreement, EU processing where possible, no training on your data, access control and an audit trail.</span>',
     '<b role="rowheader">Jeres data</b><span role="cell">Afhænger af, hvilken konto og hvilke indstillinger den enkelte medarbejder tilfældigvis bruger.</span><span role="cell">En underskrevet databehandleraftale, behandling i EU, hvor det er muligt, ingen træning på jeres data, adgangsstyring og fuld logning af, hvem der gjorde hvad.</span>', 1),
    ('<b role="rowheader">When something changes</b><span role="cell">The prompt quietly stops working.</span><span role="cell">We monitor it and fix it. One party is responsible: us.</span>',
     '<b role="rowheader">Når noget ændrer sig</b><span role="cell">Prompten holder stille og roligt op med at virke.</span><span role="cell">Vi overvåger og retter det. Én part har ansvaret: os.</span>', 1),
    ('<h3>Tested before trusted</h3><p>Every system is evaluated on a labelled sample of your own data, and you see the accuracy before it goes live.</p>',
     '<h3>Testet, før I stoler på det</h3><p>Hvert system evalueres på en stikprøve af jeres egne data med kendte svar, og I ser nøjagtigheden, før det går i drift.</p>', 1),
    ('<h3>Sources, always</h3><p>Every extracted value and answer links back to the page, paragraph or record it came from.</p>',
     '<h3>Altid med kilder</h3><p>Hver udtrukket værdi og hvert svar henviser til den side, det afsnit eller den post, det kommer fra.</p>', 1),
    ('<h3>People decide</h3><p>AI takes the first pass. Your team approves, corrects and stays accountable, with a full audit trail.</p>',
     '<h3>Mennesker beslutter</h3><p>AI tager første gennemgang. Jeres team godkender, retter og har stadig ansvaret, og alt bliver logget.</p>', 1),
    ('<h3>Your data stays yours</h3><p>Data handling agreed in writing before we start. Never used to train models for anyone else.</p>',
     '<h3>Jeres data forbliver jeres</h3><p>Datahåndteringen aftales skriftligt, før vi starter. Data bruges aldrig til at træne modeller for andre.</p>', 1),

    # team
    ('<div class="eyebrow">Who you\'ll work with</div>\n      <h2>Two engineers. No account managers in between.</h2>\n      <p class="lede">GoldenDane is a small, focused team from DTU, the Technical University of Denmark. The people you meet on the first call are the people who build and support your system.</p>',
     '<div class="eyebrow">Dem, I arbejder med</div>\n      <h2>To ingeniører. Ingen mellemled.</h2>\n      <p class="lede">GoldenDane er et lille, fokuseret team fra DTU, Danmarks Tekniske Universitet. Dem, I møder i første opkald, er dem, der bygger og supporterer jeres system.</p>', 1),
    ('<div class="role">Co-founder · CEO</div>', '<div class="role">Medstifter · CEO</div>', 1),
    ('<p>Soheil leads client work: he maps your workflow, scopes the pilot and makes sure results are measured in hours and kroner, not buzzwords. Background in Human-Centered Artificial Intelligence at DTU.</p>\n          <p class="does">Your first call and your main contact.</p>',
     '<p>Soheil leder kundearbejdet: han kortlægger jeres arbejdsgang, afgrænser pilotprojektet og sørger for, at resultaterne måles i timer og kroner, ikke i buzzwords. Baggrund i Human-Centered Artificial Intelligence på DTU.</p>\n          <p class="does">Jeres første opkald og jeres faste kontakt.</p>', 1),
    ('<div class="role">Co-founder · CTO</div>', '<div class="role">Medstifter · CTO</div>', 1),
    ('<p>International Physics Olympiad medalist with a background in algorithms, applied mathematics and machine learning. Vadim designs and builds the systems, from document pipelines to optimisation models.</p>\n          <p class="does">Builds and tests your system.</p>',
     '<p>Medaljevinder ved den Internationale Fysikolympiade med baggrund i algoritmer, anvendt matematik og machine learning. Vadim designer og bygger systemerne, fra dokumentbehandling til optimeringsmodeller.</p>\n          <p class="does">Bygger og tester jeres system.</p>', 1),
    ('<span><i aria-hidden="true"></i>Based in Copenhagen</span>', '<span><i aria-hidden="true"></i>Baseret i København</span>', 1),
    ('<span><i aria-hidden="true"></i>Reply within one working day</span>', '<span><i aria-hidden="true"></i>Svar inden for én arbejdsdag</span>', 1),

    # faq heading
    ('<div class="eyebrow">Questions</div>\n      <h2>What people usually ask us.</h2>', '<div class="eyebrow">Spørgsmål</div>\n      <h2>Det spørger folk os typisk om.</h2>', 1),
    ('Something else? Write to <a class="link" href="mailto:hello@goldenda.com">hello@goldenda.com</a> or call',
     'Noget andet? Skriv til <a class="link" href="mailto:hello@goldenda.com">hello@goldenda.com</a> eller ring på', 1),

    # contact
    ('<div class="eyebrow">Let\'s talk</div>\n      <h2>Which workflow eats your team\'s week?</h2>\n      <p class="lede">Tell us in two or three sentences. Here\'s what happens next:</p>',
     '<div class="eyebrow">Lad os tale sammen</div>\n      <h2>Hvilken arbejdsgang æder jeres teams uge?</h2>\n      <p class="lede">Fortæl os det med to-tre sætninger. Det sker der bagefter:</p>', 1),
    ('<li><span>We reply within one working day and suggest a time.</span></li>\n        <li><span>A free 30-minute call with both founders, on video or by phone.</span></li>\n        <li><span>If it\'s a fit, a written fixed-price pilot proposal. If not, we tell you.</span></li>',
     '<li><span>Vi svarer inden for én arbejdsdag og foreslår et tidspunkt.</span></li>\n        <li><span>Et gratis opkald på 30 minutter med begge stiftere, på video eller telefon.</span></li>\n        <li><span>Hvis det passer, får I et skriftligt tilbud på et pilotprojekt til fast pris. Hvis ikke, siger vi det.</span></li>', 1),
    ('mailto:hello@goldenda.com?subject=Workflow%20review', 'mailto:hello@goldenda.com?subject=Gennemgang%20af%20arbejdsgang', 1),
    ('id="copyEmail">Copy address</button>', 'id="copyEmail">Kopiér adresse</button>', 1),
    ('Prefer the phone? Call Soheil on', 'Foretrækker I telefonen? Ring til Soheil på', 1),
    ('<p class="small">GoldenDane ApS · CVR 46351789 · Copenhagen, Denmark</p>', '<p class="small">GoldenDane ApS · CVR 46351789 · København</p>', 1),
    ('<h3>Request a workflow review</h3>', '<h3>Bed om en gennemgang af en arbejdsgang</h3>', 1),
    ('<label for="f-name">Your name</label>', '<label for="f-name">Dit navn</label>', 1),
    ('<label for="f-company">Company</label>', '<label for="f-company">Virksomhed</label>', 1),
    ('<label for="f-msg">Which task takes up your team\'s time?</label>', '<label for="f-msg">Hvilken opgave tager tid fra jeres team?</label>', 1),
    ('placeholder="e.g. We get 150 orders a week by email and type them into our ERP by hand."', 'placeholder="F.eks.: Vi får 150 ordrer om ugen på mail og taster dem ind i vores ERP i hånden."', 1),
    ('Send request <span class="arr"', 'Send forespørgsel <span class="arr"', 1),
    ('This opens a pre-filled email to hello@goldenda.com from your own mail app. See our <a href="privacy.html">privacy notice</a>.',
     'Knappen åbner en udfyldt mail til hello@goldenda.com i dit eget mailprogram. Se vores <a href="privatliv.html">privatlivspolitik</a>.', 1),
    ('Your mail app should open with the message ready to send. If nothing opened, copy your note and email it to <b>hello@goldenda.com</b>. We reply within one working day.',
     'Dit mailprogram skulle nu åbne med beskeden klar til at sende. Hvis intet åbnede, så kopiér din besked og send den til <b>hello@goldenda.com</b>. Vi svarer inden for én arbejdsdag.', 1),
    ('<b>Founding clients</b>\n        <p>We\'re taking on three founding clients: a reduced price on an X-ray or pilot in exchange for honest feedback, and direct access to both founders throughout.</p>',
     '<b>Stiftende kunder</b>\n        <p>Vi tager tre stiftende kunder ind: en reduceret pris på et X-ray eller pilotprojekt mod ærlig feedback og direkte adgang til begge stiftere hele vejen.</p>', 1),

    # footer
    ('Applied AI for operations teams. We automate orders, customer emails and document work, and show you where your processes lose time.',
     'Anvendt AI til driftsteams. Vi automatiserer ordrer, kundemails og dokumentarbejde og viser jer, hvor jeres processer taber tid.', 1),
    ('<h4>Company</h4>', '<h4>Virksomhed</h4>', 1),
    ('<li>Copenhagen, Denmark</li>', '<li>København</li>', 1),
    ('<h4>Explore</h4>', '<h4>Mere</h4>', 1),
    ('<li><a href="#services">Services</a></li>\n        <li><a href="process-xray.html">Sample Process X-ray</a></li>\n        <li><a href="#how">How we work</a></li>\n        <li><a href="privacy.html">Privacy</a></li>\n        <li><a href="da/" hreflang="da" lang="da">Dansk</a></li>',
     '<li><a href="#services">Ydelser</a></li>\n        <li><a href="../process-xray.html" hreflang="en">Eksempel på Process X-ray (engelsk)</a></li>\n        <li><a href="#how">Sådan arbejder vi</a></li>\n        <li><a href="privatliv.html">Privatliv</a></li>\n        <li><a href="../" hreflang="en" lang="en">English</a></li>', 1),
    ('<span>No cookies, no tracking on this site.</span>', '<span>Ingen cookies og ingen sporing på dette website.</span>', 1),
    ('<script src="assets/site.js"></script>', '<script src="../assets/site.js"></script>', 1),
]

errors = []
for en, da, n in R:
    c = out.count(en)
    if c != n:
        errors.append(f"expected {n}, found {c}: {en[:90]!r}")
        continue
    out = out.replace(en, da)

# FAQ answers: replace each <details> block in order
faq_blocks = re.findall(r"<details><summary>.*?</summary><p>.*?</p></details>", out)
if len(faq_blocks) != len(FAQ):
    errors.append(f"expected {len(FAQ)} FAQ items, found {len(faq_blocks)}")
else:
    for block, (q, a) in zip(faq_blocks, FAQ):
        out = out.replace(block, f"<details><summary>{q}</summary><p>{a}</p></details>", 1)

# Files referenced from the page body (e.g. founder photos) live one level up.
out = out.replace('src="assets/', 'src="../assets/')

if errors:
    sys.exit("Danish build stopped. index.html text changed:\n  " + "\n  ".join(errors))

(ROOT / "da").mkdir(exist_ok=True)
(ROOT / "da" / "index.html").write_text(out, encoding="utf-8")
print("Wrote da/index.html")
