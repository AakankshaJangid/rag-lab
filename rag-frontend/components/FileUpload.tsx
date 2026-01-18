"use client";

import { useState } from "react";
import { uploadFile } from "@/app/api/api";
import { useAuth } from "@clerk/nextjs";
import Image from "next/image";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [chunkType, setChunkType] = useState("recursive");
  const [status, setStatus] = useState("");

  const { getToken } = useAuth();

  const handleUpload = async () => {
    if (!file) {
      setStatus("No file selected ❌");
      return;
    }

    setStatus("Fetching auth token...");
    try {
      // 🔑 Get backend token
      const token = await getToken({ template: "backend" });

      if (!token) {
        setStatus("No token found. Are you logged in? ❌");
        return;
      }

      console.log("Backend token:", token); // debug

      setStatus("Uploading file...");
      await uploadFile(file, chunkType, token);

      setStatus("File ingested successfully ✅");
    } catch (err: unknown) {
      let message = "Unknown error";

      if (err instanceof Error) {
        message = err.message;
      } else if (typeof err === "string") {
        message = err;
      }

      console.error("Upload error:", err);
      setStatus(`Upload failed ❌ ${message}`);
    }
  };

  return (
    <div className="flex justify-between">
      <div
        className="
      w-1/4
      h-60
      relative
    "
      >
        <Image
          src="/upload_documents1.png"
          alt="Upload documents"
          fill
          className=" object-contain absolute bottom-0 left-0 pt-6"
        />
      </div>

      <div
        className="
      w-3/4
      p-6
      bg-indigo-200
      rounded-2xl
      shadow-md
      border border-dashed border-gray-300
      hover:border-indigo-500
      transition-all duration-200 
      flex flex-col gap-4
    "
      >
        <h2 className="font-bold mb-4 text-lg">Upload Your Document</h2>
        <div className="flex justify-between mb-2">
          <input
            id="file-upload"
            title="file"
            type="file"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          {/* Custom button */}
          <div className="flex flex-col gap-1">
            <label
              htmlFor="file-upload"
              className="
            cursor-pointer
            px-4 py-2
            bg-indigo-800 text-white
            rounded
            hover:bg-indigo-900
            transition
            active:scale-95
            text-center
          "
            >
              Choose file
            </label>

            {/* Filename */}
            <span className="text-xs text-gray-600 truncate max-w-50 pl-1 italic">
              {file ? file.name : "No file chosen"}
            </span>
          </div>
          <select
            title="type"
            className="
            px-3 py-2 mb-4
    rounded
    bg-cyan-500
    text-sm
    text-white
    font-semibold
    shadow-sm
    focus:outline-none
    hover:bg-cyan-600
    transition
            "
            value={chunkType}
            onChange={(e) => setChunkType(e.target.value)}
          >
            <option value="">Chunk Type</option>
            <option value="recursive">Recursive</option>
            <option value="paragraph">Paragraph</option>
            <option value="section">Section</option>
          </select>
        </div>
        <div>
          <button
            type="button"
            onClick={handleUpload}
            className="ml-2 px-3 py-1 bg-yellow-500 text-white rounded-2xl hover:bg-yellow-600 transition active:scale-95 w-full"
          >
            Upload
          </button>
        </div>
        <p className="mt-2 text-sm">{status}</p>
      </div>
    </div>
  );
}
