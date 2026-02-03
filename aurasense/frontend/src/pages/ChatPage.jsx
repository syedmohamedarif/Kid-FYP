import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "{\n  \"intent\": \"CREATE_PLAYLIST\",\n  \"mood\": \"relaxed\",\n  \"genre\": [\"melody\"],\n  \"language\": \"English\",\n  \"activity\": \"focus\",\n  \"duration\": 30\n}"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("aurasense_token");

  const handleSend = async () => {
    if (!input.trim()) {
      return;
    }
    const nextMessages = [...messages, { role: "user", content: input }];
    setMessages(nextMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ message: input })
      });

      if (!response.ok) {
        throw new Error("Chat failed");
      }

      const data = await response.json();
      const formatted = JSON.stringify(data, null, 2);
      localStorage.setItem("aurasense_preferences", JSON.stringify(data));
      setMessages([...nextMessages, { role: "assistant", content: formatted }]);
    } catch (err) {
      setMessages([
        ...nextMessages,
        {
          role: "assistant",
          content:
            "{\n  \"intent\": \"CREATE_PLAYLIST\",\n  \"mood\": \"relaxed\",\n  \"genre\": [\"melody\"],\n  \"language\": \"English\",\n  \"activity\": \"focus\",\n  \"duration\": 30\n}"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const goToPlaylist = () => {
    navigate("/playlist");
  };

  const logout = () => {
    localStorage.removeItem("aurasense_token");
    localStorage.removeItem("aurasense_email");
    localStorage.removeItem("aurasense_preferences");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <header className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">AuraSense Chat</h2>
          <p className="text-xs text-slate-400">Describe your vibe, genre, and language.</p>
        </div>
        <button
          onClick={logout}
          className="text-xs uppercase tracking-wide text-slate-400 hover:text-slate-200"
        >
          Logout
        </button>
      </header>
      <main className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-xl rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap ${
                message.role === "user"
                  ? "bg-indigo-500 text-white rounded-br-none"
                  : "bg-slate-900 text-slate-200 border border-slate-800 rounded-bl-none"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {loading ? (
          <div className="text-slate-400 text-sm">Generating structured response...</div>
        ) : null}
      </main>
      <footer className="p-4 border-t border-slate-800 bg-slate-950">
        <div className="flex flex-col gap-3">
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe the mood, genre, language, activity, and duration..."
            className="w-full min-h-[80px] rounded-xl bg-slate-900 border border-slate-800 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleSend}
              disabled={loading}
              className="flex-1 rounded-lg bg-indigo-500 hover:bg-indigo-400 transition px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
            >
              {loading ? "Sending..." : "Send"}
            </button>
            <button
              onClick={goToPlaylist}
              className="flex-1 rounded-lg border border-indigo-400 text-indigo-200 hover:bg-indigo-500/10 transition px-4 py-2 text-sm font-semibold"
            >
              View Playlist
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
