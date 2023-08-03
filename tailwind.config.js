/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [ './templates/**/*.{html,php}',
              './templates/*.{html,php}',
              './node_modules/flowbite/**/*.js'],
  theme: {
    fontFamily: {
      sans: ['Lexend', 'sans-serif'],
    },
  },
  plugins: [
    require('flowbite/plugin')
    ],
}
