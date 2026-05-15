export const BADGE_BASE = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold w-fit'

const JOB_STATUS_MAP = {
  open:        'bg-blue-50 text-blue-800',
  matching:    'bg-teal-50 text-teal-800',
  selected:    'bg-purple-50 text-purple-800',
  in_progress: 'bg-indigo-50 text-indigo-800',
  completed:   'bg-green-50 text-green-800',
  cancelled:   'bg-slate-100 text-slate-600',
}

export function getJobStatusClass(status) {
  const key = (status || '').toLowerCase()
  return JOB_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const VERIFY_STATUS_MAP = {
  pending:      'bg-amber-50 text-amber-800',
  verified:     'bg-green-50 text-green-800',
  not_verified: 'bg-red-50 text-red-800',
}

export function getVerifyStatusClass(status) {
  const key = (status || '').toLowerCase()
  return VERIFY_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const DOC_STATUS_MAP = {
  pending:  'bg-amber-50 text-amber-800',
  approved: 'bg-green-50 text-green-800',
  rejected: 'bg-red-50 text-red-800',
}

export function getDocStatusClass(status) {
  const key = (status || '').toLowerCase()
  return DOC_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const ACTION_MAP = {
  approve_document:  'bg-green-50 text-green-800',
  verify_freelancer: 'bg-teal-50 text-teal-800',
  verify_employer:   'bg-teal-50 text-teal-800',
  reject_document:   'bg-rose-50 text-rose-800',
  unban_user:        'bg-blue-50 text-blue-800',
  update:            'bg-purple-50 text-purple-800',
  view:              'bg-sky-50 text-sky-800',
  ban_user:          'bg-orange-50 text-orange-800',
  delete:            'bg-red-100 text-red-900',
}

export function getActionClass(action) {
  const key = (action || '').toLowerCase()
  return ACTION_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const TYPE_MAP = {
  freelancer: 'bg-sky-100 text-sky-800',
  employer:   'bg-purple-50 text-purple-800',
  job:        'bg-amber-50 text-amber-800',
  document:   'bg-emerald-50 text-emerald-800',
  user:       'bg-pink-50 text-pink-800',
}

export function getTypeClass(type) {
  const key = (type || '').toLowerCase()
  return TYPE_MAP[key] ?? 'bg-gray-100 text-gray-500'
}