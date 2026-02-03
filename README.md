# AuraSense

AuraSense is an AI-powered conversational music playlist recommendation system that uses a FastAPI backend and a React + Tailwind frontend. The app provides a login screen, a chat-driven preference capture flow, and a session-only playlist rendered via YouTube embeds.

## Project Structure

```
aurasense/
│── backend/
│   ├── main.py
│   ├── auth.py
│   ├── chatbot.py
│   ├── recommender.py
│   ├── youtube_service.py
│   ├── requirements.txt
│
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── styles.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── postcss.config.js
```

## Requirements

- Python 3.10+
- Node.js 18+
- YouTube Data API v3 key
- Groq API key

## Backend Setup

```bash
cd aurasense/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export GROQ_API_KEY="your_groq_api_key"
export YOUTUBE_API_KEY="your_youtube_api_key"
export GROQ_MODEL="llama-3.1-8b-instant"

uvicorn main:app --reload
```

The backend runs on `http://localhost:8000`.

## Frontend Setup

```bash
cd aurasense/frontend
npm install

# Optional: change backend URL
export VITE_API_URL="http://localhost:8000"

npm run dev
```

The frontend runs on `http://localhost:5173`.

## Default Login

- Email: `admin@aurasense.com`
- Password: `aurasense123`

## API Endpoints

- `POST /login`
- `POST /chat`
- `POST /playlist/create`

## Notes

- No database is used. Sessions and playlists live only in memory.
- Audio files are never downloaded or hosted. The playlist uses YouTube embeds only.
- The chatbot always returns structured JSON per the required schema.
