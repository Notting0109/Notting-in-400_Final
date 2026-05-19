"""
Core functions for the Vinyl Album Discovery Tool.
Each function follows the PRD v2 specification.
"""


def get_all_moods(albums):
    """Extract and deduplicate all mood tags from the album list.

    Args:
        albums: list of album dicts.

    Returns:
        Sorted unique list of mood tag strings.
    """
    moods = set()
    for album in albums:
        # Edge case: album has empty or missing moods list -> skip it
        for mood in album.get("moods", []):
            moods.add(mood.lower())
    return sorted(moods)


def filter_by_mood(albums, mood):
    """Return all albums that contain the given mood tag.

    Args:
        albums: list of album dicts.
        mood: mood string to match (case-insensitive).

    Returns:
        List of album dicts matching the mood. Empty list if none match.
    """
    # Edge case: normalize casing
    target = mood.lower().strip()
    return [
        album
        for album in albums
        if target in [m.lower() for m in album.get("moods", [])]
    ]


def get_album_by_id(albums, album_id):
    """Find and return a single album by its ID.

    Args:
        albums: list of album dicts.
        album_id: integer ID to look up.

    Returns:
        The matching album dict, or None if not found.
        If duplicate IDs exist, returns the first match.
    """
    for album in albums:
        if album.get("id") == album_id:
            return album
    return None


def render_album_card(album):
    """Render a compact one-line card showing title, artist, year, and moods.

    Args:
        album: album dict.

    Returns:
        Formatted string suitable for terminal display.
    """
    title = album.get("title", "Untitled")
    artist = album.get("artist") or "Unknown Artist"
    year = album.get("year", "")
    moods = ", ".join(album.get("moods", []))

    # Edge case: truncate long titles
    if len(title) > 40:
        title = title[:37] + "..."

    return f"  [{album['id']:>2}] {title} — {artist} ({year})   moods: {moods}"


def render_album_detail(album):
    """Render the full detail view of a single album.

    Args:
        album: album dict.

    Returns:
        Multi-line formatted string with description and external links.
    """
    title = album.get("title", "Untitled")
    artist = album.get("artist") or "Unknown Artist"
    year = album.get("year", "")
    moods = ", ".join(album.get("moods", []))
    description = album.get("description", "(no description)")

    lines = [
        "─" * 60,
        f"  {title}",
        f"  {artist} · {year}",
        f"  Moods: {moods}",
        "",
        f'  "{description}"',
        "",
    ]

    # Edge case: hide buttons if URL is missing
    spotify = album.get("spotify_url")
    amazon = album.get("amazon_url")
    if spotify:
        lines.append(f"  [S] Preview on Spotify  →  {spotify}")
    if amazon:
        lines.append(f"  [A] Buy on Amazon       →  {amazon}")
    lines.append("─" * 60)

    return "\n".join(lines)
