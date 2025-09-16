import React, { useEffect, useState } from "react";
import "./AllJobs.css";

const AllJobs = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch("http://127.0.0.1:5000/hr/all_jobs", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await res.json();
        setJobs(data.jobs || []);
      } catch (err) {
        console.error(err);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div className="alljobs-container">
      <h2>All Jobs</h2>
      {jobs.length === 0 ? (
        <p>No jobs found</p>
      ) : (
        <ul className="alljobs-list">
          {jobs.map((job, index) => (
            <li key={index} className="alljobs-item">
              <h3>{job.title}</h3>
              <p>{job.description}</p>
              <small>
                {job.location} • {job.status}
              </small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AllJobs;
