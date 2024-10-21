const books = async () => {
  try {
    const response = await fetch("/api/books");
    if (!response.ok) {
      // handle non-200 responses
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    return await response.json();
  } catch (error) {
    throw new Error("Failed to load books. Please try again later.");
  }
};

export { books };
