<script setup>
// Step 107: single-file component with <template>, <script setup>, <style scoped>.
// Step 120: enrolled course count read directly from the Pinia store - no props needed.
import { useEnrollmentStore } from '../stores/enrollment'

const enrollmentStore = useEnrollmentStore()
</script>

<template>
  <header class="site-header">
    <RouterLink to="/" class="brand">Student Portal</RouterLink>

    <nav class="main-nav" aria-label="Main navigation">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>

    <div class="enrolled-badge" title="Courses you're enrolled in">
      <span class="enrolled-count">{{ enrollmentStore.enrolledCourses.length }}</span>
      <span class="enrolled-label">enrolled</span>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1rem 2rem;
  background: #1f2937;
  color: #f9fafb;
}

.brand {
  font-weight: 700;
  font-size: 1.25rem;
  color: #f9fafb;
  text-decoration: none;
  white-space: nowrap;
}

.main-nav {
  display: flex;
  gap: 1.25rem;
  flex: 1;
}

.main-nav a {
  color: #d1d5db;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 0.25rem 0;
  border-bottom: 2px solid transparent;
}

.main-nav a:hover {
  color: #f9fafb;
}

.main-nav a.router-link-exact-active {
  color: #f9fafb;
  border-bottom-color: #34d399;
}

.enrolled-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: #111827;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
}

.enrolled-count {
  background: #34d399;
  color: #064e3b;
  font-weight: 700;
  border-radius: 999px;
  min-width: 1.4rem;
  height: 1.4rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 0.35rem;
}

.enrolled-label {
  color: #9ca3af;
}
</style>
