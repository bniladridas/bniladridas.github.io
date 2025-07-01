import React, { useState, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, X } from 'lucide-react';

interface FullscreenPlayerProps {
  src: string;
  title: string;
  isOpen: boolean;
  onClose: () => void;
}

const FullscreenPlayer: React.FC<FullscreenPlayerProps> = ({ src, title, isOpen, onClose }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [videoRef, setVideoRef] = useState<HTMLVideoElement | null>(null);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  const togglePlay = () => {
    if (videoRef) {
      if (isPlaying) {
        videoRef.pause();
      } else {
        videoRef.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleMute = () => {
    if (videoRef) {
      videoRef.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleVideoEnd = () => {
    setIsPlaying(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
      <button
        onClick={onClose}
        className="absolute top-8 right-8 p-2 bg-white/10 backdrop-blur-sm rounded-full text-white hover:bg-white/20 transition-all duration-200 z-10"
      >
        <X size={24} />
      </button>

      <div className="relative w-full h-full flex items-center justify-center p-12">
        <video
          ref={setVideoRef}
          src={src}
          className="max-w-full max-h-full object-contain"
          muted={isMuted}
          onEnded={handleVideoEnd}
          onClick={togglePlay}
          autoPlay
          loading="lazy"
        />

        <div className="absolute inset-0 bg-black/10 opacity-0 hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
          <div className="flex items-center space-x-4">
            <button
              onClick={togglePlay}
              className="p-3 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
            >
              {isPlaying ? <Pause size={28} /> : <Play size={28} />}
            </button>
            <button
              onClick={toggleMute}
              className="p-3 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
            >
              {isMuted ? <VolumeX size={28} /> : <Volume2 size={28} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FullscreenPlayer; 