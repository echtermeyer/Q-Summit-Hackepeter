// App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home'; // Pfad zu deiner Home-Komponente
import Main from './pages/insight'; // Stelle sicher, dass der Pfad korrekt ist

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/main" element={<Main />} />
      </Routes>
    </Router>
  );
};

export default App