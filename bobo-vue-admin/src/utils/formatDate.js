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
const FL_DOC_TYPES = ['PERSONAL_ID', 'DRIVER_LICENSE', 'PUBLIC_DRIVER_LICENSE', 'VEHICLE_REGISTRATION', 'VEHICLE_INSPECTION']
const EM_DOC_TYPES = ['COMPANY_REGISTRATION', 'BUSINESS_LICENSE', 'TOURISM_LICENSE', 'TAX_ID_DOCUMENT', 'AUTHORIZED_PERSON_ID']

export function groupDocsByLatest(docs, prefix, formatDateTimeFn) {
  const byType = {}
  const typeKey = `${prefix}_doc_type`
  const uploadKey = `${prefix}_uploaded_at`
  const idKey = `${prefix}_doc_id`
  const statusKey = `${prefix}_doc_status`

  docs.forEach(d => {
    const isLatest = d.is_latest === 1 || d.is_latest === true
    const existing = byType[d[typeKey]]
    if (!existing) {
      byType[d[typeKey]] = d
    } else {
      const existingIsLatest = existing.is_latest === 1 || existing.is_latest === true
      if (isLatest && !existingIsLatest) {
        byType[d[typeKey]] = d
      } else if (isLatest && existingIsLatest && d[uploadKey] && new Date(d[uploadKey]) > new Date(existing[uploadKey])) {
        byType[d[typeKey]] = d
      }
    }
  })

  const allTypes = prefix === 'fl' ? FL_DOC_TYPES : EM_DOC_TYPES
  allTypes.forEach(type => {
    if (!byType[type]) {
      byType[type] = {
        [idKey]: `empty_${type}`,
        [typeKey]: type,
        [statusKey]: 'PENDING',
        file_url: null,
        [uploadKey]: null,
        reviewed_at: null,
        is_latest: 1,
      }
    }
  })

  return allTypes.map(type => {
    const d = byType[type]
    return {
      id: d[idKey],
      type: d[typeKey],
      status: d[statusKey],
      file_url: d.file_url,
      uploaded: d[uploadKey] ? formatDateTimeFn(d[uploadKey]) : null,
      reviewed: d.reviewed_at ? formatDateTimeFn(d.reviewed_at) : null,
      _type: prefix,
    }
  })
}