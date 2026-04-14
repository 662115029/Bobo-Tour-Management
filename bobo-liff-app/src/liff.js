import liff from '@line/liff'
import { LiffMockPlugin } from '@line/liff-mock'
import { mockProfile } from './mockData.js'

const LIFF_ID = '2009771168-w9BjE7bI'
const IS_MOCK = import.meta.env.VITE_LIFF_MOCK === 'true'

export async function initLiff() {
  try {
    if (IS_MOCK) {
      liff.use(new LiffMockPlugin())
    }

    await liff.init({ liffId: LIFF_ID, mock: IS_MOCK })

    if (IS_MOCK) {
      return {
        lineUserId: mockProfile.userId,
        displayName: mockProfile.displayName,
        pictureUrl: mockProfile.pictureUrl
      }
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

export { liff, IS_MOCK }
