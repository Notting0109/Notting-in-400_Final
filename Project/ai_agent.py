"""
AI recommendation agent for the Vinyl Album Discovery Tool.

Uses Doubao (Volcengine Ark) via the OpenAI-compatible SDK to turn a free-text
mood / situation into 1-3 album recommendations drawn ONLY from our catalog.

Required environment variables:
    ARK_API_KEY        your Volcengine Ark API key (starts with "ark-")
    DOUBAO_MODEL_ID    the model id, e.g. "doubao-1-5-lite-32k-250115"

The key is never hardcoded — it is read from the environment at call time.
"""

import base64
import json
import os

from openai import OpenAI

# Volcengine Ark endpoint (this is public, not a secret)
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"


def _build_catalog_text(albums):
    """Format the album list into a compact numbered list for the prompt."""
    lines = []
    for a in albums:
        moods = ", ".join(a.get("moods", []))
        lines.append(
            f'- id {a["id"]}: "{a["title"]}" by {a["artist"]} ({a["year"]}) '
            f"— moods: {moods}"
        )
    return "\n".join(lines)


def _extract_json(text):
    """Pull the first JSON object out of a model response.

    Handles responses wrapped in ```json ... ``` fences or with extra prose.
    Returns a dict, or raises ValueError if nothing parseable is found.
    """
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    # Find the outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response")
    return json.loads(text[start : end + 1])


def recommend_albums(user_input, albums, max_picks=3):
    """Ask the LLM to recommend albums for a user's mood/situation.

    Args:
        user_input: free text describing the user's mood or scene.
        albums: the album list (data.ALBUMS).
        max_picks: maximum number of albums to recommend.

    Returns:
        dict with keys:
          - "ids":       list[int] of recommended album IDs (validated to exist)
          - "reasoning": str explanation from the model
          - "error":     str or None — populated if the call failed

    This function never raises; on any failure it returns an empty id list
    plus an "error" message so the web layer can show a friendly fallback.
    """
    api_key = os.environ.get("ARK_API_KEY")
    model_id = os.environ.get("DOUBAO_MODEL_ID")

    if not api_key or not model_id:
        return {
            "ids": [],
            "reasoning": "",
            "error": "AI is not configured. Set ARK_API_KEY and DOUBAO_MODEL_ID.",
        }

    if not user_input or not user_input.strip():
        return {"ids": [], "reasoning": "", "error": "Please describe your mood first."}

    valid_ids = {a["id"] for a in albums}
    catalog = _build_catalog_text(albums)

    system_prompt = (
        "You are a vinyl album recommender for a small curated catalog. "
        "You MUST only recommend albums from the catalog provided. "
        "Never invent albums that are not in the list. "
        "Respond ONLY with a JSON object, no extra prose."
    )
    user_prompt = (
        f"The user described their mood / situation:\n"
        f'"{user_input.strip()}"\n\n'
        f"Here is the full catalog:\n{catalog}\n\n"
        f"Pick {max_picks} or fewer albums that best fit. "
        f'Respond with JSON exactly like this:\n'
        f'{{"recommended_ids": [1, 5], '
        f'"reasoning": "one short friendly paragraph explaining why these fit"}}'
    )

    try:
        client = OpenAI(api_key=api_key, base_url=ARK_BASE_URL)
        resp = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        content = resp.choices[0].message.content
        data = _extract_json(content)

        # Validate ids against the real catalog
        raw_ids = data.get("recommended_ids", [])
        ids = [int(i) for i in raw_ids if int(i) in valid_ids][:max_picks]
        reasoning = str(data.get("reasoning", "")).strip()

        if not ids:
            return {
                "ids": [],
                "reasoning": reasoning,
                "error": "The AI couldn't match your mood to an album. Try rephrasing.",
            }

        return {"ids": ids, "reasoning": reasoning, "error": None}

    except Exception as exc:  # noqa: BLE001 — surface any failure gracefully
        return {
            "ids": [],
            "reasoning": "",
            "error": f"AI request failed: {exc}",
        }


def recommend_from_photo(image_bytes, mime_type, albums, max_picks=3):
    """Analyze a user-uploaded photo and recommend albums for its vibe.

    Uses a Doubao VISION model (multimodal). The model both describes the
    scene and picks albums from the catalog, in a single call.

    Args:
        image_bytes: raw bytes of the uploaded image.
        mime_type: e.g. "image/jpeg" or "image/png".
        albums: the album list (data.ALBUMS).
        max_picks: maximum number of albums to recommend.

    Returns:
        dict with keys:
          - "ids":       list[int] of recommended album IDs (validated)
          - "scene":     str — what the AI saw / the mood it inferred
          - "reasoning": str — why these albums fit
          - "error":     str or None

    Never raises — any failure is returned as an "error" string.
    """
    api_key = os.environ.get("ARK_API_KEY")
    vision_model = os.environ.get("DOUBAO_VISION_MODEL_ID")

    if not api_key or not vision_model:
        return {
            "ids": [],
            "scene": "",
            "reasoning": "",
            "error": "Photo AI is not configured. Set ARK_API_KEY and DOUBAO_VISION_MODEL_ID.",
        }

    if not image_bytes:
        return {"ids": [], "scene": "", "reasoning": "", "error": "No image was uploaded."}

    valid_ids = {a["id"] for a in albums}
    catalog = _build_catalog_text(albums)

    # Encode the image as a base64 data URL (OpenAI-compatible vision format)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64}"

    system_prompt = (
        "You are a vinyl album recommender that reads the MOOD of a photo. "
        "You MUST only recommend albums from the catalog provided. "
        "Never invent albums. Respond ONLY with a JSON object, no extra prose."
    )
    user_text = (
        "Look at this photo and infer the mood / setting / time of day. "
        f"Then pick {max_picks} or fewer albums from this catalog that match that vibe:\n\n"
        f"{catalog}\n\n"
        'Respond with JSON exactly like this:\n'
        '{"scene": "one short sentence describing what you see and the mood", '
        '"recommended_ids": [1, 5], '
        '"reasoning": "one short friendly paragraph on why these fit the photo"}'
    )

    try:
        client = OpenAI(api_key=api_key, base_url=ARK_BASE_URL)
        resp = client.chat.completions.create(
            model=vision_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_text},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                },
            ],
            temperature=0.7,
        )
        content = resp.choices[0].message.content
        data = _extract_json(content)

        raw_ids = data.get("recommended_ids", [])
        ids = [int(i) for i in raw_ids if int(i) in valid_ids][:max_picks]
        scene = str(data.get("scene", "")).strip()
        reasoning = str(data.get("reasoning", "")).strip()

        if not ids:
            return {
                "ids": [],
                "scene": scene,
                "reasoning": reasoning,
                "error": "The AI couldn't match this photo to an album. Try another.",
            }

        return {"ids": ids, "scene": scene, "reasoning": reasoning, "error": None}

    except Exception as exc:  # noqa: BLE001
        return {
            "ids": [],
            "scene": "",
            "reasoning": "",
            "error": f"Photo AI request failed: {exc}",
        }


# Quick manual test:  python3 ai_agent.py "late night studying"
if __name__ == "__main__":
    import sys

    from data import ALBUMS

    query = " ".join(sys.argv[1:]) or "late night, I want to relax and read"
    print(f"Query: {query}\n")
    result = recommend_albums(query, ALBUMS)
    print(json.dumps(result, indent=2, ensure_ascii=False))
