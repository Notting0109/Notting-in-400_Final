"""
Auto-demo for the Vinyl Album Discovery Tool.
Runs through every feature without user input — useful for grading/showcase.

Run with:  python3 demo.py
"""

import time

from data import ALBUMS
from functions import (
    filter_by_mood,
    get_album_by_id,
    get_all_moods,
    render_album_card,
    render_album_detail,
)


def pause(seconds=1.2):
    time.sleep(seconds)


def banner(text):
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def demo_home_screen():
    banner("DEMO 1 — Home Screen: list available moods")
    moods = get_all_moods(ALBUMS)
    print("  What's the vibe?\n")
    for i, mood in enumerate(moods, start=1):
        print(f"    {i}. {mood}")
    pause()


def demo_mood_filter(mood):
    banner(f"DEMO 2 — Filter albums by mood: '{mood}'")
    results = filter_by_mood(ALBUMS, mood)
    print(f"  Found {len(results)} album(s):\n")
    for album in results:
        print(render_album_card(album))
    pause()
    return results


def demo_album_detail(album_id):
    banner(f"DEMO 3 — Album detail view for ID {album_id}")
    album = get_album_by_id(ALBUMS, album_id)
    print(render_album_detail(album))
    pause()


def demo_edge_cases():
    banner("DEMO 4 — Edge case handling")

    print("  (a) Filtering by a mood that doesn't exist:")
    results = filter_by_mood(ALBUMS, "nonexistent")
    print(f"      -> Returned {len(results)} albums (handled gracefully)\n")

    print("  (b) Looking up an album ID that doesn't exist:")
    missing = get_album_by_id(ALBUMS, 999)
    print(f"      -> Returned {missing} (no crash)\n")

    print("  (c) Album with missing Spotify URL — button hidden:")
    fake = {
        "id": 0,
        "title": "Test Record",
        "artist": "Test Artist",
        "year": 2024,
        "moods": ["chill"],
        "description": "Demonstrates graceful link handling.",
        "spotify_url": None,
        "amazon_url": "https://www.amazon.com/dp/TEST",
    }
    print(render_album_detail(fake))

    print("\n  (d) Case-insensitive mood matching:")
    upper = filter_by_mood(ALBUMS, "LATE NIGHT")
    lower = filter_by_mood(ALBUMS, "late night")
    print(f"      'LATE NIGHT' -> {len(upper)} albums")
    print(f"      'late night' -> {len(lower)} albums")
    print(f"      Match: {len(upper) == len(lower)}")
    pause()


def demo_stats():
    banner("DEMO 5 — Dataset stats")
    moods = get_all_moods(ALBUMS)
    print(f"  Total albums in MVP:   {len(ALBUMS)}")
    print(f"  Total unique moods:    {len(moods)}")
    print(f"  Mood tags: {', '.join(moods)}")

    print("\n  Albums per mood:")
    for mood in moods:
        count = len(filter_by_mood(ALBUMS, mood))
        bar = "#" * count
        print(f"    {mood:<12} {bar} ({count})")
    pause()


def main():
    print("\n" + "*" * 60)
    print("*  VINYL ALBUM DISCOVERY TOOL — Auto Demo".ljust(59) + "*")
    print("*" * 60)

    demo_home_screen()
    demo_mood_filter("late night")
    demo_album_detail(album_id=1)
    demo_album_detail(album_id=3)
    demo_mood_filter("hype")
    demo_edge_cases()
    demo_stats()

    banner("DEMO COMPLETE")
    print("  To use the interactive version, run:  python3 main.py\n")


if __name__ == "__main__":
    main()
