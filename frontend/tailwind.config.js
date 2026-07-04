/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#14213d',
        patrol: '#0f766e',
        signal: '#f97316',
      },
    },
  },
  plugins: [],
};
