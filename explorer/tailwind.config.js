/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#F1F0F3", // Light gray background
        "primary-text": "#2D2D2D", // Dark gray text
        "secondary-text": "#6A6A6A", // Slightly lighter dark gray text
        highlight: "#801EE3", // Purple highlight color
        accent: "#f39c12", // Orange accent color
        "ticker-background": "#8e44ad", // Purple ticker background
        "ticker-text": "#ffffff", // White ticker text
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
  plugins: [],
};
