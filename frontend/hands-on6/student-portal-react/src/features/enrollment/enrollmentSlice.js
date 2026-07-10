import { createSlice } from '@reduxjs/toolkit'

// Task 3, step 87: createSlice with initial state and two reducers.
const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: {
    enrolledCourses: [],
  },
  reducers: {
    enroll(state, action) {
      const course = action.payload
      // Immer (used internally by RTK) lets us "mutate" state safely here.
      const alreadyEnrolled = state.enrolledCourses.some((c) => c.id === course.id)
      if (!alreadyEnrolled) {
        state.enrolledCourses.push(course)
      }
    },
    unenroll(state, action) {
      const courseId = action.payload
      state.enrolledCourses = state.enrolledCourses.filter((c) => c.id !== courseId)
    },
  },
})

export const { enroll, unenroll } = enrollmentSlice.actions

// Task 3, step 89: selectors so components use useSelector(selectEnrolledCourses)
// instead of reaching into store shape directly.
export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses

export default enrollmentSlice.reducer
