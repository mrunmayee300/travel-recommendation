/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        heading: ['"Playfair Display"', "Merriweather", "serif"],
        body: ["Inter", "Lora", "system-ui", "sans-serif"],
      },
      colors: {
        sand: "#f4ede1",
        charcoal: "#2f2a28",
        forest: "#2f5d46",
        terracotta: "#c16a4a",
        slate: "#1d2420",
        olive: "#2a332c",
        amber: "#d9a441",
      },
      boxShadow: {
        soft: "0 10px 30px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [],
};


