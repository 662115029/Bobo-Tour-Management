import liff from '@line/liff'

const LIFF_ID = '2009771168-w9BjE7bI'

export async function initLiff() {
  try {
    await liff.init({
      liffId: LIFF_ID,
      mock: false
    })

    if (!liff.isLoggedIn()) {
      liff.login({ redirectUri: window.location.href })
      return
    }

    const profile = await liff.getProfile()

    return {
      lineUserId: profile.userId,
      displayName: profile.displayName,
      pictureUrl: profile.pictureUrl
    }

  } catch (error) {
    console.error('LIFF init failed:', error)
    throw error
  }
}

export { liff }
