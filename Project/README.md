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
| `main.py` | CLI entry point — 5 screens (home, browser, detail, favorites, history) |
| `functions.py` | Core logic: filter, lookup, render |
| `data.py` | Hardcoded list of 10 albums (MVP dataset) |
| `storage.py` | Backend: persistent favorites, history, notes (JSON files) |
| `test_app.py` | 7 tests covering both core logic and backend persistence |

## Features

### Frontend (in-memory)
- Browse albums by mood
- View album detail with description
- Open Spotify preview / Amazon listing in browser

### Backend (persistent, saved to JSON files)
- **Favorites** — star albums to come back to (`favorites.json`)
- **Listen history** — auto-logs every album you view (`history.json`)
- **Personal notes** — add your own notes per album (`notes.json`)

## How to use

1. Run `python3 main.py`
2. From the Home screen:
   - Pick a **mood** to browse albums
   - Press `f` to view your **favorites**
   - Press `h` to view your **listen history**
   - Press `q` to quit
3. From the Album Detail screen:
   - `s` — open Spotify in browser
   - `a` — open Amazon in browser
   - `f` / `u` — favorite / unfavorite
   - `n` — add or edit a personal note
   - `b` — go back

## Data files

`favorites.json`, `history.json`, `notes.json` are created automatically on first use and live in the `Project/` folder.
