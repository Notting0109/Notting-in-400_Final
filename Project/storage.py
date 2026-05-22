"""
Persistent storage backend for the Vinyl Album Discovery Tool.

Handles three features that survive between sessions, each in its own JSON file:
  - Favorites      -> favorites.json   (list[int]  of album IDs)
  - Listen history -> history.json     (list[dict] of {id, timestamp})
  - Personal notes -> notes.json       (dict[str, str]: album_id -> note text)

All read/write goes through small helper functions so the rest of the app
never touches the filesystem directly.
"""

import json
import os
from datetime import datetime

# All data files live next to this module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAVORITES_FILE = os.path.join(BASE_DIR, "favorites.json")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
NOTES_FILE = os.path.join(BASE_DIR, "notes.json")


# ---------- Generic helpers ----------

def _load_json(path, default):
    """Load JSON from path. If missing or malformed, return default."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Edge case: corrupted file -> fall back to default, don't crash
        return default


def _save_json(path, data):
    """Write data to path as pretty JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------- 1. Favorites ----------

def load_favorites():
    """Return the list of favorited album IDs."""
    data = _load_json(FAVORITES_FILE, [])
    # Edge case: ensure all entries are ints
    return [int(x) for x in data if isinstance(x, (int, str)) and str(x).isdigit()]


def add_favorite(album_id):
    """Add an album ID to favorites. No-op if already there."""
    favorites = load_favorites()
    if album_id not in favorites:
        favorites.append(album_id)
        _save_json(FAVORITES_FILE, favorites)
    return favorites


def remove_favorite(album_id):
    """Remove an album ID from favorites. No-op if not there."""
    favorites = load_favorites()
    if album_id in favorites:
        favorites.remove(album_id)
        _save_json(FAVORITES_FILE, favorites)
    return favorites


def is_favorite(album_id):
    """Return True if the album is in favorites."""
    return album_id in load_favorites()


# ---------- 2. Listen History ----------

def load_history():
    """Return the list of view-history entries, newest last."""
    data = _load_json(HISTORY_FILE, [])
    # Edge case: filter out malformed entries
    return [e for e in data if isinstance(e, dict) and "id" in e]


def log_view(album_id):
    """Append an album view to history with the current timestamp."""
    history = load_history()
    history.append({
        "id": album_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    })
    _save_json(HISTORY_FILE, history)
    return history


def get_recent_history(limit=10):
    """Return the most recent N history entries, newest first."""
    history = load_history()
    return list(reversed(history[-limit:]))


def clear_history():
    """Delete all history entries."""
    _save_json(HISTORY_FILE, [])


# ---------- 3. Personal Notes ----------

def load_notes():
    """Return the full notes dict {album_id_str: note_text}."""
    data = _load_json(NOTES_FILE, {})
    # Edge case: ensure dict with string keys
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def get_note(album_id):
    """Return the note for an album, or '' if none exists."""
    return load_notes().get(str(album_id), "")


def set_note(album_id, text):
    """Save (or replace) a note for an album. Empty text deletes the note."""
    notes = load_notes()
    text = text.strip()
    if text:
        notes[str(album_id)] = text
    else:
        notes.pop(str(album_id), None)
    _save_json(NOTES_FILE, notes)
    return notes


def delete_note(album_id):
    """Remove a note entirely."""
    set_note(album_id, "")
