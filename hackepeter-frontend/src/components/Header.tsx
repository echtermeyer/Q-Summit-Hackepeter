import React from "react";
import "./Header.css";

import logo from "../assets/logo.png";
import q_logo from "../assets/q_logo.png";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <a href="/">
          <img src={logo} alt="Empirio Logo" className="company-icon" />
        </a>
      </div>
      <div className="q-logo">
        <img src={q_logo} alt="Q Logo" className="company-icon" />
      </div>

      {/* <nav className="header-nav">
        <a href="/main" className="text-lg font-semibold nav-link">Analyze</a>
        <a href="/about" className="text-lg font-semibold nav-lin">About</a>
        <a href="/contact" className="text-lg font-semibold nav-lin">Contact</a>
      </nav> */}
    </header>
  );
};

export default Header;
