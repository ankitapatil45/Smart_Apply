import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import HomeNavbar from "../pages/HomeNavbar";
import "./Home.css";
import axios from "axios";

export default function Home() {
  const [jobs, setJobs] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user"); // Example method
    setIsLoggedIn(!!user);

    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get("http://localhost:5000/jobs");
      if (response.data && Array.isArray(response.data.jobs)) {
        setJobs(response.data.jobs);
      } else {
        console.error("Invalid job data format:", response.data);
        setJobs([]);
      }
    } catch (error) {
      console.error("Error fetching jobs:", error);
      setJobs([]);
    }
  };

  const handleApply = (jobId) => {
    if (!isLoggedIn) {
      if (window.confirm("You are not logged in, first sign in")) {
        navigate("/login");
      }
      return;
    }

    console.log(`Applying for job ID ${jobId}`);
  };

  return (
    <div>
      <HomeNavbar isLoggedIn={isLoggedIn} />
      <div className="jobs-container">
        <h2>Active Jobs</h2>
        {jobs.length === 0 ? (
          <p>No active jobs available.</p>
        ) : (
          <ul className="jobs-list">
            {jobs.map((job) => (
              <li key={job.id} className="job-item">
                <h3>{job.title}</h3>
                <p>{job.description}</p>
                <p>
                  <strong>Location:</strong> {job.location}
                </p>
                <button onClick={() => handleApply(job.id)}>Apply</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
