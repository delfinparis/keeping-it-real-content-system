"use client";

import { useState, useEffect, useCallback } from "react";

const STORAGE_KEY = "kir-saved-episodes";

export function useSavedEpisodes() {
  const [savedEpisodes, setSavedEpisodes] = useState<number[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load saved episodes from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        setSavedEpisodes(JSON.parse(stored));
      }
    } catch (e) {
      console.error("Failed to load saved episodes:", e);
    }
    setIsLoaded(true);
  }, []);

  // Save to localStorage whenever savedEpisodes changes
  useEffect(() => {
    if (isLoaded) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(savedEpisodes));
      } catch (e) {
        console.error("Failed to save episodes:", e);
      }
    }
  }, [savedEpisodes, isLoaded]);

  const toggleSaved = useCallback((episodeId: number) => {
    setSavedEpisodes((prev) => {
      if (prev.includes(episodeId)) {
        return prev.filter((id) => id !== episodeId);
      }
      return [...prev, episodeId];
    });
  }, []);

  const isSaved = useCallback(
    (episodeId: number) => savedEpisodes.includes(episodeId),
    [savedEpisodes]
  );

  const clearAll = useCallback(() => {
    setSavedEpisodes([]);
  }, []);

  return {
    savedEpisodes,
    toggleSaved,
    isSaved,
    clearAll,
    isLoaded,
    count: savedEpisodes.length,
  };
}
