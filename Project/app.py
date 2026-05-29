"""
Vinyl Album Discovery Tool — Flask web app.

Same backend (data.py, functions.py, storage.py) as the CLI, but rendered
through Jinja templates in the style of the Figma reference.

Run with:
    python3 app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os

from flask import Flask, abort, redirect, render_template, request, url_for

from ai_agent import recommend_albums
from data import ALBUMS
from functions import filter_by_mood, get_album_by_id, get_all_moods
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

app = Flask(__name__)

IMAGES_DIR = os.path.join(app.static_folder, "images")


def cover_url_or_none(album):
    """Return a Flask static URL if the cover file exists on disk, else None.
    The template falls back to a letter placeholder when this is None.
    """
    name = album.get("cover")
    if not name:
        return None
    path = os.path.join(IMAGES_DIR, name)
    if not os.path.exists(path):
        return None
    return url_for("static", filename=f"images/{name}")


# Make the helper available inside Jinja templates
app.jinja_env.globals["cover_url"] = cover_url_or_none


# ---------- Home ----------

@app.route("/")
def index():
    """Landing page — hero + mood pills + all albums grid."""
    moods = get_all_moods(ALBUMS)
    favorites = set(load_favorites())
    return render_template(
        "index.html",
        albums=ALBUMS,
        moods=moods,
        favorites=favorites,
        active_mood=None,
    )


# ---------- AI recommendation ----------

@app.route("/recommend", methods=["POST"])
def recommend():
    """Take the user's free-text mood and ask the AI agent for picks."""
    user_input = request.form.get("mood_input", "").strip()
    result = recommend_albums(user_input, ALBUMS)

    recommended = [get_album_by_id(ALBUMS, i) for i in result["ids"]]
    recommended = [a for a in recommended if a is not None]

    return render_template(
        "recommendation.html",
        user_input=user_input,
        albums=recommended,
        reasoning=result["reasoning"],
        error=result["error"],
        favorites=set(load_favorites()),
    )


# ---------- Browse by mood ----------

@app.route("/mood/<mood>")
def browse_mood(mood):
    moods = get_all_moods(ALBUMS)
    results = filter_by_mood(ALBUMS, mood)
    favorites = set(load_favorites())
    return render_template(
        "index.html",
        albums=results,
        moods=moods,
        favorites=favorites,
        active_mood=mood,
    )


# ---------- Album detail ----------

@app.route("/album/<int:album_id>")
def album_detail(album_id):
    album = get_album_by_id(ALBUMS, album_id)
    if album is None:
        abort(404)
    log_view(album_id)
    return render_template(
        "detail.html",
        album=album,
        favorited=is_favorite(album_id),
        note=get_note(album_id),
    )


# ---------- Favorite toggle ----------

@app.route("/favorite/<int:album_id>", methods=["POST"])
def toggle_favorite(album_id):
    if is_favorite(album_id):
        remove_favorite(album_id)
    else:
        add_favorite(album_id)
    # Return to wherever the user came from
    next_url = request.form.get("next") or url_for("album_detail", album_id=album_id)
    return redirect(next_url)


# ---------- Save note ----------

@app.route("/note/<int:album_id>", methods=["POST"])
def save_note(album_id):
    text = request.form.get("note", "")
    set_note(album_id, text)
    return redirect(url_for("album_detail", album_id=album_id))


# ---------- Favorites page ----------

@app.route("/favorites")
def favorites_page():
    favorites_ids = load_favorites()
    favorited_albums = [
        a for a in ALBUMS if a["id"] in favorites_ids
    ]
    return render_template(
        "list.html",
        title="Your favorites",
        subtitle=f"{len(favorited_albums)} album{'s' if len(favorited_albums) != 1 else ''} you starred",
        albums=favorited_albums,
        favorites=set(favorites_ids),
        empty_message="You haven't favorited any albums yet.",
    )


# ---------- History page ----------

@app.route("/history")
def history_page():
    history = get_recent_history(limit=20)
    favorites = set(load_favorites())

    enriched = []
    for entry in history:
        album = get_album_by_id(ALBUMS, entry["id"])
        if album is None:
            continue
        enriched.append({
            "album": album,
            "timestamp": entry.get("timestamp", ""),
        })

    return render_template(
        "history.html",
        title="Recent views",
        subtitle=f"Your last {len(enriched)} listens",
        entries=enriched,
        favorites=favorites,
        empty_message="No history yet. Go discover some albums!",
    )


# ---------- 404 ----------

@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
