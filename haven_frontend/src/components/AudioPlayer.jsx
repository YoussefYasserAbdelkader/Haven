import React, { useEffect, useRef } from 'react';

const AudioPlayer = ({ audioUrl }) => {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioUrl && audioRef.current) {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
    }
  }, [audioUrl]);

  return <audio ref={audioRef} hidden />;
};

export default AudioPlayer;
