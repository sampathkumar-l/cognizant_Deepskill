import { createContext, useContext, useState } from 'react'

// Task 2, step 81: Context definition + provider that holds enrolledCourses
// state, so any descendant component can read/update it without prop drilling.
const EnrollmentContext = createContext(null)

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([])

  const enrollCourse = (course) => {
    setEnrolledCourses((prev) => {
      if (prev.some((c) => c.id === course.id)) return prev
      return [...prev, course]
    })
  }

  // Task 2, step 84: Remove/un-enroll function exposed through the context.
  const removeCourse = (courseId) => {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId))
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, removeCourse }}>
      {children}
    </EnrollmentContext.Provider>
  )
}

// Convenience hook so consumers just call useEnrollment() instead of
// useContext(EnrollmentContext) directly.
export function useEnrollment() {
  return useContext(EnrollmentContext)
}

// NOTE: This Context-based store was used to satisfy Task 2. Task 3 migrates
// the same responsibility to Redux Toolkit (see features/enrollment/enrollmentSlice.js).
// The app below wires up the Redux version, since Task 3 says to replace Context
// with Redux — this file is kept to show/compare the two approaches side by side.
