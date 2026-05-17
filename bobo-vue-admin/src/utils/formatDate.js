export const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

export const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

export const formatJobStatus = (status) => {
  if (!status) return ''
  const map = { MATCHING: 'PENDING', SELECTED: 'MATCHED' }
  return map[status.toUpperCase()] ?? status
}