const endpoint = "/api/books";

const getBooks = async () => {
  try {
    const response = await fetch(endpoint);

    if (!response.ok) {
      // handle non-200 responses
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    return await response.json();
  } catch (error) {
    console.error("Error Fetching Books: ", error);
    throw new Error("Failed to load books. Please try again later.");
  }
};

const postBooks = async () => {};

export { getBooks, postBooks };
