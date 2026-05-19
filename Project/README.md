# Vinyl Album Discovery Tool

A curated CLI tool that helps new vinyl listeners discover what to play next, filtered by mood, with quick links to Spotify previews and Amazon listings.

## Run it

```bash
cd Project
python3 main.py
```

## Run the tests

```bash
python3 test_app.py
```

## Files

| File | Purpose |
|---|---|
| `main.py` | CLI entry point — handles the three screens (mood selector, album browser, album detail) |
| `functions.py` | Core logic: `get_all_moods`, `filter_by_mood`, `get_album_by_id`, `render_album_card`, `render_album_detail` |
| `data.py` | Hardcoded list of 10 albums (MVP dataset) |
| `test_app.py` | Tests for all 4 cases from PRD v2 Section 7 |

## How to use

1. Run `python3 main.py`
2. Pick a mood (e.g. `late night`)
3. Pick an album by its ID
4. Press `s` to open Spotify or `a` to open Amazon in your browser
5. Press `b` to go back, or `q` from the home screen to quit
