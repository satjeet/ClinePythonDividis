/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cosmic: {
          50: '#f0f7ff',
          100: '#e0eeff',
          200: '#bae0ff',
          300: '#7cc7ff',
          400: '#36a9ff',
          500: '#0d8fff',
          600: '#006adb',
          700: '#0054b3',
          800: '#004693',
          900: '#090f20',
          950: '#002451',
        }
      },
      animation: {
        'cosmic-pulse': 'cosmic-pulse 2s ease-in-out infinite',
        'cosmic-glow': 'cosmic-glow 3s ease-in-out infinite',
        'cosmic-float': 'cosmic-float 4s ease-in-out infinite',
      },
      keyframes: {
        'cosmic-pulse': {
          '0%, 100%': { opacity: 1, transform: 'scale(1)' },
          '50%': { opacity: 0.8, transform: 'scale(1.05)' },
        },
        'cosmic-glow': {
          '0%, 100%': { boxShadow: '0 0 15px rgb(13 143 255 / 0.3)' },
          '50%': { boxShadow: '0 0 25px rgb(13 143 255 / 0.5)' },
        },
        'cosmic-float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
