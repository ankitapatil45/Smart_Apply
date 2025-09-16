import React, { useState, useEffect } from "react";

const AdminDashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer); // Clean up on component unmount
  }, []);

  // Generate greeting based on time of day
  const getGreeting = () => {
    const hour = currentTime.getHours();
    if (hour < 12) return "Good Morning";
    if (hour < 18) return "Good Afternoon";
    return "Good Evening";
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>{getGreeting()}, Admin!</h1>
      <p>Welcome back to your dashboard.</p>
      <p>
        Today is <strong>{currentTime.toLocaleDateString()}</strong>
      </p>
      <p>
        Current time: <strong>{currentTime.toLocaleTimeString()}</strong>
      </p>
    </div>
  );
};

export default AdminDashboard;
