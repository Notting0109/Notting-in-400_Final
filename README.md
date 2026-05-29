# Vinyl Album Discovery Tool

A curated tool that helps new vinyl listeners discover what to play next — by mood, by AI text prompt, or even by uploading a photo of their surroundings. Links out to Spotify previews and Amazon listings.

## Repo layout

| Folder | Contents |
|---|---|
| `Project/` | All the application code (Flask web app + CLI). See `Project/README.md` to run it. |
| `Archive/` | Project documents — PRD v2, AI usage log, project home note. |

## Quick start

```bash
cd Project
pip3 install -r requirements.txt
python3 app.py
```

Then open http://127.0.0.1:8000

Full setup (including the optional Doubao AI features) is documented in **`Project/README.md`**.

## Features

- Browse a curated catalog of 10 albums, filterable by mood
- Album detail pages with Spotify preview + Amazon buy links
- Favorites, listen history, and personal notes (persistent)
- AI text recommendation — describe your mood, get album picks (Doubao)
- AI photo recommendation — upload a photo, the AI reads the vibe and recommends (Doubao vision)
