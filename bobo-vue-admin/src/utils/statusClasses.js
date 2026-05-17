export const BADGE_BASE = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold w-fit'

const JOB_STATUS_MAP = {
  open:        'bg-blue-100 text-blue-800',
  matching:    'bg-amber-100 text-amber-800',
  selected:    'bg-green-100 text-green-800',
  in_progress: 'bg-amber-100 text-amber-800',
  completed:   'bg-slate-100 text-slate-600',
  cancelled:   'bg-red-100 text-red-800',
}

export function getJobStatusClass(status) {
  const key = (status || '').toLowerCase()
  return JOB_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const VERIFY_STATUS_MAP = {
  pending:      'bg-amber-100 text-amber-800',
  verified:     'bg-green-100 text-green-800',
  not_verified: 'bg-red-100 text-red-800',
}

export function getVerifyStatusClass(status) {
  const key = (status || '').toLowerCase()
  return VERIFY_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const DOC_STATUS_MAP = {
  pending:  'bg-amber-100 text-amber-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
}

export function getDocStatusClass(status) {
  const key = (status || '').toLowerCase()
  return DOC_STATUS_MAP[key] ?? 'bg-gray-100 text-gray-500'
}

const ACTION_MAP = {
  approve_document:  'action-approve',
  verify_freelancer: 'action-verify',
  verify_employer:   'action-verify',
  reject_document:   'action-reject',
  unban_user:        'action-unban',
  update:            'action-update',
  view:              'action-view',
  ban_user:          'action-ban',
  delete:            'action-delete',
  delete_job:        'action-delete',
}

export function getActionClass(action) {
  const key = (action || '').toLowerCase()
  return ACTION_MAP[key] ?? 'action-default'
}

const TYPE_MAP = {
  freelancer: 'type-freelancer',
  employer:   'type-employer',
  job:        'type-job',
  document:   'type-document',
  user:       'type-user',
}

export function getTypeClass(type) {
  const key = (type || '').toLowerCase()
  return TYPE_MAP[key] ?? 'type-default'
}