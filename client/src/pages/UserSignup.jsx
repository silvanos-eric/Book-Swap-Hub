import React, { useState } from "react";
import NavBar from "../components/Navbar";
import Footer from "../components/Footer";

const UserSignup = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password_confirmation: "",
    profile_picture: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((newUser) => console.log(newUser));
    alert("Account created successfully").catch((error) => {
      console.error("Error creating your account. Please try again", error);
      alert("Failed to create account. Please try again.");
    });
  };

  return (
    <div>
      <NavBar />
      <h2>Create an account</h2>
      <form id="signup" onSubmit={handleSubmit}>
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
        <label htmlFor="password_confirmation">Confirm Password</label>{" "}
        <input
          type="password"
          id="password_confirmation"
          value={formData.password_confirmation}
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
