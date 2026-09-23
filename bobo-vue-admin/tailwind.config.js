/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  safelist: [
    { pattern: /^(bg|text)-(blue|teal|purple|amber|gray|red|orange|green|pink|violet|sky|emerald|fuchsia)-(50|100|200|500|600|700|800)$/ },
    'inline-flex', 'items-center', 'px-2.5', 'py-0.5',
    'rounded-full', 'text-meta', 'font-semibold', 'w-fit',
  ],
  theme: {
    extend: {
      fontFamily: {
        kanit: ['Kanit', 'sans-serif'],
      },
      fontSize: {
        meta: ['11px', '1.4'],     // badge, timestamp, small tag
        caption: ['13px', '1.4'],  // helper text, sub-label
        body: ['15px', '1.5'],     // main content, form, button
        header: ['18px', '1.4'],   // card/section header
        title: ['22px', '1.3'],    // page title
      },
    },
  },
}