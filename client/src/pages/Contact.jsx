import React from "react";
import { FaGithub, FaLinkedin, FaEnvelope, FaWhatsapp } from "react-icons/fa";
import NavBar from "../components/Navbar";
import Footer from "../components/Footer";

function Contact() {
  const email = "bookswaphub@gmail.com";
  const subject = "Inquiry about Book Swap Hub";
  const body = "Hello Book Swap Hub team,\n\nI have an inquiry regarding:\n\n";

  const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(
    subject
  )}&body=${encodeURIComponent(body)}`;

  return (
    <div className="contact-container">
      <NavBar />
      <h2>Contact Book Swap Hub</h2>
      <h3>Get in Touch</h3>
      <p>
        We’d love to hear from you! If you have any questions about our book
        exchange platform, need help, or want to provide feedback, feel free to
        reach out via email:
      </p>
      <a href={mailtoLink} className="contact-email-link">
        Send Us an Email
      </a>

      <div className="social-links">
        <a href="https://github.com/bookswaphub">
          <FaGithub /> GitHub
        </a>
        <a href="https://linkedin.com/in/bookswaphub">
          <FaLinkedin /> LinkedIn
        </a>
        <a href="https://chat.whatsapp.com/HOAFbtTT34pLopYcn0oUGG">
          <FaWhatsapp /> Whatsapp
        </a>
      </div>
      <Footer />
    </div>
  );
}

export default Contact;
