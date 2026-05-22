"""
Tests for the Vinyl Album Discovery Tool.
Covers all 4 test cases from PRD v2 Section 7.
Run with:  python test_app.py
"""

import os

from data import ALBUMS
from functions import (
    filter_by_mood,
    get_album_by_id,
    get_all_moods,
    render_album_detail,
)
import storage


def test_filter_by_mood():
    """Test 1: mood filter returns only albums containing the mood."""
    results = filter_by_mood(ALBUMS, "late night")
    assert len(results) > 0, "Expected at least one album tagged 'late night'"
    for album in results:
        assert "late night" in [m.lower() for m in album["moods"]], (
            f"Album {album['title']} doesn't contain 'late night'"
        )
    print("PASS  Test 1: filter_by_mood returns correct albums")


def test_get_album_by_id():
    """Test 2: album detail loads by ID."""
    album = get_album_by_id(ALBUMS, 1)
    assert album is not None, "Album id=1 should exist"
    assert album["title"] == "Kind of Blue"
    assert album["artist"] == "Miles Davis"
    print("PASS  Test 2: get_album_by_id returns correct album")


def test_missing_spotify_link():
    """Test 3: missing spotify_url doesn't break the detail render."""
    fake_album = {
        "id": 999,
        "title": "Test Album",
        "artist": "Test Artist",
        "year": 2024,
        "moods": ["chill"],
        "description": "A test album.",
        "spotify_url": None,
        "amazon_url": "https://amazon.com/test",
    }
    output = render_album_detail(fake_album)
    assert "Spotify" not in output, "Spotify button should be hidden"
    assert "Amazon" in output, "Amazon button should still show"
    print("PASS  Test 3: missing Spotify URL hides button gracefully")


def test_get_all_moods_no_duplicates():
    """Test 4: get_all_moods returns no duplicates."""
    moods = get_all_moods(ALBUMS)
    assert len(moods) == len(set(moods)), "Found duplicate moods"
    assert len(moods) > 0, "Should have at least one mood"
    print(f"PASS  Test 4: get_all_moods returned {len(moods)} unique moods")


def _use_tmp_storage():
    """Redirect storage to temp files so real user data isn't touched."""
    tmp_dir = os.path.join(os.path.dirname(__file__), ".test_tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    storage.FAVORITES_FILE = os.path.join(tmp_dir, "favorites.json")
    storage.HISTORY_FILE = os.path.join(tmp_dir, "history.json")
    storage.NOTES_FILE = os.path.join(tmp_dir, "notes.json")
    # Reset to clean slate
    for f in (storage.FAVORITES_FILE, storage.HISTORY_FILE, storage.NOTES_FILE):
        if os.path.exists(f):
            os.remove(f)


def test_favorites():
    """Test 5: favorites add/remove/check round-trip."""
    _use_tmp_storage()
    assert storage.is_favorite(1) is False
    storage.add_favorite(1)
    storage.add_favorite(3)
    storage.add_favorite(1)  # duplicate ignored
    assert storage.load_favorites() == [1, 3], "Duplicates should be ignored"
    storage.remove_favorite(1)
    assert storage.load_favorites() == [3]
    assert storage.is_favorite(3) is True
    print("PASS  Test 5: favorites add/remove/persist correctly")


def test_history():
    """Test 6: history logs views in order."""
    _use_tmp_storage()
    storage.log_view(1)
    storage.log_view(5)
    storage.log_view(2)
    recent = storage.get_recent_history(limit=10)
    # Newest first
    ids = [e["id"] for e in recent]
    assert ids == [2, 5, 1], f"Expected [2, 5, 1], got {ids}"
    assert all("timestamp" in e for e in recent), "Each entry should have a timestamp"
    print("PASS  Test 6: history logs views in correct order")


def test_notes():
    """Test 7: notes save/retrieve/delete correctly."""
    _use_tmp_storage()
    assert storage.get_note(1) == ""
    storage.set_note(1, "Best record ever")
    assert storage.get_note(1) == "Best record ever"
    storage.set_note(1, "Updated note")
    assert storage.get_note(1) == "Updated note"
    storage.set_note(1, "")  # empty deletes
    assert storage.get_note(1) == ""
    print("PASS  Test 7: notes save/update/delete correctly")


def run_all():
    print("\nRunning tests...\n")
    test_filter_by_mood()
    test_get_album_by_id()
    test_missing_spotify_link()
    test_get_all_moods_no_duplicates()
    test_favorites()
    test_history()
    test_notes()
    print("\nAll tests passed.\n")


if __name__ == "__main__":
    run_all()
