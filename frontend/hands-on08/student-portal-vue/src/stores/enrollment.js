import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// Step 117: Pinia store defined in "setup store" (Composition API) style.
// This is more flexible and TypeScript-friendly than the Options API style.
export const useEnrollmentStore = defineStore('enrollment', () => {
  // state
  const enrolledCourses = ref([])

  // computed (getter)
  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0)
  )

  // actions
  function enroll(course) {
    const alreadyEnrolled = enrolledCourses.value.some((c) => c.id === course.id)
    if (!alreadyEnrolled) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId)
  }

  // Step 149 (advanced, from Hands-On 10 preview): async action + $reset-style helper.
  // Included here so the store already demonstrates the pattern.
  async function fetchAndEnroll(course) {
    // simulate a network delay, e.g. an API call confirming enrollment
    await new Promise((resolve) => setTimeout(resolve, 400))
    enroll(course)
  }

  function resetEnrollment() {
    enrolledCourses.value = []
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll,
    fetchAndEnroll,
    resetEnrollment
  }
})
