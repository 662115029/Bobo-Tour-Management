import { ref } from 'vue'

   const verifyStatus = ref('')

   export function useVerifyBanner() {
     return { verifyStatus }
   }