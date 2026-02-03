import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function PlaylistPage() {
  const [playlist, setPlaylist] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const token = localStorage.getItem("aurasense_token");

  useEffect(() => {
    const preferences = localStorage.getItem("aurasense_preferences");
    if (!preferences) {
      setError("No preferences found. Please chat first.");
      setLoading(false);
      return;
    }

    const fetchPlaylist = async () => {
      try {
        const response = await fetch(`${API_URL}/playlist/create`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: preferences
        });

        if (!response.ok) {
          throw new Error("Playlist request failed");
        }

        const data = await response.json();
        setPlaylist(data.items || []);
        setQuery(data.query || "");
      } catch (err) {
        setError("Unable to generate playlist right now.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylist();
  }, [token]);

  const goBack = () => {
    navigate("/chat");
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
          <h2 className="text-xl font-semibold">Playlist</h2>
          <p className="text-xs text-slate-400">Generated for your session.</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={goBack}
            className="text-xs uppercase tracking-wide text-slate-400 hover:text-slate-200"
          >
            Back to Chat
          </button>
          <button
            onClick={logout}
            className="text-xs uppercase tracking-wide text-slate-400 hover:text-slate-200"
          >
            Logout
          </button>
        </div>
      </header>
      <main className="flex-1 overflow-y-auto px-4 py-6">
        {loading ? (
          <div className="text-slate-400">Generating playlist...</div>
        ) : null}
        {error ? (
          <div className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
            {error}
          </div>
        ) : null}
        {!loading && !error ? (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm uppercase text-slate-400">Search Query</h3>
              <p className="text-lg font-semibold mt-1">{query}</p>
            </div>
            <div className="grid gap-6 lg:grid-cols-2">
              {playlist.map((item) => (
                <div
                  key={item.video_id}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
                >
                  <h4 className="font-semibold text-slate-100 mb-2">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-400 mb-3">{item.channel_title}</p>
                  <div className="aspect-video w-full overflow-hidden rounded-xl">
                    <iframe
                      className="w-full h-full"
                      src={`https://www.youtube.com/embed/${item.video_id}`}
                      title={item.title}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
}
