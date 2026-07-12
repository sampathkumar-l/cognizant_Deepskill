<script setup>
import { storeToRefs } from 'pinia'
import { useEnrollmentStore } from '../stores/enrollment'

const enrollmentStore = useEnrollmentStore()

// storeToRefs keeps reactivity when destructuring state/getters out of the
// store - plain destructuring (const { enrolledCourses } = store) would lose it.
const { enrolledCourses, totalCredits } = storeToRefs(enrollmentStore)

function handleRemove(courseId) {
  enrollmentStore.unenroll(courseId)
}
</script>

<template>
  <section class="profile">
    <h2>My Enrollment</h2>

    <p v-if="enrolledCourses.length === 0" class="empty">
      You haven't enrolled in any courses yet.
      <RouterLink to="/courses">Browse courses</RouterLink>
    </p>

    <ul v-else class="enrolled-list">
      <li v-for="course in enrolledCourses" :key="course.id" class="enrolled-item">
        <div>
          <strong>{{ course.name }}</strong>
          <span class="code">{{ course.code }}</span>
        </div>
        <div class="enrolled-item__right">
          <span>{{ course.credits }} credits</span>
          <button class="remove-btn" @click="handleRemove(course.id)">Remove</button>
        </div>
      </li>
    </ul>

    <p v-if="enrolledCourses.length > 0" class="summary">
      Total credits enrolled: <strong>{{ totalCredits }}</strong>
    </p>
  </section>
</template>

<style scoped>
.profile {
  max-width: 40rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.profile h2 {
  color: #111827;
  margin-bottom: 1.25rem;
}

.empty {
  color: #6b7280;
}

.enrolled-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.enrolled-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.9rem 1.1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
}

.enrolled-item .code {
  display: block;
  color: #6b7280;
  font-size: 0.8rem;
}

.enrolled-item__right {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: #374151;
}

.remove-btn {
  padding: 0.35rem 0.8rem;
  border: 1px solid #fca5a5;
  border-radius: 6px;
  background: #fef2f2;
  color: #b91c1c;
  cursor: pointer;
  font-size: 0.85rem;
}

.remove-btn:hover {
  background: #fee2e2;
}

.summary {
  margin-top: 1.5rem;
  color: #111827;
}
</style>
