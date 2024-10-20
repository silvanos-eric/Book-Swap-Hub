const checkSession = async () => {
  const response = await fetch("/api/check_session");

  // Handle non-200 responses
  if (!response.ok) {
    const erorrData = await response.json();
    throw new Error(erorrData.message || "Authentication Required");
  }

  return await response.json();
};

export { checkSession };
