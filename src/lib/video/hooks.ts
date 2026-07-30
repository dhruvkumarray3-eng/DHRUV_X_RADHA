import { useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    startRecording?: () => void;
    stopRecording?: () => void;
  }
}

export function useVideoPlayer({ durations }: { durations: Record<string, number> }) {
  const keys = Object.keys(durations);
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
  const hasRecorded = useRef(false);
  const hasStarted = useRef(false);

  useEffect(() => {
    if (!hasStarted.current) {
      hasStarted.current = true;
      window.startRecording?.();
    }

    const key = keys[currentSceneIndex];
    const duration = durations[key];

    const timer = setTimeout(() => {
      const nextIndex = currentSceneIndex + 1;
      if (nextIndex >= keys.length) {
        if (!hasRecorded.current) {
          hasRecorded.current = true;
          window.stopRecording?.();
        }
        setCurrentSceneIndex(0);
      } else {
        setCurrentSceneIndex(nextIndex);
      }
    }, duration);

    return () => clearTimeout(timer);
  }, [currentSceneIndex]);

  return { currentScene: currentSceneIndex };
}
