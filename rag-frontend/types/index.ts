export interface SourceChunk {
  source: string;
  chunk_type?: string;
  page?: number;
  preview: string;
}

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: SourceChunk[];
};
