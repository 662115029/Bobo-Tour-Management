<template>
  <div>
    <h1 class="title">Dashboard</h1>
    
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-label">TOTAL JOBS</span>
        <span class="stat-value">{{ stats.totalJobs.toLocaleString() }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">PENDING VERIFY</span>
        <span class="stat-value">{{ stats.pendingVerify }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">FREELANCERS</span>
        <span class="stat-value">{{ stats.freelancers }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">EMPLOYERS</span>
        <span class="stat-value">{{ stats.employers }}</span>
      </div>
    </div>

    <section>
      <h2 class="section-title">Recent Jobs</h2>
      <table class="table">
        <thead>
          <tr>
            <th>JOB TITLE</th>
            <th>COMPANY</th>
            <th>DATE</th>
            <th>STATUS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in mockJobs.slice(0, 3)" :key="job.id">
            <td>{{ job.title }}</td>
            <td>{{ job.company }}</td>
            <td>{{ job.date }}</td>
            <td>
              <span class="badge" :class="job.status.toLowerCase()">{{ job.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2 class="section-title">Recent Verifications</h2>
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>TYPE</th>
            <th>SUBMITTED</th>
            <th>STATUS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in mockVerifications.slice(0, 2)" :key="v.id">
            <td>{{ v.name }}</td>
            <td>{{ v.type }}</td>
            <td>{{ v.submitted }}</td>
            <td>
              <span class="badge" :class="v.status.toLowerCase()">{{ v.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { mockJobs, mockVerifications, stats } from '../data/mockData'
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 600;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #1a1a2e;
}

section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  margin-bottom: 16px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.closed {
  background: #f5f5f5;
  color: #666;
}

.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.rejected {
  background: #ffebee;
  color: #c62828;
}
</style>