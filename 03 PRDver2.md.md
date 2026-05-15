# Vinyl Album Discovery Tool

## 1. PROJECT IDENTITY

**Project Name:** Vinyl Album Discovery Tool

**One-Sentence Pitch:** A curated web tool that helps new vinyl listeners discover what to play next, filtered by mood, with instant links to Spotify previews and Amazon purchase listings.

**Target User:** 16–28 year olds who recently got their first turntable and don't know where to start — they want to be told what's good, not browse endlessly.

**Why this project:** New vinyl owners are overwhelmed by choice and genre-heavy recommendation systems. This tool speaks their language (mood/vibe) instead of music theory labels.

---

## 2. FEATURE SCOPE

**Feature 1: Mood-Based Album Browser**

- What it does: Displays albums filtered by a mood tag the user selects (e.g. "late night", "hype", "focus").
- Why it matters: The core discovery mechanism — users find albums by how they feel, not by genre knowledge they don't have yet.
- User flow:
    1. User opens the app and sees available mood tags.
    2. User clicks a mood tag.
    3. All albums with that tag are displayed as cards.
- Edge cases:
    - Tag has only 1 album → still displays, no error.
    - User clicks the same tag twice → re-renders the same list (no crash).

**Feature 2: Album Detail View**

- What it does: Shows full details for a selected album — title, artist, year, mood tags, a short description, and external links.
- Why it matters: Gives users enough context to commit to a pick before they leave the app.
- User flow:
    1. User clicks an album card.
    2. Detail view opens with album info, Spotify preview link, and Amazon listing link.
- Edge cases:
    - Spotify link is missing → hide the button, don't show a broken link.
    - Amazon link is missing → same: hide button gracefully.

**Feature 3: Spotify Preview + Amazon Purchase Links**

- What it does: Each album detail page has two external link buttons — "Preview on Spotify" and "Buy on Amazon".
- Why it matters: Bridges discovery to action — the user can hear before committing, or buy immediately.
- User flow:
    1. User views album detail.
    2. Clicks "Preview on Spotify" → opens Spotify in a new tab.
    3. Clicks "Buy on Amazon" → opens Amazon product page in a new tab.
- Edge cases:
    - Link opens in same tab accidentally → ensure `target="_blank"` is set.
    - Amazon listing goes out of stock/dead URL → outside app's control; link still opens, no in-app handling needed for MVP.

---

## 3. DATA ARCHITECTURE

Each album is stored as a Python dictionary in a list (no database for MVP).

```
{  "id": 1,  "title": "Kind of Blue",  "artist": "Miles Davis",  "year": 1959,  "moods": ["late night", "focus", "chill"],  "description": "The best-selling jazz album of all time. Perfect for reading or winding down.",  "spotify_url": "https://open.spotify.com/album/1weenld61qoidwYuZ1GESA",  "amazon_url": "https://www.amazon.com/dp/B000002ADT"}
```

**Data flow:**

1. Albums are hardcoded in a `data.py` file as a list of dicts.
2. On app start, the list is loaded into memory.
3. When a user selects a mood, the app filters the list by matching mood tag.
4. When a user selects an album, the app retrieves the dict by `id` and renders the detail view.

---

## 4. FUNCTION SPECIFICATIONS

**`get_all_moods(albums)`**

- Parameters: `albums` (list of dicts)
- Returns: `list[str]` — sorted unique list of all mood tags
- Docstring: Extracts and deduplicates all mood tags from the album list.
- Edge cases: Album has empty moods list → skip it. Duplicate tags across albums → deduplicated.

**`filter_by_mood(albums, mood)`**

- Parameters: `albums` (list of dicts), `mood` (str)
- Returns: `list[dict]` — albums matching the mood
- Docstring: Returns all albums that contain the given mood tag.
- Edge cases: No albums match → returns empty list. Mood string has different casing → normalize to lowercase before comparing.

**`get_album_by_id(albums, album_id)`**

- Parameters: `albums` (list of dicts), `album_id` (int)
- Returns: `dict` or `None`
- Docstring: Finds and returns a single album by its ID.
- Edge cases: ID not found → returns `None`. Duplicate IDs in data → returns the first match.

**`render_album_card(album)`**

- Parameters: `album` (dict)
- Returns: HTML string (or Streamlit component)
- Docstring: Renders a compact card showing title, artist, year, and mood tags.
- Edge cases: Missing artist field → display "Unknown Artist". Title too long → truncate with ellipsis.

**`render_album_detail(album)`**

- Parameters: `album` (dict)
- Returns: HTML string (or Streamlit component)
- Docstring: Renders full album detail view with description and external links.
- Edge cases: `spotify_url` is None → hide Spotify button. `amazon_url` is None → hide Amazon button.

---

## 5. UI / INTERACTION DESIGN

**Screen 1 — Home / Mood Selector**

```
Vinyl Discovery Tool────────────────────────────────What's the vibe?[ late night ]  [ hype ]  [ focus ]  [ chill ]  [ morning ](Click a mood to see albums)
```

**Screen 2 — Album Browser (after selecting "late night")**

```
← Back to moods          Showing: late night (4 albums)────────────────────────────────[ Kind of Blue – Miles Davis, 1959 ][ Blue Train – John Coltrane, 1957 ][ ...                              ](Click an album for details)
```

**Screen 3 — Album Detail View**

```
← Back to results────────────────────────────────Kind of BlueMiles Davis · 1959Moods: late night, focus, chill"The best-selling jazz album of all time. Perfect for reading or winding down."[ Preview on Spotify ↗ ]   [ Buy on Amazon ↗ ]
```

---

## 6. ERROR HANDLING

|#|What can go wrong|How the app responds|
|---|---|---|
|1|User selects a mood with no albums|Show: "No albums found for this mood yet. Try another!"|
|2|Album ID not found in detail view|Show: "Album not found." — don't crash|
|3|Spotify URL is missing/null|Hide the Spotify button entirely|
|4|Amazon URL is missing/null|Hide the Amazon button entirely|
|5|Data file is empty or malformed|Show: "No albums loaded. Check your data file." on startup|

---

## 7. TESTING PLAN

**Test 1 — Mood filter works correctly**

- Input: Call `filter_by_mood(albums, "late night")`
- Expected: Returns only albums whose `moods` list contains `"late night"`
- Pass condition: Length > 0, every result contains the tag

**Test 2 — Album detail loads by ID**

- Input: Call `get_album_by_id(albums, 1)`
- Expected: Returns the dict for album with `id: 1`
- Pass condition: Returned dict has correct title and artist

**Test 3 — Missing links don't break UI**

- Input: Render detail view for an album where `spotify_url` is `None`
- Expected: No Spotify button rendered, no error thrown
- Pass condition: Page loads, Amazon button still shows if present

**Test 4 — get_all_moods returns no duplicates**

- Input: Call `get_all_moods(albums)` on full 10-album dataset
- Expected: Each mood tag appears exactly once in the result
- Pass condition: `len(result) == len(set(result))`