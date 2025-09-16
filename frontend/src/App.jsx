// src/App.jsx
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import CandidateNavbar from "./pages/Candidate/CandidateNavbar";
import AdminNavbar from "./pages/Admin/AdminNavbar";
import HomeNavbar from "./pages/HomeNavbar";
import Hrnavbar from "./pages/Hr/Hrnavbar";

// Pages
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Home from "./pages/Home";
import CandidateDashboard from "./pages/Candidate/CandidateDashboard";
import CandidateProfile from "./pages/Candidate/CandidateProfile";
import AdminDashboard from "./pages/Admin/AdminDashboard";
import HrDashboard from "./pages/Hr/HrDashboard";
import PostJob from "./pages/Hr/PostJob";
import AllJobs from "./pages/Hr/AllJobs";

// New pages for HR management
import AddHr from "./pages/Admin/AddHr";
import ManageHr from "./pages/Admin/ManageHr";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Default route: redirect to /login */}
        <Route path="/" element={<Navigate to="/Home" />} />

        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/SignUp" element={<SignUp />} />
        <Route path="/home" element={<Home />} />

        {/* Home  */}
        <Route
          path="/home"
          element={
            <>
              <HomeNavbar />
              <Home />
            </>
          }
        />

        {/* Candidate Dashboard */}
        <Route
          path="/candidate-dashboard"
          element={
            <>
              <CandidateNavbar />
              <CandidateDashboard />
            </>
          }
        />

        {/* Candidate Profile */}
        <Route
          path="/candidate-profile"
          element={
            <>
              <CandidateNavbar />
              <CandidateProfile />
            </>
          }
        />

        {/* Admin Dashboard */}
        <Route
          path="/admin-dashboard"
          element={
            <>
              <AdminNavbar />
              <AdminDashboard />
            </>
          }
        />

        {/* Add HR Page (Admin side) */}
        <Route
          path="/Add-Hr"
          element={
            <>
              <AdminNavbar />
              <AddHr />
            </>
          }
        />

        {/* Manage HR Page (Admin side) */}
        <Route
          path="/Manage-Hr"
          element={
            <>
              <AdminNavbar />
              <ManageHr />
            </>
          }
        />

        {/* ✅ HR Dashboard with nested routes */}
        <Route
          path="/hr-dashboard"
          element={
            <>
              <Hrnavbar />
              <HrDashboard />
            </>
          }
        >
          {/* Default redirect when just /hr-dashboard is opened */}
          <Route index element={<Navigate to="post-job" replace />} />

          {/* Nested HR routes */}
          <Route path="post-job" element={<PostJob />} />
          <Route path="all-jobs" element={<AllJobs />} />
        </Route>

        {/* Fallback route */}
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
  );
}
