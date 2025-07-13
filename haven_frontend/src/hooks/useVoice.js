import { useEffect, useRef, useState } from 'react';

const useVoice = ({ onTranscription }) => {
  const mediaRecorderRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const chunks = [];

    recorder.ondataavailable = (e) => chunks.push(e.data);
    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const audioFile = new File([blob], 'recording.webm', { type: 'audio/webm' });

      const formData = new FormData();
      formData.append('audio', audioFile);

      fetch('http://localhost:8000/transcribe', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          if (data.text) onTranscription(data.text);
        });
    };

    mediaRecorderRef.current = recorder;
    recorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  return {
    startRecording,
    stopRecording,
    isRecording
  };
};

export default useVoice;
