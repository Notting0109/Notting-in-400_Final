"""
Vinyl Album Discovery Tool — MVP CLI

Implements:
  1. Home / Mood Selector
  2. Album Browser (filtered by mood)
  3. Album Detail View
  + Backend features:
    - Favorites (saved to favorites.json)
    - Listen history (saved to history.json)
    - Personal notes (saved to notes.json)
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
from storage import (
    add_favorite,
    get_note,
    get_recent_history,
    is_favorite,
    load_favorites,
    log_view,
    remove_favorite,
    set_note,
)


# ---------- Screen 1: Home ----------

def screen_home(albums):
    """Show the main menu. Returns one of:
       - a mood string  -> go to browser
       - 'favorites'    -> go to favorites screen
       - 'history'      -> go to history screen
       - None           -> quit
    """
    print()
    print("=" * 60)
    print("  Vinyl Album Discovery Tool")
    print("=" * 60)
    print("  What's the vibe?\n")

    moods = get_all_moods(albums)
    if not moods:
        print("  No albums loaded. Check your data file.")
        return None

    for i, mood in enumerate(moods, start=1):
        print(f"    {i}. {mood}")
    print()
    print("    f. View favorites")
    print("    h. View listen history")
    print("    q. Quit\n")

    choice = input("  Pick a mood (number/name) or option: ").strip().lower()

    if choice in ("q", "quit", "exit"):
        return None
    if choice in ("f", "favorites"):
        return "favorites"
    if choice in ("h", "history"):
        return "history"

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(moods):
            return moods[idx]
        print("  Invalid number. Try again.")
        return screen_home(albums)

    if choice in moods:
        return choice

    print(f"  '{choice}' is not a valid mood. Try again.")
    return screen_home(albums)


# ---------- Screen 2: Browser ----------

def screen_browser(albums, mood):
    """Show all albums matching a mood. Returns album_id or None to go back."""
    results = filter_by_mood(albums, mood)
    favorites = load_favorites()

    print()
    print("=" * 60)
    print(f"  Showing: {mood}  ({len(results)} album{'s' if len(results) != 1 else ''})")
    print("=" * 60)

    if not results:
        print("  No albums found for this mood yet. Try another!")
        input("\n  Press Enter to go back...")
        return None

    for album in results:
        print(render_album_card(album, favorited=album["id"] in favorites))

    print("\n  Enter an album ID for details, or 'b' to go back.")
    choice = input("  > ").strip().lower()

    if choice in ("b", "back", ""):
        return None

    if not choice.isdigit():
        print("  Please enter a number.")
        input("  Press Enter to continue...")
        return screen_browser(albums, mood)

    return int(choice)


# ---------- Screen 3: Detail ----------

def screen_detail(albums, album_id):
    """Show album detail. Logs the view to history."""
    album = get_album_by_id(albums, album_id)
    print()

    if album is None:
        print("  Album not found.")
        input("\n  Press Enter to go back...")
        return

    # Log this view to history (only once per detail open)
    log_view(album_id)

    while True:
        favorited = is_favorite(album_id)
        note = get_note(album_id)
        print(render_album_detail(album, favorited=favorited, note=note))

        fav_label = "[u]nfavorite" if favorited else "[f]avorite"
        note_label = "[n]ote (edit)" if note else "[n]ote (add)"
        print(f"\n  [s] Spotify   [a] Amazon   {fav_label}   {note_label}   [b] back")
        choice = input("  > ").strip().lower()

        if choice == "s" and album.get("spotify_url"):
            webbrowser.open(album["spotify_url"])
            print("  Opened Spotify in your browser.")
            input("  Press Enter to continue...")
        elif choice == "a" and album.get("amazon_url"):
            webbrowser.open(album["amazon_url"])
            print("  Opened Amazon in your browser.")
            input("  Press Enter to continue...")
        elif choice == "f" and not favorited:
            add_favorite(album_id)
            print("  Added to favorites.")
        elif choice == "u" and favorited:
            remove_favorite(album_id)
            print("  Removed from favorites.")
        elif choice == "n":
            print(f"  Current note: {note if note else '(none)'}")
            new_note = input("  New note (leave blank to delete): ").strip()
            set_note(album_id, new_note)
            print("  Note saved.")
        else:
            return


# ---------- Screen 4: Favorites ----------

def screen_favorites(albums):
    """Show all favorited albums. Returns selected album_id or None."""
    favorites = load_favorites()
    print()
    print("=" * 60)
    print(f"  Your Favorites ({len(favorites)})")
    print("=" * 60)

    if not favorites:
        print("  You haven't favorited any albums yet.")
        input("\n  Press Enter to go back...")
        return None

    for album_id in favorites:
        album = get_album_by_id(albums, album_id)
        if album is None:
            print(f"  [{album_id}] (album missing from dataset)")
        else:
            print(render_album_card(album, favorited=True))

    print("\n  Enter an album ID for details, or 'b' to go back.")
    choice = input("  > ").strip().lower()

    if choice in ("b", "back", ""):
        return None
    if not choice.isdigit():
        return None
    return int(choice)


# ---------- Screen 5: History ----------

def screen_history(albums):
    """Show recent view history. Returns selected album_id or None."""
    history = get_recent_history(limit=15)
    print()
    print("=" * 60)
    print(f"  Recent Views ({len(history)})")
    print("=" * 60)

    if not history:
        print("  No history yet. Go discover some albums!")
        input("\n  Press Enter to go back...")
        return None

    for entry in history:
        album = get_album_by_id(albums, entry["id"])
        ts = entry.get("timestamp", "")
        if album is None:
            print(f"  {ts}   [{entry['id']}] (album missing)")
        else:
            print(f"  {ts}   [{album['id']:>2}] {album['title']} — {album['artist']}")

    print("\n  Enter an album ID for details, or 'b' to go back.")
    choice = input("  > ").strip().lower()

    if choice in ("b", "back", ""):
        return None
    if not choice.isdigit():
        return None
    return int(choice)


# ---------- Main loop ----------

def main():
    while True:
        action = screen_home(ALBUMS)
        if action is None:
            print("\n  Goodbye! Enjoy the records.\n")
            break

        if action == "favorites":
            album_id = screen_favorites(ALBUMS)
        elif action == "history":
            album_id = screen_history(ALBUMS)
        else:
            # action is a mood
            album_id = screen_browser(ALBUMS, action)

        if album_id is not None:
            screen_detail(ALBUMS, album_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Goodbye! Enjoy the records.\n")
