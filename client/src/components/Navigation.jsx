// Navigation.jsx
import React from 'react';

export function Navigation({ categories, sources, onSelectCategory, onSelectSource, onSearchChange, searchQuery }) {
  return (
    <nav className="bg-gray-200 p-3 sticky top-16 z-10">
      <div className="flex items-center space-x-4">
        <p className="text-sm">Filter by:</p>
        <select
          onChange={onSelectCategory}
          className="px-2 py-1 border rounded text-sm focus:outline-none focus:border-blue-500"
        >
          <option value="">All Categories</option>
          {categories.map((category, index) => (
            <option key={index} value={category}>
              {category}
            </option>
          ))}
        </select>
        <select
          onChange={onSelectSource}
          className="px-2 py-1 border rounded text-sm focus:outline-none focus:border-blue-500"
        >
          <option value="">All Sources</option>
          {sources.map((source, index) => (
            <option key={index} value={source}>
              {source}
            </option>
          ))}
        </select>
        {/* Agregar el campo de búsqueda */}
        <input
          type="text"
          placeholder="Search news..."
          value={searchQuery}
          onChange={onSearchChange}
          className="px-2 py-1 border rounded text-sm focus:outline-none focus:ring focus:border-blue-300"
        />
      </div>
    </nav>
  );
}