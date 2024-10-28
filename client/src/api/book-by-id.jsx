const getBook = async (id) => {
  try {
    const response = await fetch(`/api/books/${id}`);

    // handle non-200 responses
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    return await response.json();
  } catch (error) {
    console.error("Error Fetching Book", error);
    throw new Error("Failed to load book. Please try again later");
  }
};

const updateBook = async (id) => {};

export { getBook, updateBook };
