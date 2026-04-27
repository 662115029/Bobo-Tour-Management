export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/admin/stats`)
  if (!res.ok) throw new Error('Failed to fetch stats')
  return res.json()
}

export async function fetchJobs() {
  const res = await fetch(`${API_BASE}/jobs`)
  if (!res.ok) throw new Error('Failed to fetch jobs')
  return res.json()
}

export async function fetchFreelancers() {
  const res = await fetch(`${API_BASE}/admin/freelancers`)
  if (!res.ok) throw new Error('Failed to fetch freelancers')
  return res.json()
}

export async function fetchEmployers() {
  const res = await fetch(`${API_BASE}/admin/employers`)
  if (!res.ok) throw new Error('Failed to fetch employers')
  return res.json()
}

export async function fetchVerifications() {
  const [freelancers, employers] = await Promise.all([
    fetchFreelancers(),
    fetchEmployers()
  ])
  const pendingFreelancers = freelancers.items
    .filter(f => f.fl_verify_status === 'PENDING')
    .map(f => ({
      id: f.fl_id,
      name: f.fl_name || f.line_user_id,
      type: 'Freelancer',
      status: f.fl_verify_status,
      submitted: new Date(f.fl_created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
    }))
  const pendingEmployers = employers.items
    .filter(e => e.em_verify_status === 'PENDING')
    .map(e => ({
      id: e.em_id,
      name: e.em_name || e.em_username,
      type: 'Employer',
      status: e.em_verify_status,
      submitted: new Date(e.em_created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
    }))
  return [...pendingFreelancers, ...pendingEmployers]
}

export async function fetchLogs() {
  const res = await fetch(`${API_BASE}/admin/logs`)
  if (!res.ok) throw new Error('Failed to fetch logs')
  return res.json()
}