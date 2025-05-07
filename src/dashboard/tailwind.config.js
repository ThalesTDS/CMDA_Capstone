/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./app.jsx",
    "./main.jsx",
    "./components/**/*.{js,jsx}", 
    "./hooks/**/*.{js,jsx}",
    "./contexts/**/*.{js,jsx}",
    "./services/**/*.{js,jsx}",
    "./utils/**/*.{js,jsx}",
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
        // Aquatic theme (default)
        aquatic: {
          primary: "#0072B5",
          secondary: "#00A9CE",
          accent: "#38B0DE",
          muted: "#E0F4FF",
          background: "#F0F8FF",
          foreground: "#0A4D68",
          surface: "#FFFFFF",
          border: "#D0E6F5",
          text: {
            primary: "#0A4D68",
            secondary: "#498BA6",
            muted: "#759EB3"
          }
        },
        // Neon-Futuristic theme
        neon: {
          primary: "#8A2BE2",
          secondary: "#FF00FF",
          accent: "#00FFFF",
          muted: "#181634",
          background: "#0D0C22",
          foreground: "#E0E0FF",
          surface: "#1A1A3A",
          border: "#4B0082",
          text: {
            primary: "#E0E0FF",
            secondary: "#BC9DFF",
            muted: "#7A71A5"
          }
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        "pulse-slow": {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.7 },
        },
        "float": {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        "ship-aquatic": {
          '0%': { transform: 'translateX(-100%) translateY(5px)', opacity: 0 },
          '5%': { transform: 'translateX(-80%) translateY(0px)', opacity: 1 },
          '95%': { transform: 'translateX(180%) translateY(-5px)', opacity: 1 },
          '100%': { transform: 'translateX(200%) translateY(0px)', opacity: 0 },
        },
        "ship-neon": {
          '0%': { transform: 'translateX(-100%) translateY(5px) rotate(0deg)', opacity: 0 },
          '5%': { transform: 'translateX(-80%) translateY(0px) rotate(-1deg)', opacity: 0.7 },
          '50%': { transform: 'translateX(50%) translateY(-10px) rotate(-2deg)', opacity: 1 },
          '95%': { transform: 'translateX(180%) translateY(0px) rotate(-1deg)', opacity: 0.7 },
          '100%': { transform: 'translateX(200%) translateY(0px) rotate(0deg)', opacity: 0 },
        },
        "fish-swim": {
          '0%': { transform: 'translateX(-100%) translateY(0px) scaleX(1)' },
          '49.9%': { transform: 'translateX(100%) translateY(-20px) scaleX(1)' },
          '50%': { transform: 'translateX(100%) translateY(-20px) scaleX(-1)' },
          '99.9%': { transform: 'translateX(-100%) translateY(0px) scaleX(-1)' },
          '100%': { transform: 'translateX(-100%) translateY(0px) scaleX(1)' },
        },
        "bubbles-rise": {
          '0%': { transform: 'translateY(100%)', opacity: 0.2 },
          '50%': { transform: 'translateY(50%) translateX(20px)', opacity: 0.5 },
          '100%': { transform: 'translateY(0%) translateX(0px)', opacity: 0 },
        },
        "wave": {
          '0%': { transform: 'translateX(0) translateZ(0) scaleY(1)' },
          '50%': { transform: 'translateX(-25%) translateZ(0) scaleY(0.9)' },
          '100%': { transform: 'translateX(-50%) translateZ(0) scaleY(1)' },
        },
        "wave-reverse": {
          '0%': { transform: 'translateX(0) translateZ(0) scaleY(1)' },
          '50%': { transform: 'translateX(25%) translateZ(0) scaleY(0.9)' },
          '100%': { transform: 'translateX(50%) translateZ(0) scaleY(1)' },
        },
        "glow": {
          '0%, 100%': { 'box-shadow': '0 0 10px 2px rgba(0, 255, 255, 0.2)' },
          '50%': { 'box-shadow': '0 0 25px 5px rgba(0, 255, 255, 0.5)' },
        },
        "rotate-slow": {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        "ping-slow": {
          '75%, 100%': { transform: 'scale(1.5)', opacity: 0 },
        },
        "progress-indeterminate": {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "pulse-slow": "pulse-slow 3s infinite",
        "float": "float 3s ease-in-out infinite",
        "ship-aquatic": "ship-aquatic 60s linear infinite",
        "ship-neon": "ship-neon 30s ease-in-out infinite", 
        "wave1": "wave 20s linear infinite",
        "wave2": "wave-reverse 25s linear infinite",
        "wave3": "wave 30s linear infinite",
        "glow": "glow 3s ease-in-out infinite",
        "rotate-slow": "rotate-slow 8s linear infinite",
        "ping-slow": "ping-slow 3s ease-in-out infinite",
        "progress-indeterminate": "progress-indeterminate 1.5s ease-in-out infinite",
        "fish-swim": "fish-swim 30s ease-in-out infinite",
        "bubbles-rise": "bubbles-rise 15s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}