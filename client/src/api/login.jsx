const login = async (formData) => {
  const response = await fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  // Handle non-200 responses
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Failed to log in");
  }

  return await response.json();
};

export { login };
