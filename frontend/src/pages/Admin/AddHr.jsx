// src/pages/Admin/AddHr.jsx
import React, { useState } from "react";
import axios from "axios";
import "./AddHr.css";

const AddHr = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("access_token"); // ✅ Retrieve JWT token from localStorage

    if (!token) {
      setMessage("Authentication token not found. Please log in again.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5000/admin/create_hr",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`, // ✅ Add Authorization header
          },
          // withCredentials is not needed when using token header
        }
      );
      setMessage(response.data.message);
      setFormData({ name: "", email: "", phone: "", password: "" });
    } catch (error) {
      console.error(error);
      setMessage(error.response?.data?.error || "Error adding HR");
    }
  };

  return (
    <div className="add-hr-container">
      <h2>Add HR</h2>
      <form onSubmit={handleSubmit} className="add-hr-form">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="phone"
          placeholder="Phone"
          value={formData.phone}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Add HR</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default AddHr;
