// src/utils/toastUtils.js
import { toast } from "react-toastify";

/**
 * Success toast notification
 * @param {string} message - Message to display in the toast
 */
export const showSuccessToast = (message) => {
  toast.success(message, {
    autoClose: 3000, // Automatically closes after 3 seconds
    position: "top-center",
  });
};

/**
 * Error toast notification
 * @param {string} message - Message to display in the toast
 */
export const showErrorToast = (message) => {
  toast.error(message, {
    autoClose: 8000, // Automatically closes after 5 seconds
    position: "top-center",
  });
};

/**
 * Info toast notification
 * @param {string} message - Message to display in the toast
 */
export const showInfoToast = (message) => {
  toast.info(message, {
    autoClose: 4000, // Automatically closes after 4 seconds
    position: "top-center",
  });
};
