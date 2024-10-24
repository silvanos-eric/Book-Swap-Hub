function trimText(text, maxLength) {
  // Check if the text length is already less than or equal to the desired length
  if (text.length <= maxLength) {
    return text;
  }

  // Trim the text to the max length
  let trimmedText = text.slice(0, maxLength);

  // If the last character is in the middle of a word, find the last space and trim up to that
  let lastSpaceIndex = trimmedText.lastIndexOf(" ");

  // If there is a space, trim up to the last full word; otherwise, use the trimmed text as-is
  if (lastSpaceIndex > 0) {
    trimmedText = trimmedText.slice(0, lastSpaceIndex);
  }

  // Return the trimmed text with ellipsis
  return `${trimmedText}...`;
}

export { trimText };
