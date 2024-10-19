import React from "react";
import {
  FaGithub,
  FaLinkedin,
  FaEnvelope,
  FaWhatsapp,
  FaPhone,
} from "react-icons/fa";
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
      <section className="feedback_form">
        <h2>Talk To Us</h2>
        <label htmlFor="First Name">First Name</label>
        <input type="text" name="first name" id="firstname" />
        <label htmlFor="First Name">Last Name</label>
        <input type="text" name="last name" id="lastname" />
        <label htmlFor="email">Email</label>
        <input type="email" name="email" id="email" />
        <label htmlFor="Subject">Subject</label>
        <input type="text" name="subject" id="subject" />
        <textarea placeholder="Type your message here"></textarea>
        <button>Send</button>
      </section>
      <section>
        <h2>Connect With Us</h2>
        <p>Let's connect via our social media:</p>

        <ul className="social-links">
          <li>
            <a
              href="https://linkedin.com/in/bookswaphub"
              aria-label="Visit OurLinkedIn profile"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaLinkedin /> LinkedIn
            </a>
          </li>
          <li>
            <a
              href="https://chat.whatsapp.com/HOAFbtTT34pLopYcn0oUGG"
              aria-label="Join our Whatsapp group"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaWhatsapp /> Whatsapp
            </a>
          </li>
          <li>
            <a
              href="https://github.com/bookswaphub"
              aria-label="Visit our GitHub page"
              target="_blank"
              rel="noopener noreferrer"
            >
              <FaGithub /> GitHub
            </a>
          </li>
          <li>
            <a
              href={mailtoLink}
              className="contact-email-link"
              aria-label="Send us an email"
            >
              <FaEnvelope /> Email Us
            </a>
          </li>
          <li>
            <a
              href="tel:+254750923269"
              aria-label="Call or Text Us at +254750923269"
            >
              <FaPhone /> Call/Text
            </a>
          </li>
        </ul>
      </section>
      <Footer />
    </div>
  );
}

export default Contact;
