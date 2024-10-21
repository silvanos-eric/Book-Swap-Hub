const books = async () => {
  const response = await fetch("/api/books");

  if (!response.ok) {
    // handle non-200 responses
    const errorData = await response.json();
    throw Error(errorData.message);
  }

  return await response.json();
};

export { books };
