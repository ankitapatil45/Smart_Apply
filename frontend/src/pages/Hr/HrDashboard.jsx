import React from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import "./HrDashboard.css";

const HrDashboard = () => {
  const location = useLocation();

  return (
    <div className="hr-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h2>HR Dashboard</h2>
      </header>

      {/* Navigation */}
      <nav className="dashboard-nav">
        <Link
          to="post-job"
          className={location.pathname.includes("post-job") ? "active" : ""}
        >
          Post Job
        </Link>
        <Link
          to="all-jobs"
          className={location.pathname.includes("all-jobs") ? "active" : ""}
        >
          All Jobs
        </Link>
      </nav>

      {/* Main content */}
      <main className="dashboard-content">
        <Outlet />
      </main>
    </div>
  );
};

export default HrDashboard;
