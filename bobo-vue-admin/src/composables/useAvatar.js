export function useAvatar() {
  const AVATAR_PALETTES = [
    { bg: '#e3f2fd', text: '#1565c0' }, { bg: '#fce4ec', text: '#ad1457' },
    { bg: '#e8f5e9', text: '#2e7d32' }, { bg: '#fff3e0', text: '#e65100' },
    { bg: '#f3e5f5', text: '#6a1b9a' }, { bg: '#e0f7fa', text: '#00695c' },
    { bg: '#fff8e1', text: '#f57f17' }, { bg: '#fbe9e7', text: '#bf360c' },
  ]

  const JOB_ICON_PALETTES = [
    { bg: '#e8f0fe', text: '#1a73e8' }, { bg: '#fce8e6', text: '#d93025' },
    { bg: '#e6f4ea', text: '#1e8e3e' }, { bg: '#fef3cd', text: '#b45309' },
    { bg: '#f3e8fd', text: '#7b1fa2' }, { bg: '#e0f7fa', text: '#00796b' },
    { bg: '#fff3e0', text: '#e65100' }, { bg: '#fce4ec', text: '#c2185b' },
  ]

  const _hash = (str) => {
    let h = 0
    for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0
    return h
  }

  const avatarStyle = (id, name) => {
    const p = AVATAR_PALETTES[_hash(String(id || name || '?')) % AVATAR_PALETTES.length]
    return { backgroundColor: p.bg, color: p.text }
  }

  const jobIconStyle = (id) => {
    const p = JOB_ICON_PALETTES[_hash(String(id || '?')) % JOB_ICON_PALETTES.length]
    return { backgroundColor: p.bg, color: p.text }
  }

  const initials2 = (name) => {
    if (!name) return '?'
    return name.trim().split(/\s+/).slice(0, 2).map(p => p[0]?.toUpperCase() || '').join('')
  }

  return { avatarStyle, jobIconStyle, initials2 }
}