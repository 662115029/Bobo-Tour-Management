export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
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
  plugins: [],
}