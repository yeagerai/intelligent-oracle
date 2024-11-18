// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: "#111111", // Dark background
        "primary-text": "#ffffff", // White text
        "secondary-text": "#999999", // Gray secondary text
        highlight: "#8e44ad", // Purple highlight color (AI-Powered Oracle)
        accent: "#f39c12", // Orange accent (Prediction markets line)
        "ticker-background": "#8e44ad", // Purple ticker background
        "ticker-text": "#ffffff", // White text for ticker
      },
      fontFamily: {
        sans: ['"Helvetica Neue"', "Arial", "sans-serif"], // Clean, sans-serif font
      },
      spacing: {
        128: "32rem", // Custom spacing value
      },
      borderRadius: {
        xl: "1.25rem", // Rounded corners for certain elements
      },
      boxShadow: {
        xl: "0 20px 25px -5px rgba(0, 0, 0, 0.5)", // Subtle shadow
      },
    },
  },
};
