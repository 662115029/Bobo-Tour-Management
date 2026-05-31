/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  safelist: [
    { pattern: /^(bg|text)-(blue|teal|purple|amber|gray|red|orange|green|pink|violet|sky|emerald|fuchsia)-(50|100|200|500|600|700|800)$/ },
    'inline-flex', 'items-center', 'px-2.5', 'py-0.5',
    'rounded-full', 'text-xs', 'font-semibold', 'w-fit',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}