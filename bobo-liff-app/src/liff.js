import liffSdk from '@line/liff'

const LIFF_ID = import.meta.env.VITE_LIFF_ID || ''
// Force mock even if LIFF_ID is set — useful for `npm run dev` on http://localhost,
// where real LIFF init always fails (endpoint isn't registered in LINE console).
const FORCE_MOCK = import.meta.env.VITE_LIFF_MOCK === 'true'
const USE_MOCK = FORCE_MOCK || !LIFF_ID

export async function initLiff() {
  // --- Dev fallback: mock LINE profile via sessionStorage ---
  if (USE_MOCK) {
    const stored = sessionStorage.getItem('mock_line_profile')
    if (stored) return JSON.parse(stored)
    const fallback = {
      lineUserId: 'Umockdev0000000000000000000000',
      displayName: 'Dev Tester',
      pictureUrl: '',
    }
    sessionStorage.setItem('mock_line_profile', JSON.stringify(fallback))
    return fallback
  }

  // --- Real LIFF ---
  await liffSdk.init({ liffId: LIFF_ID })

  if (!liffSdk.isLoggedIn()) {
    liffSdk.login()
    return null
  }

  const profile = await liffSdk.getProfile()
  return {
    lineUserId: profile.userId,
    displayName: profile.displayName,
    pictureUrl: profile.pictureUrl,
  }
}

export { liffSdk as liff }

// Closes the LIFF window, returning the person to the LINE chat — used by
// "back" buttons on entry screens (Login/Register) instead of navigating to
// an in-app page. In mock/dev mode there's no real window to close, so it's
// a no-op there (nothing else makes sense on localhost).
export function closeLiff() {
  if (USE_MOCK) return
  liffSdk.closeWindow()
}