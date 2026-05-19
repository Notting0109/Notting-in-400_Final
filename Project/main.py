"""
Vinyl Album Discovery Tool — MVP CLI

Entry point. Implements the three screens from PRD v2:
  1. Home / Mood Selector
  2. Album Browser
  3. Album Detail View
"""

import webbrowser

from data import ALBUMS
from functions import (
    filter_by_mood,
    get_album_by_id,
    get_all_moods,
    render_album_card,
    render_album_detail,
)


def screen_home(albums):
    """Screen 1: show available moods and let the user pick one."""
    print()
    print("=" * 60)
    print("  Vinyl Album Discovery Tool")
    print("=" * 60)
    print("  What's the vibe?\n")

    moods = get_all_moods(albums)
    # Edge case 5: data file is empty or malformed
    if not moods:
        print("  No albums loaded. Check your data file.")
        return None

    for i, mood in enumerate(moods, start=1):
        print(f"    {i}. {mood}")
    print("    q. Quit\n")

    choice = input("  Pick a mood (number or name): ").strip().lower()
    if choice in ("q", "quit", "exit"):
        return None

    # Allow numeric choice
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(moods):
            return moods[idx]
        print("  Invalid number. Try again.")
        return screen_home(albums)

    # Allow name choice
    if choice in moods:
        return choice

    print(f"  '{choice}' is not a valid mood. Try again.")
    return screen_home(albums)


def screen_browser(albums, mood):
    """Screen 2: show all albums matching the chosen mood."""
    results = filter_by_mood(albums, mood)
    print()
    print("=" * 60)
    print(f"  Showing: {mood}  ({len(results)} album{'s' if len(results) != 1 else ''})")
    print("=" * 60)

    # Edge case 1: mood has no albums
    if not results:
        print("  No albums found for this mood yet. Try another!")
        input("\n  Press Enter to go back...")
        return None

    for album in results:
        print(render_album_card(album))

    print("\n  Enter an album ID for details, or 'b' to go back.")
    choice = input("  > ").strip().lower()

    if choice in ("b", "back", ""):
        return None

    if not choice.isdigit():
        print("  Please enter a number.")
        input("  Press Enter to continue...")
        return screen_browser(albums, mood)

    return int(choice)


def screen_detail(albums, album_id):
    """Screen 3: show the chosen album's detail page."""
    album = get_album_by_id(albums, album_id)
    print()

    # Edge case 2: album ID not found
    if album is None:
        print("  Album not found.")
        input("\n  Press Enter to go back...")
        return

    print(render_album_detail(album))
    print("\n  [s] open Spotify   [a] open Amazon   [b] back")
    choice = input("  > ").strip().lower()

    if choice == "s" and album.get("spotify_url"):
        webbrowser.open(album["spotify_url"])
        print("  Opened Spotify in your browser.")
        input("  Press Enter to continue...")
        return screen_detail(albums, album_id)

    if choice == "a" and album.get("amazon_url"):
        webbrowser.open(album["amazon_url"])
        print("  Opened Amazon in your browser.")
        input("  Press Enter to continue...")
        return screen_detail(albums, album_id)

    # 'b' or anything else: go back
    return


def main():
    """Main app loop. Cycles between the three screens until the user quits."""
    while True:
        mood = screen_home(ALBUMS)
        if mood is None:
            print("\n  Goodbye! Enjoy the records.\n")
            break

        album_id = screen_browser(ALBUMS, mood)
        if album_id is not None:
            screen_detail(ALBUMS, album_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Goodbye! Enjoy the records.\n")
