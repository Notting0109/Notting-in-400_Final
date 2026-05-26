# Vinyl Album Discovery Tool

A curated tool that helps new vinyl listeners discover what to play next, filtered by mood, with quick links to Spotify previews and Amazon listings.

Two front-ends, one backend:
- 🌐 **Web app (Flask)** — full visual UI styled after the Figma reference
- 💻 **CLI (terminal)** — same features, keyboard-driven

## Setup (one-time)

```bash
pip3 install flask
```

## Run the web app (recommended)

```bash
cd Project
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Run the CLI

```bash
cd Project
python3 main.py
```

## Run the tests

```bash
cd Project
python3 test_app.py
```

## File layout

| File | Purpose |
|---|---|
| `app.py` | Flask web app — routes for catalog, detail, favorites, history, notes |
| `main.py` | CLI entry point — same features for terminal users |
| `functions.py` | Core logic: filter by mood, lookup, render |
| `data.py` | Hardcoded list of 10 albums (MVP dataset) |
| `storage.py` | Persistent backend: favorites, history, notes (JSON files) |
| `test_app.py` | 7 tests covering both core logic and backend |
| `templates/` | Jinja2 HTML templates for the web app |
| `static/style.css` | Web styling (modeled on the Figma reference) |

## Features

### Discovery (frontend)
- Browse the full catalog of 10 curated albums
- Filter by mood: late night, chill, focus, hype, feelgood, morning
- Open a detail page for any album with full description
- One-click links to Spotify preview and Amazon listing

### Personal (persistent backend)
- ⭐ **Favorites** — star albums to come back to (`favorites.json`)
- 📜 **History** — auto-logs every album you view (`history.json`)
- 📝 **Notes** — write your own private notes per album (`notes.json`)

All three persist between sessions so you can pick up where you left off.

## How to use the web app

1. Open `http://127.0.0.1:5000`
2. Click a **mood pill** at the top of the catalog to filter
3. Click any **album** for the detail page
4. On the detail page you can:
   - Open Spotify preview / Amazon listing
   - Add to favorites (or unfavorite)
   - Write a private note (saved on submit)
5. Navigate to **favorites** or **history** from the top nav

## Data files

`favorites.json`, `history.json`, `notes.json` are created automatically on first use and live in the `Project/` folder.
