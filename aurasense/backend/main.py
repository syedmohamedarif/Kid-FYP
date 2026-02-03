import os
from typing import Dict, List

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import authenticate, session_store
from chatbot import GroqClient
from recommender import score_songs
from youtube_service import YouTubeService, build_query, get_api_key

app = FastAPI(title="AuraSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    email: str


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    intent: str
    mood: str
    genre: List[str]
    language: str
    activity: str
    duration: int


class PlaylistRequest(BaseModel):
    mood: str
    genre: List[str]
    language: str
    activity: str
    duration: int


class PlaylistResponse(BaseModel):
    query: str
    items: List[Dict[str, object]]


def require_session(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "").strip()
    if not session_store.get(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


@app.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    if not authenticate(payload.email, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session = session_store.create(payload.email)
    return LoginResponse(token=session.token, email=session.email)


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, token: str = Depends(require_session)) -> ChatResponse:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not set")
    client = GroqClient(api_key)
    response = await client.chat(payload.message)
    return ChatResponse(**response)


@app.post("/playlist/create", response_model=PlaylistResponse)
async def create_playlist(
    payload: PlaylistRequest, token: str = Depends(require_session)
) -> PlaylistResponse:
    query = build_query(payload.mood, payload.genre, payload.language, payload.activity)
    api_key = get_api_key()
    youtube = YouTubeService(api_key)
    songs = await youtube.search_songs(query=query, max_results=20)
    scored = score_songs(
        songs, payload.mood, payload.genre, payload.language, payload.activity
    )
    return PlaylistResponse(query=query, items=scored[:10])
