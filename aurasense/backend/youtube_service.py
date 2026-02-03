import os
from typing import List

import httpx

from recommender import Song

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeService:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def search_songs(self, query: str, max_results: int = 15) -> List[Song]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "videoCategoryId": "10",
            "maxResults": max_results,
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(f"{YOUTUBE_API_URL}/search", params=params)
            response.raise_for_status()
            search_data = response.json()

        video_ids = [item["id"]["videoId"] for item in search_data.get("items", [])]
        if not video_ids:
            return []

        details_params = {
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            details_response = await client.get(
                f"{YOUTUBE_API_URL}/videos", params=details_params
            )
            details_response.raise_for_status()
            details_data = details_response.json()

        songs: List[Song] = []
        for item in details_data.get("items", []):
            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            songs.append(
                Song(
                    video_id=item["id"],
                    title=snippet.get("title", ""),
                    channel_title=snippet.get("channelTitle", ""),
                    description=snippet.get("description", ""),
                    view_count=int(stats.get("viewCount", 0)),
                    like_count=int(stats.get("likeCount", 0)),
                )
            )
        return songs


def build_query(mood: str, genres: list[str], language: str, activity: str) -> str:
    parts = [mood, language, activity] + genres
    return " ".join([part for part in parts if part]) + " music"


def get_api_key() -> str:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("YOUTUBE_API_KEY is not set")
    return api_key
