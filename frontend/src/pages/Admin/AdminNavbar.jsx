import React from "react";
import { useNavigate } from "react-router-dom"; // for redirecting
import "./AdminNavbar.css";

export default function AdminNavbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear authentication data (adjust if you're using cookies or context)
    localStorage.removeItem("authToken"); // or whatever key you're using
    localStorage.removeItem("user"); // optional: clear user info
    // Redirect to login page
    navigate("/login");
  };

  return (
    <header className="navbar">
      <h1 className="logo">Smart-Apply</h1>

      <div className="nav-right">
        <nav>
          <a href="/Add-Hr">Add Hr</a>
          <a href="/Manage-Hr">Manage Hr</a>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </nav>
      </div>
    </header>
  );
}
