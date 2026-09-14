import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./workplace/modules/**/*.{js,ts,jsx,tsx,mdx}",
    "./workplace/shared/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0F172A", // Deep Slate
        foreground: "#F8FAFC",
        primary: {
          DEFAULT: "#38BDF8", // Precision Cyan
          foreground: "#0F172A",
        },
        verified: {
          DEFAULT: "#10B981", // Cryptographic Green
          foreground: "#FFFFFF",
        },
        alert: {
          DEFAULT: "#F43F5E", // Poisoning Quarantine Red
          foreground: "#FFFFFF",
        },
        muted: {
          DEFAULT: "#1E293B",
          foreground: "#94A3B8",
        },
        border: "#334155",
      },
    },
  },
  plugins: [],
};

export default config;
