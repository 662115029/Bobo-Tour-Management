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

/**
 * Groups an array of documents by type, keeping only the latest
 * uploaded doc per type, then normalizes to a flat shape.
 *
 * @param {Array} docs - raw doc array (fl-documents or em-documents)
 * @param {'fl'|'em'} prefix - field prefix ('fl' or 'em')
 * @param {Function} formatDateTimeFn - formatDateTime function to format dates
 * @returns {Array} normalized doc objects: { id, type, status, file_url, uploaded, reviewed, _type }
 */
export function groupDocsByLatest(docs, prefix, formatDateTimeFn) {
  const byType = {}
  const typeKey = `${prefix}_doc_type`
  const uploadKey = `${prefix}_uploaded_at`

  docs.forEach(d => {
    if (!byType[d[typeKey]] || new Date(d[uploadKey]) > new Date(byType[d[typeKey]][uploadKey])) {
      byType[d[typeKey]] = d
    }
  })

  return Object.values(byType).map(d => ({
    id: d[`${prefix}_doc_id`],
    type: d[typeKey],
    status: d[`${prefix}_doc_status`],
    file_url: d.file_url,
    uploaded: formatDateTimeFn(d[uploadKey]),
    reviewed: d.reviewed_at ? formatDateTimeFn(d.reviewed_at) : null,
    _type: prefix,
  }))
}