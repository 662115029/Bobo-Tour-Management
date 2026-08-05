import { ref } from 'vue'

const isOpen = ref(true)

export function useSidebar() {
  const toggle = () => { isOpen.value = !isOpen.value }
  const close = () => { isOpen.value = false }
  const open = () => { isOpen.value = true }
  return { isOpen, toggle, close, open }
}

