// src/components/CandidateProfile.jsx
import React, { useEffect, useState } from "react";
import "./CandidateProfile.css";

const CandidateProfile = () => {
  const [formData, setFormData] = useState({});
  const [resume, setResume] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);

  // 🔹 Fetch candidate profile on mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          setMessage("No token found. Please log in again.");
          setLoading(false);
          return;
        }

        const res = await fetch("http://localhost:5000/candidate/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch profile");

        const data = await res.json();
        console.log("Fetched Profile:", data);

        if (data.candidate_id) {
          localStorage.setItem("candidate_id", data.candidate_id); // backup
        }

        setFormData(data); // save everything from backend
        setLoading(false);
      } catch (err) {
        console.error("Profile fetch error:", err);
        setMessage("No profile data available ");
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  // Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle file upload
  const handleFileChange = (e) => {
    setResume(e.target.files[0]);
  };

  // Submit profile update
  const handleSubmit = async (e) => {
    e.preventDefault();

    const candidateId =
      formData.candidate_id || localStorage.getItem("candidate_id");

    if (!candidateId) {
      setMessage("Candidate ID not found. Please log in again.");
      return;
    }

    const payload = new FormData();
    Object.keys(formData).forEach((key) => {
      if (formData[key] !== null && formData[key] !== undefined) {
        payload.append(key, formData[key]);
      }
    });
    if (resume) {
      payload.append("resume", resume);
    }

    try {
      const res = await fetch(
        `http://localhost:5000/candidate/form/${candidateId}/complete-profile`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: payload,
        }
      );

      const data = await res.json();

      if (res.ok) {
        setMessage("Profile updated successfully ✅");
        setEditMode(false);
        setFormData(data); // refresh with latest saved values
      } else {
        setMessage(`Error: ${data.error || "Something went wrong"}`);
      }
    } catch (err) {
      console.error("Update error:", err);
      setMessage("Network error. Try again later.");
    }
  };

  if (loading) {
    return <p>Loading profile...</p>;
  }

  return (
    <div className="candidate-profile">
      <h2>Candidate Profile</h2>
      {message && <p className="status">{message}</p>}

      {!editMode ? (
        // 🔹 READ-ONLY DISPLAY
        <div className="profile-details">
          {formData && formData.candidate_id ? (
            <div className="profile-grid">
              <p>
                <strong>Candidate ID:</strong> {formData.candidate_id}
              </p>
              <p>
                <strong>Name:</strong> {formData.name}
              </p>
              <p>
                <strong>Email:</strong> {formData.email}
              </p>
              <p>
                <strong>Password:</strong> Hidden
              </p>
              <p>
                <strong>Phone:</strong> {formData.phone}
              </p>
              <p>
                <strong>Date of Birth:</strong> {formData.date_of_birth}
              </p>
              <p>
                <strong>Gender:</strong> {formData.gender}
              </p>
              <p>
                <strong>Address:</strong> {formData.address}
              </p>
              <p>
                <strong>Aadhar Number:</strong> {formData.aadhar_number}
              </p>
              <p>
                <strong>PAN Number:</strong> {formData.pan_number}
              </p>
              <p>
                <strong>Highest Education:</strong> {formData.highest_education}
              </p>
              <p>
                <strong>Institute:</strong> {formData.institute}
              </p>
              <p>
                <strong>Passing Year:</strong> {formData.passing_year}
              </p>
              <p>
                <strong>Education Status:</strong> {formData.education_status}
              </p>
              <p>
                <strong>Skills:</strong> {formData.skills}
              </p>
              <p>
                <strong>Experience (years):</strong> {formData.experience_years}
              </p>
              <p>
                <strong>Resume:</strong>{" "}
                {formData.resume_path ? (
                  <a
                    href={`http://localhost:5000/${formData.resume_path}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    View Resume
                  </a>
                ) : (
                  "Not Uploaded"
                )}
              </p>
              <p>
                <strong>Preferred Job Role:</strong>{" "}
                {formData.preferred_job_role}
              </p>
              <p>
                <strong>Expected Salary:</strong> {formData.expected_salary}
              </p>
              <p>
                <strong>Willing to Relocate:</strong>{" "}
                {formData.willing_to_relocate ? "Yes" : "No"}
              </p>
              <p>
                <strong>LinkedIn:</strong>{" "}
                {formData.linkedin_profile ? (
                  <a
                    href={formData.linkedin_profile}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {formData.linkedin_profile}
                  </a>
                ) : (
                  "Not Provided"
                )}
              </p>
              <p>
                <strong>GitHub:</strong>{" "}
                {formData.github_portfolio ? (
                  <a
                    href={formData.github_portfolio}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {formData.github_portfolio}
                  </a>
                ) : (
                  "Not Provided"
                )}
              </p>
              <p>
                <strong>Created At:</strong> {formData.created_at}
              </p>
            </div>
          ) : (
            <p>No profile data available </p>
          )}
          <button onClick={() => setEditMode(true)}>Edit Profile</button>
        </div>
      ) : (
        // 🔹 EDIT FORM
        <form onSubmit={handleSubmit} className="profile-form">
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name || ""}
            onChange={handleChange}
          />

          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email || ""}
            onChange={handleChange}
          />

          <label>Phone:</label>
          <input
            type="text"
            name="phone"
            value={formData.phone || ""}
            onChange={handleChange}
          />

          <label>Date of Birth:</label>
          <input
            type="date"
            name="date_of_birth"
            value={formData.date_of_birth || ""}
            onChange={handleChange}
          />

          <label>Gender:</label>
          <select
            name="gender"
            value={formData.gender || ""}
            onChange={handleChange}
          >
            <option value="">Select</option>
            <option value="MALE">Male</option>
            <option value="FEMALE">Female</option>
            <option value="OTHER">Other</option>
          </select>

          <label>Address:</label>
          <input
            type="text"
            name="address"
            value={formData.address || ""}
            onChange={handleChange}
          />

          <label>Aadhar Number:</label>
          <input
            type="text"
            name="aadhar_number"
            value={formData.aadhar_number || ""}
            onChange={handleChange}
          />

          <label>PAN Number:</label>
          <input
            type="text"
            name="pan_number"
            value={formData.pan_number || ""}
            onChange={handleChange}
          />

          <label>Highest Education:</label>
          <input
            type="text"
            name="highest_education"
            value={formData.highest_education || ""}
            onChange={handleChange}
          />

          <label>Institute:</label>
          <input
            type="text"
            name="institute"
            value={formData.institute || ""}
            onChange={handleChange}
          />

          <label>Passing Year:</label>
          <input
            type="number"
            name="passing_year"
            value={formData.passing_year || ""}
            onChange={handleChange}
          />

          <label>Education Status:</label>
          <select
            name="education_status"
            value={formData.education_status || ""}
            onChange={handleChange}
          >
            <option value="">Select</option>
            <option value="pursuing">Pursuing</option>
            <option value="passed_out">Passed Out</option>
          </select>

          <label>Skills:</label>
          <input
            type="text"
            name="skills"
            value={formData.skills || ""}
            onChange={handleChange}
          />

          <label>Experience (years):</label>
          <input
            type="number"
            name="experience_years"
            value={formData.experience_years || ""}
            onChange={handleChange}
          />

          <label>Preferred Job Role:</label>
          <input
            type="text"
            name="preferred_job_role"
            value={formData.preferred_job_role || ""}
            onChange={handleChange}
          />

          <label>Expected Salary:</label>
          <input
            type="number"
            name="expected_salary"
            value={formData.expected_salary || ""}
            onChange={handleChange}
          />

          <label>Willing to Relocate:</label>
          <select
            name="willing_to_relocate"
            value={formData.willing_to_relocate || ""}
            onChange={handleChange}
          >
            <option value="">Select</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>

          <label>LinkedIn Profile:</label>
          <input
            type="url"
            name="linkedin_profile"
            value={formData.linkedin_profile || ""}
            onChange={handleChange}
          />

          <label>GitHub Portfolio:</label>
          <input
            type="url"
            name="github_portfolio"
            value={formData.github_portfolio || ""}
            onChange={handleChange}
          />

          <label>Upload Resume:</label>
          <input type="file" onChange={handleFileChange} />

          <button type="submit">Save Profile</button>
          <button type="button" onClick={() => setEditMode(false)}>
            Cancel
          </button>
        </form>
      )}
    </div>
  );
};

export default CandidateProfile;
