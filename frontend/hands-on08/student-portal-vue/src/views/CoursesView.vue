<script setup>
import { ref, computed, onMounted } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import { useEnrollmentStore } from '../stores/enrollment'
import { courses as courseData } from '../data/courses'

// Step 109: reactive courses array, populated inside onMounted
// (simulating an async load, e.g. from an API).
const courses = ref([])
const isLoading = ref(true)

onMounted(async () => {
  // simulate a short network delay before "arriving" with data
  await new Promise((resolve) => setTimeout(resolve, 300))
  courses.value = courseData
  isLoading.value = false
})

// Step 111: computed property filters by a ref searchTerm.
// computed() is cached and only re-runs when courses or searchTerm change.
const searchTerm = ref('')
const filteredCourses = computed(() =>
  courses.value.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
)

// Step 118: enrollment goes through the Pinia store.
const enrollmentStore = useEnrollmentStore()

function isEnrolled(courseId) {
  return enrollmentStore.enrolledCourses.some((c) => c.id === courseId)
}

function handleEnroll(courseId) {
  const course = courses.value.find((c) => c.id === courseId)
  if (course) enrollmentStore.enroll(course)
}
</script>

<template>
  <section class="courses">
    <h2>Course Listing</h2>

    <input
      v-model="searchTerm"
      type="text"
      class="search-input"
      placeholder="Search courses..."
      aria-label="Search courses"
    />

    <p role="status" aria-live="polite" class="results-count">
      {{ filteredCourses.length }} course(s) found
    </p>

    <p v-if="isLoading">Loading courses...</p>

    <div v-else class="course-grid">
      <!-- Step 110: v-for with :key, props passed via v-bind shorthand -->
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
        :enrolled="isEnrolled(course.id)"
        @enroll="handleEnroll"
      />
    </div>

    <p v-if="!isLoading && filteredCourses.length === 0" class="empty">
      No courses found.
    </p>
  </section>
</template>

<style scoped>
.courses {
  max-width: 72rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.courses h2 {
  margin-bottom: 1rem;
  color: #111827;
}

.search-input {
  width: 100%;
  max-width: 24rem;
  padding: 0.6rem 0.9rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.results-count {
  color: #6b7280;
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.empty {
  color: #6b7280;
  margin-top: 1.5rem;
}
</style>
