import React, { useState } from 'react';
import VideoCard from './VideoCard';

const VideoLibrary = () => {
  const [ageGroup, setAgeGroup] = useState('6-8');

  const videos = [
    { id: 1, title: 'Juegos de Movimiento', age: '6-8', duration: '10 min', difficulty: 'Fácil' },
    { id: 2, title: 'Coordinación Básica', age: '6-8', duration: '15 min', difficulty: 'Fácil' },
    { id: 3, title: 'Calistenia Inicial', age: '9-11', duration: '20 min', difficulty: 'Media' },
    { id: 4, title: 'Rutina de Fuerza', age: '12-14', duration: '30 min', difficulty: 'Fuerte' },
  ];

  const filteredVideos = videos.filter(video => video.age === ageGroup);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Biblioteca de Videos</h2>
      
      <div className="flex gap-4 mb-8">
        {['6-8', '9-11', '12-14'].map(age => (
          <button
            key={age}
            onClick={() => setAgeGroup(age)}
            className={\px-4 py-2 rounded-lg font-semibold transition-colors \\}
          >
            {age} años
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredVideos.map(video => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>
    </div>
  );
};

export default VideoLibrary;
