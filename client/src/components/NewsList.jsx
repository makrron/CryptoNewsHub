// NewsList.jsx
import React, { useEffect, useState } from 'react';
import { getAllNews } from '../api/news.api.js';
import { NewsCard } from './NewsCard.jsx';
import { Navigation } from './Navigation.jsx';
import ReloadButton from './reloadboton.jsx'
export function NewsList() {
  const [news, setNews] = useState([]);
  const [filteredNews, setFilteredNews] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sources, setSources] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSource, setSelectedSource] = useState('');
  const [visibleNewsCount, setVisibleNewsCount] = useState(50);
  const [reachedEnd, setReachedEnd] = useState(false);
  const [searchQuery, setSearchQuery] = useState(''); // Nuevo estado para la búsqueda

  useEffect(() => {
    async function loadNews() {
      const res = await getAllNews();
      setNews(res.data);
      setFilteredNews(res.data);
      const uniqueCategories = [...new Set(res.data.map(item => item.category))];
      const sortedCategories = uniqueCategories.sort();
      setCategories(sortedCategories);
      const uniqueSources = [...new Set(res.data.map(item => item.source))];
      setSources(uniqueSources);
    }
    loadNews();
  }, []);

  useEffect(() => {
    const filtered = news.filter(item => {
      const categoryMatch = selectedCategory ? item.category === selectedCategory : true;
      const sourceMatch = selectedSource ? item.source === selectedSource : true;
      const titleMatch = item.title.toLowerCase().includes(searchQuery.toLowerCase()); // Búsqueda en el título
      const summaryMatch = item.summary.toLowerCase().includes(searchQuery.toLowerCase()); // Búsqueda en el resumen
      return categoryMatch && sourceMatch && (titleMatch || summaryMatch);
    });
    setFilteredNews(filtered);
  }, [selectedCategory, selectedSource, searchQuery, news]);

  const handleCategoryChange = event => {
    setSelectedCategory(event.target.value);
    setVisibleNewsCount(50);
    setReachedEnd(false);
  };

  const handleSourceChange = event => {
    setSelectedSource(event.target.value);
    setVisibleNewsCount(50);
    setReachedEnd(false);
  };

  const handleLoadMoreClick = () => {
    const newVisibleNewsCount = visibleNewsCount + 50;
    if (newVisibleNewsCount >= filteredNews.length) {
      setReachedEnd(true);
    }
    setVisibleNewsCount(newVisibleNewsCount);
  };

  const handleSearchChange = event => {
    const { value } = event.target;
    setSearchQuery(value);
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100">
      <div className="w-full max-w-screen-lg p-6">
        <Navigation
          categories={categories}
          sources={sources}
          onSelectCategory={handleCategoryChange}
          onSelectSource={handleSourceChange}
          onSearchChange={handleSearchChange} // Pasa la función de búsqueda
          searchQuery={searchQuery} // Pasa el estado de búsqueda
        />
        <div className="justify-center items-center mt-12">
          {filteredNews.slice(0, visibleNewsCount).map(n => (
            <div key={n.id} className="mb-6">
              <NewsCard news={n} />
            </div>
          ))}
        </div>
        <div className="flex justify-center mt-4">
          {reachedEnd ? (
            <p className="text-gray-600 text-sm mt-2">No more news to load</p>
          ) : (
            <button
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md shadow-md"
              onClick={handleLoadMoreClick}
            >
              Load more
            </button>
          )}
        </div>
      </div>
        <ReloadButton />
    </div>
  );
}