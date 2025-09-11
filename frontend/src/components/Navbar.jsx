// src/components/Navbar.jsx
import React from "react";
import { Search, User } from "lucide-react";
import "./Navbar.css";

export default function Navbar() {
  return (
    <header className="navbar">
      <h1 className="logo">Smart-Apply</h1>

      <div className="nav-search">
        <input type="text" placeholder="Search jobs..." />
        <button>
          <Search size={16} /> Search
        </button>
      </div>

      <div className="nav-right">
        <nav>
          <a href="/homepage">Home</a>
          <a href="/jobs">Jobs</a>
          <a href="/companies">Companies</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </nav>
        <a href="/profile" className="btn-primary profile-link">
          <User size={20} /> <span>Profile</span>
        </a>
      </div>
    </header>
  );
}
