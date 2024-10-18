import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer>
      <p>
        <a href="#about">Book Swap Hub</a> |
        <Link to="/contact">Contact us</Link> |<a href="#faqs"> FAQs</a> |
        <a href="#terms"> Terms of Service</a>
      </p>
    </footer>
  );
};

export default Footer;
