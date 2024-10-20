import React, { useState } from "react";
import NavBar from "../components/Navbar";
import Footer from "../components/Footer";

const UserSignup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    profile_picture: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // note: add the Logic to handle form submission
    console.log("Form Data: ", formData);
  };

  return (
    <div>
      <NavBar />
      <form onSubmit={handleSubmit}>
        <h2>Signup</h2>

        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <label htmlFor="profile_picture">Profile Picture URL</label>
        <input
          type="text"
          id="profile_picture"
          value={formData.profile_picture}
          onChange={handleChange}
        />

        <button type="submit">Sign Up</button>
      </form>
      <Footer />
    </div>
  );
};

export default UserSignup;
