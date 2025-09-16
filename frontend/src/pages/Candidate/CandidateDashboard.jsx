import React from "react";
import "./CandidateDashboard.css";

// Reusable Dashboard Card Component
const DashboardCard = ({ title, description, link, buttonText }) => {
  return (
    <div className="col-md-4 mb-4">
      <div className="card h-100 shadow-sm dashboard-card">
        <div className="card-body d-flex flex-column">
          <h5 className="card-title">{title}</h5>
          <p className="card-text flex-grow-1">{description}</p>
          <a href={link} className="btn btn-primary mt-auto">
            {buttonText}
          </a>
        </div>
      </div>
    </div>
  );
};

export default function CandidateDashboard() {
  const cards = [
    {
      title: "Applied Jobs",
      description: "Track your job applications here.",
      link: "/applied-jobs",
      buttonText: "View Applied Jobs",
    },
    {
      title: "Profile",
      description: "Update your personal and professional details.",
      link: "/candidate-profile",
      buttonText: "Go to Profile",
    },
    {
      title: "Browse Jobs",
      description: "Find jobs that match your skills and preferences.",
      link: "/jobs",
      buttonText: "Search Jobs",
    },
  ];

  return (
    <div className="candidate-dashboard container mt-5">
      <h2 className="mb-5 text-center">Candidate Dashboard</h2>
      <div className="row">
        {cards.map((card, index) => (
          <DashboardCard key={index} {...card} />
        ))}
      </div>
    </div>
  );
}

