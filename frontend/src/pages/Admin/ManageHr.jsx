import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ManageHr.css"; // Keep CSS import

const ManageHr = () => {
  const [hrs, setHrs] = useState([]);
  const [filteredHrs, setFilteredHrs] = useState([]);
  const [message, setMessage] = useState("");
  const [editingHr, setEditingHr] = useState(null);
  const [editForm, setEditForm] = useState({
    name: "",
    phone: "",
    password: "",
  });
  const [searchTerm, setSearchTerm] = useState("");

  const fetchHrs = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://localhost:5000/admin/hrs_list", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setHrs(response.data.hrs);
      setFilteredHrs(response.data.hrs);
      setMessage("");
    } catch (error) {
      setMessage("Error fetching HRs");
    }
  };

  useEffect(() => {
    fetchHrs();
  }, []);

  const handleDelete = async (hrId) => {
    if (!window.confirm("Are you sure you want to delete this HR?")) return;
    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(`http://localhost:5000/admin/hr/${hrId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage("HR deleted successfully");
      fetchHrs();
    } catch (error) {
      setMessage("Error deleting HR");
    }
  };

  const handleEditClick = (hr) => {
    setEditingHr(hr.id);
    setEditForm({
      name: hr.name,
      phone: hr.phone,
      password: "",
    });
  };

  const handleInputChange = (e) => {
    setEditForm({
      ...editForm,
      [e.target.name]: e.target.value,
    });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");
      const payload = {
        name: editForm.name,
        phone: editForm.phone,
      };
      if (editForm.password.trim() !== "") {
        payload.password = editForm.password;
      }
      await axios.put(`http://localhost:5000/admin/hr/${editingHr}`, payload, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage("HR updated successfully");
      setEditingHr(null);
      fetchHrs();
    } catch (error) {
      setMessage("Error updating HR");
    }
  };

  const handleSearch = () => {
    const filtered = hrs.filter((hr) =>
      hr.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredHrs(filtered);
  };

  return (
    <div className="manage-hr-container">
      <h2>Manage HR</h2>
      {message && <p className="message">{message}</p>}

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search HR..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredHrs.map((hr) => (
            <tr key={hr.id}>
              <td>{hr.id}</td>
              <td>{hr.name}</td>
              <td>{hr.email}</td>
              <td>{hr.phone}</td>
              <td>
                <button onClick={() => handleEditClick(hr)}>Edit</button>
                <button onClick={() => handleDelete(hr.id)}>Delete</button>
              </td>
            </tr>
          ))}
          {filteredHrs.length === 0 && (
            <tr>
              <td colSpan="5">No HRs found.</td>
            </tr>
          )}
        </tbody>
      </table>

      {editingHr && (
        <div className="edit-form">
          <h3>Edit HR</h3>
          <form onSubmit={handleEditSubmit}>
            <input
              type="text"
              name="name"
              value={editForm.name}
              onChange={handleInputChange}
              placeholder="Name"
              required
            />
            <input
              type="text"
              name="phone"
              value={editForm.phone}
              onChange={handleInputChange}
              placeholder="Phone"
            />
            <input
              type="password"
              name="password"
              value={editForm.password}
              onChange={handleInputChange}
              placeholder="New Password (leave blank to keep current)"
            />
            <button type="submit">Save Changes</button>
            <button type="button" onClick={() => setEditingHr(null)}>
              Cancel
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ManageHr;
