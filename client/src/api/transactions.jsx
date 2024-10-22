const transactions = async (method = "GET", body = null) => {
  const headers = {
    "Content-Type": "application/json",
  };

  const options = {
    method,
    headers,
  };

  if (body) {
    options.body = JSON.stringify(body); // Attach the request body if it is a POST request
  }

  try {
    const response = await fetch("/api/transactions", options);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message);
    }

    return await response.json();
  } catch (error) {
    throw new Error(error);
  }
};

const getTransactions = async () => {
  return await transactions();
};

const postTransactions = async (userData) => {
  return await transactions("POST", userData);
};

export { getTransactions, postTransactions };
