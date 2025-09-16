import React from "react";
import { Link } from "react-router-dom";
import "./HomeNavbar.css";

export default function HomeNavbar({ isLoggedIn }) {
  console.log("isLoggedIn:", isLoggedIn); // Debugging line
  return (
    <div className="navbar">
      <div className="logo">Smart Apply</div>
      <div className="nav-links">
        {!isLoggedIn && (
          <>
            <Link to="/login" className="nav-button">
              Login
            </Link>
            <Link to="/signup" className="nav-button">
              Register
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
