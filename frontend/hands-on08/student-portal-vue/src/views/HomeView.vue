<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const enrollmentStore = useEnrollmentStore()
</script>

<template>
  <section class="hero">
    <h1>Welcome to the Student Portal</h1>
    <p>Browse your courses, track credits, and manage your profile - built with Vue 3.</p>
    <RouterLink to="/courses" class="cta">Explore Courses</RouterLink>
  </section>

  <section class="stats">
    <div class="stat">
      <span class="stat__value">{{ enrollmentStore.enrolledCourses.length }}</span>
      <span class="stat__label">Courses Enrolled</span>
    </div>
    <div class="stat">
      <span class="stat__value">{{ enrollmentStore.totalCredits }}</span>
      <span class="stat__label">Total Credits</span>
    </div>
    <div class="stat">
      <span class="stat__value">6</span>
      <span class="stat__label">Semester</span>
    </div>
  </section>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 4rem 1.5rem;
  min-height: 40vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: linear-gradient(180deg, #eef2ff 0%, #ffffff 100%);
}

.hero h1 {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  color: #1f2937;
  margin: 0;
}

.hero p {
  color: #4b5563;
  max-width: 32rem;
}

.cta {
  margin-top: 0.5rem;
  display: inline-block;
  padding: 0.65rem 1.5rem;
  background: #2563eb;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
}

.cta:hover {
  background: #1d4ed8;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  padding: 2rem 1rem;
  flex-wrap: wrap;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat__value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
}

.stat__label {
  color: #6b7280;
  font-size: 0.85rem;
}
</style>
