import { ref } from 'vue'

const isOpen = ref(false)
const message = ref('')
const title = ref('')
let resolvePromise = null

export function useConfirm() {
  function confirmDialog(msg, dialogTitle = 'Confirm Action') {
    message.value = msg
    title.value = dialogTitle
    isOpen.value = true
    return new Promise((resolve) => { resolvePromise = resolve })
  }
  function handleConfirm() { isOpen.value = false; resolvePromise?.(true) }
  function handleCancel() { isOpen.value = false; resolvePromise?.(false) }
  return { isOpen, message, title, confirmDialog, handleConfirm, handleCancel }
}
