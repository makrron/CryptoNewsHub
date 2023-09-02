import React from 'react';

export function NewsCard({ news }) {
  // Suponiendo que news.date es el timestamp de la fecha
  const date = new Date(news.date * 1000); // Multiplica por 1000 para convertirlo en milisegundos

  const formattedDate = date.toLocaleDateString('en-EEUU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <a href={news.url} target="_blank" rel="noopener noreferrer" className="block">
      <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition duration-300 transform hover:scale-105 flex">
        <div className="w-40 h-32 mr-6">
          <img
            src={news.image_url}
            alt={news.title}
            className="w-full h-full object-cover rounded shadow-md"
          />
        </div>
        <div className="flex-grow">
          <h2 className="text-xl font-semibold mb-2 hover:text-blue-600">
            {news.title}
          </h2>
          <p className="text-gray-600 mb-2">{news.summary}</p>
          <div className="flex justify-between items-center">
            <p className="text-gray-500">{news.category}</p>
            <p className="text-gray-500">{formattedDate}</p> {/* Utiliza la fecha formateada aquí */}
          </div>
        </div>
      </div>
    </a>
  );
}
