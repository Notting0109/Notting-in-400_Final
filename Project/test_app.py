"""
Tests for the Vinyl Album Discovery Tool.
Covers all 4 test cases from PRD v2 Section 7.
Run with:  python test_app.py
"""

from data import ALBUMS
from functions import (
    filter_by_mood,
    get_album_by_id,
    get_all_moods,
    render_album_detail,
)


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


def run_all():
    print("\nRunning tests...\n")
    test_filter_by_mood()
    test_get_album_by_id()
    test_missing_spotify_link()
    test_get_all_moods_no_duplicates()
    print("\nAll tests passed.\n")


if __name__ == "__main__":
    run_all()
