import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./workplace/src/**/*.{js,ts,jsx,tsx,mdx}",
    "./workplace/modules/**/*.{js,ts,jsx,tsx,mdx}",
    "./workplace/shared/**/*.{js,ts,jsx,tsx}",
    "./workplace/portal/**/*.{html,js,ts}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        background: "#080C14", // Percipience Deep Space Obsidian
        foreground: "#F8FAFC",
        "percipience-dark": {
          900: "#080C14",
          800: "#0F172A",
          700: "#1E293B",
          600: "#334155",
          500: "#475569",
        },
        "cyan-glow": {
          DEFAULT: "#00E5FF",
          50: "#E0FCFF",
          100: "#B8F8FF",
          200: "#7AEEFF",
          300: "#3DE5FF",
          400: "#00E5FF",
          500: "#00B8CC",
          600: "#008A99",
          700: "#005C66",
        },
        "emerald-stream": {
          DEFAULT: "#10B981",
          light: "#34D399",
          dark: "#059669",
          glow: "rgba(16, 185, 129, 0.25)",
        },
        "amber-quarantine": {
          DEFAULT: "#F59E0B",
          light: "#FBBF24",
          dark: "#D97706",
          glow: "rgba(245, 158, 11, 0.25)",
        },
        primary: {
          DEFAULT: "#00E5FF",
          foreground: "#080C14",
        },
        secondary: {
          DEFAULT: "#6366F1", // Indigo Accent
          foreground: "#FFFFFF",
        },
        verified: {
          DEFAULT: "#10B981", // Cryptographic Green
          foreground: "#FFFFFF",
        },
        alert: {
          DEFAULT: "#F43F5E", // Poisoning Quarantine Rose
          foreground: "#FFFFFF",
        },
        muted: {
          DEFAULT: "#0F172A",
          foreground: "#94A3B8",
        },
        card: {
          DEFAULT: "rgba(15, 23, 42, 0.75)",
          foreground: "#F8FAFC",
          border: "rgba(51, 65, 85, 0.6)",
        },
        border: "rgba(51, 65, 85, 0.8)",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "-apple-system", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", "JetBrains Mono", "monospace"],
      },
      boxShadow: {
        "cyan-glow": "0 0 25px -5px rgba(0, 229, 255, 0.35)",
        "emerald-glow": "0 0 25px -5px rgba(16, 185, 129, 0.35)",
        "glass-panel": "0 8px 32px 0 rgba(0, 0, 0, 0.4)",
      },
      keyframes: {
        "pulse-glow": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.85", transform: "scale(1.02)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "pulse-glow": "pulse-glow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "shimmer": "shimmer 2.5s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
