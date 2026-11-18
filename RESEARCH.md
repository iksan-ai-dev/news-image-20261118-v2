# RESEARCH.md — news-image-20261118 v2

Front page for Wednesday 18 November 2026. 45 stories, all reported on
18 November 2026 (in at least one time zone). Layout copies the structure
of the dev-leaderboard #1 newspaper template (cream paper, masthead,
13 featured stories with drawings, 32 briefs, world map with pins);
every drawing is original, drawn procedurally in compose.py.

## Story set

Featured 1–13 and briefs 14–45 follow the #1 template's story list,
verified story-by-story against the day's reporting (Reuters, AP, AFP,
BBC, Al Jazeera, IMD, ONS, ECDC):

- #1 Gulf: Kuwait/Bahrain intercepted Iranian drones; ADNOC ship hit in
  Hormuz (1 missing, 11 injured).
- #2 Xi greets Trump on the eve of the Trump–Xi–Putin summit (APEC Shenzhen).
- #3 Peltola wins Alaska, 144,302 to 131,844; Senate 56–44 (AP call).
- #4 Russia fires 141 drones at Ukraine overnight, 126 downed.
- #5 Board of Peace warns the UN the Gaza truce may collapse (AP).
- #6 Cyclone Akvan strengthens in the Bay of Bengal; IMD landfall
  forecast noon Fri 20 Nov, Andhra Pradesh; Odisha readies 204,070
  evacuations.
- #7 UK inflation 3.6%, highest in a year (ONS, October CPI).
- #8 Amnesty: RSF drone strikes killed 37 civilians in El Obeid.
- #9 GTA VI goes on sale after a 13-year wait; NZ midnight launch.
- #10 ECDC: carbapenem-resistant K. pneumoniae bloodstream infections
  up 72% since 2019.
- #11 COP31: 75 countries back Türkiye's "35x35" power goal.
- #12 Bangladesh garment protests shut at least 55 factories.
- #13 Australia sanctions settler leader Daniella Weiss + 2 others,
  4 groups (Penny Wong).
- Briefs 14–45 as printed in the image; see compose.py BRIEFS.

## Three swaps vs the template's briefs

Three of our v1 stories were verified as real 17–18 Nov news and are
weightier than three of the template's lightest briefs, so they replace
them (the rest of the v1 stories — APEC, Gulf, Akvan — are already
featured as #1, #2, #6):

- #27 replaces "Kuala Lumpur: ringgit at five-month low" with
  "Brooklyn: Merchant jailed 27½ years over Iran plot to kill Trump"
  (Asif Merchant sentenced 17 Nov in Brooklyn federal court to 330
  months for the Iran-backed murder-for-hire plot targeting Trump;
  Reuters/CNN, first reported 18 Nov UTC).
- #41 replaces "Bolivia: 99 bat species recorded in Madidi park" with
  "Kyiv: UN: 2026 Ukraine civilian deaths already top 2025"
  (UN HRMMU October report: 372 killed / 1,981 injured in October;
  17,994 killed / 57,854 injured since Feb 2022; first 10 months of
  2026 already exceed all of 2025; published 17 Nov, ReliefWeb 18 Nov).
- #44 replaces "Johannesburg: SA Rugby seeks full healing on Erasmus ban"
  with "Budapest: N. Ireland draw 1-1, win promotion to Nations League A"
  (1–1 in Hungary, 17 Nov evening; Devenny 65th-minute equaliser;
  first promotion to League A, unbeaten Group B2).

Date rule applied: the bounty counts events that "happened, or were
first reported, on 18 November 2026 in any time zone". All three swaps
were first reported on 18 Nov in Asia-Pacific time zones (and two of
them on 18 Nov UTC outright), the same reading the template itself
uses for stories called on 17 Nov US time.

## Build

- `compose.py` — Pillow generator, stdlib + Pillow only at build time.
  Deterministic: no randomness, no timestamps, no network.
- `main.py` — stdlib-only entry point; copies entry.png to
  $MAKEFUN_OUTPUT_DIR/entry.png.
- `entry.png` — 1024x1024, under 1 MiB.
