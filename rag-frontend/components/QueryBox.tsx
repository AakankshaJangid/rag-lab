"use client";

import { Dispatch, SetStateAction, useRef, useState } from "react";
import { queryRagStream } from "@/app/api/api";
import { ChatMessage } from "@/types";
import { useAuth } from "@clerk/nextjs";

export default function QueryBox({
  messages,
  setMessages,
  onStart,
}: {
  messages: ChatMessage[];
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  onStart: () => void;
}) {
  const [query, setQuery] = useState("");
  const [k, setK] = useState(5);
  const [loading, setLoading] = useState(false);

  const sessionId = useRef(crypto.randomUUID());

  // ✅ Clerk hook (CORRECT)
  const { getToken } = useAuth();

  const handleQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    onStart();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: query },
      { role: "assistant", content: "" },
    ]);

    try {
      // 🔑 fetch backend token once
      const token = await getToken({ template: "backend" });
      if (!token) throw new Error("No backend token. Are you logged in?");

      await queryRagStream(
        sessionId.current,
        query,
        k,
        token, // pass token directly
        (chunk) => {
          setMessages((prev) => {
            const copy = [...prev];
            copy[copy.length - 1].content += chunk;
            return copy;
          });
        },
        (sources) => {
          setMessages((prev) => {
            const copy = [...prev];
            copy[copy.length - 1].sources = sources;
            return copy;
          });
          setLoading(false);
        }
      );
    } catch (err: unknown) {
      let message = "Unknown error";

      if (err instanceof Error) {
        message = err.message;
      } else if (typeof err === "string") {
        message = err;
      }
      console.error("Query error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${message}` },
      ]);
      setLoading(false);
    }

    setQuery("");
  };

  return (
    <div className="mt-4">
      <textarea
        className="w-full border-b-2 p-2 bg-indigo-50 border-indigo-800 shadow-md focus:outline-none"
        placeholder="Ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className="flex justify-end  my-2">
        <input
          title="number"
          type="number"
          value={k}
          onChange={(e) => setK(Number(e.target.value))}
          className="w-16 bg-indigo-50 text-center border border-gray-300 rounded px-2 py-1 mr-2 focus:outline-none focus:ring-2 focus:ring-indigo-100"
        />

        <button
          onClick={handleQuery}
          disabled={loading}
          className="mx-2 px-4 py-2 bg-indigo-800 text-white rounded-full hover:bg-indigo-900 active:scale-95 transition-all duration-200"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}
