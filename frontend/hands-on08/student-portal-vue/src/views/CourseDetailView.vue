<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courses } from '../data/courses'
import { useEnrollmentStore } from '../stores/enrollment'

// Step 114: useRoute() reads the :id param from the URL.
const route = useRoute()
// Step 115: useRouter() lets us navigate programmatically after enrolling.
const router = useRouter()

const enrollmentStore = useEnrollmentStore()

const course = computed(() =>
  courses.find((c) => c.id === Number(route.params.id))
)

const isEnrolled = computed(() =>
  course.value
    ? enrollmentStore.enrolledCourses.some((c) => c.id === course.value.id)
    : false
)

function handleEnroll() {
  if (!course.value) return
  enrollmentStore.enroll(course.value)
  // Step 115: redirect to /profile after enrolling.
  router.push('/profile')
}
</script>

<template>
  <section class="course-detail">
    <RouterLink to="/courses" class="back-link">&larr; Back to courses</RouterLink>

    <div v-if="course" class="detail-card">
      <h2>{{ course.name }}</h2>
      <p class="code">{{ course.code }}</p>
      <dl>
        <dt>Credits</dt>
        <dd>{{ course.credits }}</dd>
        <dt>Grade</dt>
        <dd>{{ course.grade }}</dd>
      </dl>

      <button class="enroll-btn" :disabled="isEnrolled" @click="handleEnroll">
        {{ isEnrolled ? 'Already Enrolled' : 'Enroll' }}
      </button>
    </div>

    <p v-else class="not-found">
      No course found with id "{{ route.params.id }}".
    </p>
  </section>
</template>

<style scoped>
.course-detail {
  max-width: 40rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  color: #2563eb;
  text-decoration: none;
  font-size: 0.9rem;
}

.detail-card {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.75rem;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.detail-card h2 {
  margin: 0 0 0.25rem;
  color: #111827;
}

.code {
  color: #6b7280;
  margin-bottom: 1rem;
}

dl {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.35rem 1rem;
  margin-bottom: 1.5rem;
}

dt {
  font-weight: 600;
  color: #374151;
}

dd {
  margin: 0;
  color: #111827;
}

.enroll-btn {
  padding: 0.55rem 1.4rem;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.enroll-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.enroll-btn:disabled {
  background: #d1fae5;
  color: #065f46;
  cursor: default;
}

.not-found {
  color: #6b7280;
}
</style>
