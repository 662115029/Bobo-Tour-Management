import liffSdk from '@line/liff'

const LIFF_ID = import.meta.env.VITE_LIFF_ID || ''

export async function initLiff() {
  // --- Dev fallback: no LIFF_ID or not inside LINE ---
  if (!LIFF_ID) {
    const stored = sessionStorage.getItem('dev_user')
    if (stored) return JSON.parse(stored)
    return null   // triggers login screen in App.vue
  }

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