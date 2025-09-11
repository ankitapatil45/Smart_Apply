// src/pages/Login.jsx
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    role: "Candidate", // default role
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:5000/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = response.data;

      // Store token and user details (localStorage/sessionStorage as needed)
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      // Navigate based on role
      const role = data.user.role;
      if (role === "admin") {
        navigate("/admin-dashboard");
      } else if (role === "hr") {
        navigate("/hr-dashboard");
      } else if (role === "candidate") {
        navigate("/candidate-dashboard");
      } else {
        setError("Unknown role.");
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "400px" }}>
      <h3 className="text-center mb-4">Login</h3>
      <form onSubmit={handleSubmit} className="card p-4 shadow-sm">
        {error && <div className="alert alert-danger">{error}</div>}

        <div className="mb-3">
          <label>Email</label>
          <input
            type="email"
            name="email"
            className="form-control"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter email"
            required
          />
        </div>

        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            name="password"
            className="form-control"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter password"
            required
          />
        </div>

        <div className="mb-3">
          <label>Role</label>
          <select
            name="role"
            className="form-control"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="Admin">Admin</option>
            <option value="HR">HR</option>
            <option value="Candidate">Candidate</option>
          </select>
        </div>

        <button type="submit" className="btn btn-primary w-100">
          Login
        </button>

        {/* ✅ Signup link */}
        <div className="text-center mt-3">
          Don't have an account? <Link to="/SignUp">Sign Up Here</Link>
        </div>
      </form>
    </div>
  );
};

export default Login;
