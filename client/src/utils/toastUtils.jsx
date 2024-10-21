// src/utils/toastUtils.js
import { toast } from "react-toastify";

/**
 * Success toast notification
 * @param {string} message - Message to display in the toast
 */
export const showSuccessToast = (message) => {
  toast.success(message, {
    position: toast.POSITION.TOP_RIGHT,
    autoClose: 3000, // Automatically closes after 3 seconds
  });
};

/**
 * Error toast notification
 * @param {string} message - Message to display in the toast
 */
export const showErrorToast = (message) => {
  toast.error(message, {
    position: toast.POSITION.TOP_RIGHT,
    autoClose: 5000, // Automatically closes after 5 seconds
  });
};

/**
 * Info toast notification
 * @param {string} message - Message to display in the toast
 */
export const showInfoToast = (message) => {
  toast.info(message, {
    position: toast.POSITION.TOP_RIGHT,
    autoClose: 4000, // Automatically closes after 4 seconds
  });
};
