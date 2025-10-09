/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
    './static/js/**/*.js',
    './**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6', // Blue-600
        secondary: '#6b7280', // Gray-500
        accent: '#10b981', // Emerald-500
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-in': 'bounceIn 0.6s ease-out',
      }
    }
  },
  plugins: [],
}
