export const mockJobs = [
  {
    id: 1,
    title: 'Tour Driver - Chiang Rai',
    company: 'NorthTour Co.',
    date: '20 Apr 2026',
    status: 'Active'
  },
  {
    id: 2,
    title: 'City Guide - Bangkok',
    company: 'BKK Travel',
    date: '19 Apr 2026',
    status: 'Active'
  },
  {
    id: 3,
    title: 'Transfer Driver - Phuket',
    company: 'AndaSea Ltd.',
    date: '18 Apr 2026',
    status: 'Closed'
  },
  {
    id: 4,
    title: 'Night Tour - Chiang Mai',
    company: 'LannaTour',
    date: '17 Apr 2026',
    status: 'Active'
  },
  {
    id: 5,
    title: 'Airport Shuttle - HKT',
    company: 'SkyLink',
    date: '16 Apr 2026',
    status: 'Closed'
  }
]

export const mockVerifications = [
  {
    id: 1,
    name: 'Somchai W.',
    type: 'Freelancer',
    status: 'Pending',
    submitted: '20 Apr 2026'
  },
  {
    id: 2,
    name: 'Praew K.',
    type: 'Freelancer',
    status: 'Verified',
    submitted: '18 Apr 2026'
  },
  {
    id: 3,
    name: 'Natt P.',
    type: 'Freelancer',
    status: 'Pending',
    submitted: '17 Apr 2026'
  },
  {
    id: 4,
    name: 'Tong S.',
    type: 'Freelancer',
    status: 'Rejected',
    submitted: '15 Apr 2026'
  },
  {
    id: 5,
    name: 'Kanda Corp.',
    type: 'Employer',
    status: 'Pending',
    submitted: '19 Apr 2026'
  }
]

export const mockUsers = [
  {
    id: 1,
    name: 'Praew Kanchanawong',
    initials: 'PK',
    status: 'Active',
    score: 4.8,
    jobs: 32
  },
  {
    id: 2,
    name: 'Nattapon Siri',
    initials: 'NS',
    status: 'Active',
    score: 4.5,
    jobs: 18
  },
  {
    id: 3,
    name: 'Tong Prasong',
    initials: 'TP',
    status: 'Banned',
    score: 2.1,
    jobs: 5
  }
]

export const mockLogs = [
  {
    id: 1,
    admin: 'admin@app.com',
    action: 'VERIFY',
    target: 'Praew Kanchanawong',
    time: '20 Apr 14:32'
  },
  {
    id: 2,
    admin: 'admin@app.com',
    action: 'REJECT',
    target: 'Tong Prasong',
    time: '20 Apr 13:15'
  },
  {
    id: 3,
    admin: 'admin@app.com',
    action: 'BAN',
    target: 'Tong Prasong',
    time: '20 Apr 11:02'
  },
  {
    id: 4,
    admin: 'admin@app.com',
    action: 'DELETE',
    target: 'Job #1091',
    time: '19 Apr 17:44'
  },
  {
    id: 5,
    admin: 'admin@app.com',
    action: 'VERIFY',
    target: 'Nattapon Siri',
    time: '19 Apr 10:20'
  },
  {
    id: 6,
    admin: 'admin@app.com',
    action: 'VERIFY',
    target: 'BKK Travel Co.',
    time: '18 Apr 09:11'
  }
]

export const stats = {
  totalJobs: 1284,
  pendingVerify: 47,
  freelancers: 832,
  employers: 213
}