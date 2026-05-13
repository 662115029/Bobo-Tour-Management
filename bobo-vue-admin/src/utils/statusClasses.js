export const BADGE_BASE = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold w-fit'

const JOB_STATUS_MAP = {
  open:        'bg-blue-50 text-blue-700',
  matching:    'bg-teal-50 text-teal-700',
  selected:    'bg-purple-50 text-purple-700',
  in_progress: 'bg-amber-100 text-amber-800',
  completed:   'bg-gray-100 text-gray-500',
  cancelled:   'bg-red-50 text-red-700',
}

export function getJobStatusClass(status) {
  const key = (status || '').toLowerCase()
  return JOB_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const VERIFY_STATUS_MAP = {
  pending:      'bg-orange-50 text-orange-600',
  verified:     'bg-green-50 text-green-700',
  not_verified: 'bg-red-50 text-red-700',
}

export function getVerifyStatusClass(status) {
  const key = (status || '').toLowerCase()
  return VERIFY_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const DOC_STATUS_MAP = {
  pending:  'bg-orange-50 text-orange-600',
  approved: 'bg-green-50 text-green-700',
  rejected: 'bg-red-50 text-red-700',
}

export function getDocStatusClass(status) {
  const key = (status || '').toLowerCase()
  return DOC_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const ACTION_MAP = {
  approve_document:  'bg-green-50 text-green-700',
  verify_freelancer: 'bg-teal-50 text-teal-700',
  verify_employer:   'bg-teal-50 text-teal-700',
  reject_document:   'bg-pink-50 text-pink-700',
  unban_user:        'bg-blue-50 text-blue-700',
  update:            'bg-violet-50 text-violet-700',
  view:              'bg-sky-50 text-sky-700',
  ban_user:          'bg-orange-100 text-orange-700',
  delete:            'bg-red-100 text-red-800',
}

export function getActionClass(action) {
  const key = (action || '').toLowerCase()
  return ACTION_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const TYPE_MAP = {
  freelancer: 'bg-sky-100 text-sky-800',
  employer:   'bg-purple-50 text-purple-700',
  job:        'bg-orange-50 text-orange-800',
  document:   'bg-emerald-50 text-emerald-700',
  user:       'bg-fuchsia-50 text-fuchsia-700',
}

export function getTypeClass(type) {
  const key = (type || '').toLowerCase()
  return TYPE_MAP[key] ?? 'bg-gray-100 text-gray-500'
}