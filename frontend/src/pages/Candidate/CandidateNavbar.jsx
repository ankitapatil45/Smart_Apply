// src/components/Navbar.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./CandidateNavbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear authentication data (adjust according to your implementation)
    localStorage.removeItem("authToken"); // or whatever key you're using
    localStorage.removeItem("user"); // optional: clear user info
    // Redirect to login page
    navigate("/login");
  };

  return (
    <header className="navbar">
      <h1 className="logo">Smart-Apply</h1>

      <div className="nav-right">
        <nav>{/* Additional nav links can be added here if needed */}</nav>
        <button onClick={handleLogout} className="btn-primary logout-button">
          Logout
        </button>
      </div>
    </header>
  );
}
