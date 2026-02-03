from dataclasses import dataclass
from typing import Dict
import uuid

DEFAULT_EMAIL = "admin@aurasense.com"
DEFAULT_PASSWORD = "aurasense123"


@dataclass
class Session:
    token: str
    email: str


class SessionStore:
    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}

    def create(self, email: str) -> Session:
        token = str(uuid.uuid4())
        session = Session(token=token, email=email)
        self._sessions[token] = session
        return session

    def get(self, token: str) -> Session | None:
        return self._sessions.get(token)


session_store = SessionStore()


def authenticate(email: str, password: str) -> bool:
    return email == DEFAULT_EMAIL and password == DEFAULT_PASSWORD
