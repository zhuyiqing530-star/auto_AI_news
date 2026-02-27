"use client";

import { useEffect, useState, useCallback } from "react";

type Article = {
  id: string;
  title: string;
  url: string;
  source: string;
  relevanceScore: number;
  publishedAt: string;
  crawledAt: string;
};

export function useArticleStream() {
  const [newArticles, setNewArticles] = useState<Article[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const es = new EventSource("/api/stream");

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "connected") {
          setConnected(true);
          return;
        }
        if (Array.isArray(data)) {
          setNewArticles((prev) => {
            const ids = new Set(prev.map((a) => a.id));
            const fresh = data.filter((a: Article) => !ids.has(a.id));
            return [...fresh, ...prev].slice(0, 100);
          });
        }
      } catch {}
    };

    es.onerror = () => setConnected(false);

    return () => es.close();
  }, []);

  const clear = useCallback(() => setNewArticles([]), []);

  return { newArticles, connected, clear };
}
