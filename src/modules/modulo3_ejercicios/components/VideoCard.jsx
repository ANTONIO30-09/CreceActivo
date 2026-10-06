import React from 'react';

const VideoCard = ({ video }) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-100 hover:shadow-lg transition-shadow">
      <div className="h-40 bg-gray-200 flex items-center justify-center">
        <span className="text-gray-500 font-medium">Video Placeholder</span>
      </div>
      <div className="p-4">
        <h3 className="font-bold text-lg text-gray-800 mb-1">{video.title}</h3>
        <div className="flex justify-between text-sm text-gray-600">
          <span>⏱ {video.duration}</span>
          <span>🔥 {video.difficulty}</span>
        </div>
      </div>
    </div>
  );
};

export default VideoCard;
