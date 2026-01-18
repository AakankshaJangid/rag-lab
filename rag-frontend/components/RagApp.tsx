"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import QueryBox from "@/components/QueryBox";
import AnswerBox from "@/components/AnswerBox";
import UserMenu from "@/components/UserMenu";
import { ChatMessage } from "@/types";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  return (
    <main className="min-h-screen bg-yellow-50">
      <div className="max-w-3xl mx-auto px-4 space-y-6">
        <div className="flex items-center justify-between py-6 px-2 ">
          <h1 className="text-2xl font-bold tracking-tight text-indigo-900">RAG <span className="text-indigo-700">Lab</span></h1>
          <UserMenu />
        </div>

        <FileUpload />

        <QueryBox
          messages={messages}
          setMessages={setMessages}
          onStart={() => {}}
        />

        <AnswerBox messages={messages} />
      </div>
    </main>
  );
}
