import React, { useState, useEffect } from 'react';
import { Play, Pause, Volume2, VolumeX, Maximize, X } from 'lucide-react';

interface VideoPlayerProps {
  src: string;
  title: string;
  index: number;
  onFullscreen: () => void;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ src, title, index, onFullscreen }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(true);
  const [videoRef, setVideoRef] = useState<HTMLVideoElement | null>(null);
  const [isLoading, setIsLoading] = useState(true);

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

  const handleLoadedData = () => {
    setIsLoading(false);
  };

  return (
    <div className="group relative">
      {/* Gradient Border Container */}
      <div className="relative p-[2px] rounded-lg bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        {/* Animated Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500 via-pink-500 via-cyan-500 to-purple-500 rounded-lg opacity-75 blur-sm animate-pulse"></div>
        
        {/* Video Container */}
        <div className="relative bg-gray-950 rounded-md overflow-hidden">
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center z-10">
              <div className="w-8 h-8 border-4 border-t-transparent border-white rounded-full animate-spin"></div>
            </div>
          )}
          <video
            ref={setVideoRef}
            src={src}
            className="w-full aspect-video object-cover"
            muted={isMuted}
            onEnded={handleVideoEnd}
            onClick={togglePlay}
            preload="metadata"
            playsInline
            controlsList="nodownload"
            disablePictureInPicture
            onLoadedData={handleLoadedData}
            style={isLoading ? { visibility: 'hidden' } : {}}
          />
          
          <div className="absolute inset-0 bg-black/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
            <div className="flex items-center space-x-3">
              <button
                onClick={togglePlay}
                className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
              >
                {isPlaying ? <Pause size={20} /> : <Play size={20} />}
              </button>
              <button
                onClick={toggleMute}
                className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
              >
                {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
              </button>
              <button
                onClick={onFullscreen}
                className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
              >
                <Maximize size={20} />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Fallback for non-hover state */}
      <div className="absolute inset-0 bg-gray-950 rounded-lg group-hover:opacity-0 transition-opacity duration-500">
        <video
          ref={setVideoRef}
          src={src}
          className="w-full aspect-video object-cover rounded-lg"
          muted={isMuted}
          onEnded={handleVideoEnd}
          onClick={togglePlay}
        />
        
        <div className="absolute inset-0 bg-black/10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center rounded-lg">
          <div className="flex items-center space-x-3">
            <button
              onClick={togglePlay}
              className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            </button>
            <button
              onClick={toggleMute}
              className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
            >
              {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
            </button>
            <button
              onClick={onFullscreen}
              className="p-2.5 bg-white/15 backdrop-blur-sm rounded-full text-white hover:bg-white/25 transition-all duration-200"
            >
              <Maximize size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

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
  const [isLoading, setIsLoading] = useState(true);

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

  const handleLoadedData = () => {
    setIsLoading(false);
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
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <div className="w-12 h-12 border-4 border-t-transparent border-white rounded-full animate-spin"></div>
          </div>
        )}
        <video
          ref={setVideoRef}
          src={src}
          className="max-w-full max-h-full object-contain"
          muted={isMuted}
          onEnded={handleVideoEnd}
          onClick={togglePlay}
          autoPlay
          preload="metadata"
          playsInline
          controlsList="nodownload"
          disablePictureInPicture
          onLoadedData={handleLoadedData}
          style={isLoading ? { visibility: 'hidden' } : {}}
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

function App() {
  const [fullscreenVideo, setFullscreenVideo] = useState<{ src: string; title: string } | null>(null);

  const videos = [
    {
      src: "https://github.com/user-attachments/assets/0f2bc199-7887-453f-b1d8-4d6f63b2119f",
      title: "Video One"
    },
    {
      src: "https://github.com/user-attachments/assets/bfee69dc-8da3-45df-8d55-c204b2cff619",
      title: "Video Two"
    },
    {
      src: "https://github.com/user-attachments/assets/d6fd9e83-06c9-4917-9983-ac6530d37948",
      title: "Video Three"
    }
  ];

  const socialLinks = [
    {
      name: 'GitHub',
      url: 'https://github.com/bniladridas',
      icon: () => (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
      )
    },
    {
      name: 'LinkedIn',
      url: 'https://linkedin.com/in/bniladridas',
      icon: () => (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
      )
    },
    {
      name: 'X',
      url: 'https://x.com/bniladridas',
      icon: () => (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>
        </svg>
      )
    },
    {
      name: 'Hugging Face',
      url: 'https://huggingface.co/bniladridas',
      icon: () => (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.004 5.367 18.637.001 12.017.001zm0 21.5c-5.238 0-9.513-4.262-9.513-9.513S6.779 2.487 12.017 2.487s9.513 4.275 9.513 9.513-4.275 9.5-9.513 9.5z"/>
          <path d="M8.542 8.542a1.013 1.013 0 1 1 2.025 0 1.013 1.013 0 0 1-2.025 0z"/>
          <path d="M13.433 8.542a1.013 1.013 0 1 1 2.025 0 1.013 1.013 0 0 1-2.025 0z"/>
          <path d="M12.017 18.958c-2.329 0-4.096-1.267-4.096-3.096 0-.329.267-.596.596-.596s.596.267.596.596c0 1.154 1.154 1.904 2.904 1.904s2.904-.75 2.904-1.904c0-.329.267-.596.596-.596s.596.267.596.596c0 1.829-1.767 3.096-4.096 3.096z"/>
        </svg>
      )
    }
  ];

  const openFullscreen = (src: string, title: string) => {
    setFullscreenVideo({ src, title });
  };

  const closeFullscreen = () => {
    setFullscreenVideo(null);
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="max-w-5xl mx-auto px-8 pt-16 pb-20">
        <h1 className="text-xl font-light tracking-wider text-gray-100 mb-16">
          @bniladridas
        </h1>
        
        {/* Video Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {videos.map((video, index) => (
            <VideoPlayer
              key={index}
              src={video.src}
              title={video.title}
              index={index}
              onFullscreen={() => openFullscreen(video.src, video.title)}
            />
          ))}
        </div>
      </div>

      {/* Social Links - Fixed Bottom Right */}
      <div className="fixed bottom-8 right-8 flex flex-col space-y-3">
        {socialLinks.map((link) => {
          const IconComponent = link.icon;
          return (
            <a
              key={link.name}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2.5 text-gray-500 hover:text-gray-300 transition-colors duration-200 bg-gray-900/50 backdrop-blur-sm rounded-full hover:bg-gray-800/60"
              aria-label={link.name}
            >
              <IconComponent />
            </a>
          );
        })}
      </div>

      {/* Footer */}
      <div className="max-w-5xl mx-auto px-8 pb-8">
        <p className="text-gray-600 text-xs font-light">
          © 2025
        </p>
      </div>

      {/* Fullscreen Player */}
      {fullscreenVideo && (
        <FullscreenPlayer
          src={fullscreenVideo.src}
          title={fullscreenVideo.title}
          isOpen={!!fullscreenVideo}
          onClose={closeFullscreen}
        />
      )}
    </div>
  );
}

export default App;