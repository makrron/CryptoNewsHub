// App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { MenuBar } from './components/MenuBar.jsx';
import { NewsPage } from "./pages/NewsPage.jsx";
import { HomePage } from "./pages/HomePage.jsx";

function App() {
  return (
    <Router>
      <div className="bg-white min-h-screen">
        <MenuBar />
        <Routes>
          <Route path="/news" element={<NewsPage />} />
          <Route path="/" element={<HomePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
