"use client";

import { ChatMessage, SourceChunk } from "@/types";
import { useEffect, useRef, useState } from "react";

export default function AnswerBox({ messages }: { messages: ChatMessage[] }) {
  const chatRef = useRef<HTMLDivElement>(null);
  const [selectedSource, setSelectedSource] = useState<SourceChunk | null>(null);

  useEffect(() => {
    chatRef.current?.scrollTo({
      top: chatRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  return (
  <>
    <div
      ref={chatRef}
      className="mt-4 max-h-[70vh] overflow-y-auto p-4 border border-dashed border-indigo-900 rounded bg-indigo-50"
    >
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-center text-gray-500 space-y-3">
          <span className="text-3xl">👋</span>
          <h3 className="text-lg font-semibold text-gray-700">
            Hello, let’s get started
          </h3>
          <p className="text-sm max-w-md">
            Upload a document and ask your first question to see answers here.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`max-w-[80%] p-3 rounded whitespace-pre-wrap ${
                msg.role === "user"
                  ? "ml-auto bg-indigo-600 text-white"
                  : "mr-auto bg-gray-50 text-gray-900"
              }`}
            >
              {renderWithCitations(
                msg.content,
                msg.sources ?? [],
                setSelectedSource
              )}
            </div>
          ))}
        </div>
      )}
    </div>

    {selectedSource && (
      <SourceModal
        source={selectedSource}
        onClose={() => setSelectedSource(null)}
      />
    )}
  </>
);

}

function renderWithCitations(
  text: string,
  sources: SourceChunk[],
  open: (s: SourceChunk) => void
) {
  return text.split(/(\[\d+\])/g).map((part, i) => {
    const match = part.match(/\[(\d+)\]/);
    if (!match) return part;

    const idx = Number(match[1]) - 1;
    const source = sources[idx];

    return (
      <button
        key={i}
        className="text-blue-600 hover:underline mx-1"
        onClick={() => source && open(source)}
      >
        {part}
      </button>
    );
  });
}

function SourceModal({
  source,
  onClose,
}: {
  source: SourceChunk;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white p-4 rounded max-w-xl w-full">
        <h3 className="font-bold mb-2">{source.source}</h3>
        <p className="text-sm whitespace-pre-wrap">{source.preview}</p>

        <button
          onClick={onClose}
          className="mt-4 px-3 py-1 bg-gray-200 rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
}
