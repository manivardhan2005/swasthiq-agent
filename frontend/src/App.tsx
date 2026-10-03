import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import HandoffQueue from './HandoffQueue';
import ConversationDetail from './ConversationDetail';

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-[#F8F9FB] text-[#101828] font-sans">
        <Sidebar />
        <main className="flex-1 p-8">
          <Routes>
            <Route path="/" element={<HandoffQueue />} />
            <Route path="/cv_4471" element={<ConversationDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
