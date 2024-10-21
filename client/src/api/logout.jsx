const logout = async () => {
  const response = await fetch("/api/clear_session", {
    method: "DELETE",
  });

  if (!response.ok) {
    // Handle non-200 responses
    const errorData = await response.json();
    throw new Error(errorData.message || "An unknown error occured");
  }

  return await response.json();
};

export { logout };
