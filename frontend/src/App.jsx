// src/App.jsx
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Navbar from "./components/Navbar";

// Pages
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import CandidateDashboard from "./pages/Candidate/CandidateDashboard";
import AdminDashboard from "./pages/Admin/AdminDashboard";
import HrDashboard from "./pages/Hr/HrDashboard";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Default route: redirect to /login */}
        <Route path="/" element={<Navigate to="/login" />} />
        {/* Public Route */}
        <Route path="/login" element={<Login />} />

        {/* Public Route */}
        <Route path="/SignUp" element={<SignUp />} />

        {/* Candidate Dashboard */}
        <Route
          path="/candidate-dashboard"
          element={
            <>
              <Navbar />
              <CandidateDashboard />
            </>
          }
        />

        {/* Admin Dashboard */}
        <Route
          path="/admin-dashboard"
          element={
            <>
              <Navbar />
              <AdminDashboard />
            </>
          }
        />

        {/* HR Dashboard */}
        <Route
          path="/hr-dashboard/*"
          element={
            <>
              <Navbar />
              <HrDashboard />
            </>
          }
        />

        {/* Fallback route */}
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
  );
}
