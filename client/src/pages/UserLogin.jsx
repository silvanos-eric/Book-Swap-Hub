import React, { useState } from "react";
import NavBar from "../components/Navbar";
import Footer from "../components/Footer";

const UserLogin = () => {
  const [login, setLogin] = useState(false); // Tracks login status
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  // Update formData when the input fields change
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  // Submit form data and attempt login
  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((r) => {
        if (!r.ok) {
          throw new Error("Login failed: Invalid credentials");
        }
        return r.json();
      })
      .then((data) => {
        //update the state if login is successful to "true"
        setLogin(true);
        console.log("Login sucessful", data);
      })
      .catch((error) => {
        console.error("Error during login:", error);
        setError("Login failed. Please check your credentials."); //alerts user if login is unsuccessful
      });
  };

  return (
    <div>
      <NavBar />
      <h2>Welcome back, please Log in</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p className="error">{error}</p>}
      <Footer />
    </div>
  );
};

export default UserLogin;
