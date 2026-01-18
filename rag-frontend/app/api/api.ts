import { SourceChunk } from "@/types";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function uploadFile(file: File, chunkType: string, token: string) {
  if (!token) throw new Error("No auth token. Are you logged in?");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/ingest-file?chunk_type=${chunkType}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // always send the backend token
    },
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload failed (${res.status}): ${text}`);
  }

  return res.json();
}

export async function queryRagStream(
  sessionId: string,
  query: string,
  k: number,
  token: string, // 👈 pass token directly
  onToken: (chunk: string) => void,
  onDone: (sources: SourceChunk[]) => void
) {
  if (!token) throw new Error("No auth token. Are you logged in?");

  const res = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, // send token here
    },
    body: JSON.stringify({ session_id: sessionId, query, k }),
  });

  if (!res.body) throw new Error("No stream");

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let buffer = "";
  let sourcesBuffer = "";
  let isSource = false;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });

    if (!isSource) {
      buffer += chunk;
      const markerIndex = buffer.indexOf("[[SOURCES]]");

      if (markerIndex !== -1) {
        onToken(buffer.slice(0, markerIndex));
        sourcesBuffer += buffer.slice(markerIndex + "[[SOURCES]]".length);
        isSource = true;
        buffer = "";
      } else {
        if (buffer.trim()) {
          onToken(buffer);
        }
        buffer = "";
      }
    } else {
      sourcesBuffer += chunk;
    }
  }

  try {
    onDone(sourcesBuffer ? JSON.parse(sourcesBuffer) : []);
  } catch {
    onDone([]);
  }
}
