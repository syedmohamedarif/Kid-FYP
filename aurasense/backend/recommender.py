from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Song:
    video_id: str
    title: str
    channel_title: str
    description: str
    view_count: int
    like_count: int


def score_songs(
    songs: List[Song],
    mood: str,
    genres: List[str],
    language: str,
    activity: str,
) -> List[Dict[str, object]]:
    max_views = max((song.view_count for song in songs), default=1)
    max_likes = max((song.like_count for song in songs), default=1)

    scored = []
    for song in songs:
        text = f"{song.title} {song.channel_title} {song.description}".lower()
        mood_score = 1.0 if mood.lower() in text else 0.0
        genre_score = 0.0
        for genre in genres:
            if genre.lower() in text:
                genre_score += 1.0
        genre_score = min(1.0, genre_score / max(len(genres), 1))
        language_score = 1.0 if language.lower() in text else 0.0
        activity_score = 1.0 if activity.lower() in text else 0.0
        relevance_score = max(language_score, activity_score)
        popularity_score = 0.5 * (song.view_count / max_views) + 0.5 * (
            song.like_count / max_likes
        )

        total_score = (
            0.4 * mood_score
            + 0.3 * genre_score
            + 0.2 * relevance_score
            + 0.1 * popularity_score
        )
        scored.append(
            {
                "video_id": song.video_id,
                "title": song.title,
                "channel_title": song.channel_title,
                "score": round(total_score, 4),
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored
