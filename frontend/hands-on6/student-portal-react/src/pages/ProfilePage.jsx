import { useSelector, useDispatch } from 'react-redux'
import { selectEnrolledCourses, unenroll } from '../features/enrollment/enrollmentSlice.js'

// Task 3, step 89: reads state via useSelector + the selector function
// instead of touching store shape directly.
export default function ProfilePage() {
  const enrolledCourses = useSelector(selectEnrolledCourses)
  const dispatch = useDispatch()

  return (
    <section id="profile">
      <h2>My Enrolled Courses</h2>
      {enrolledCourses.length === 0 && <p>You haven't enrolled in any courses yet.</p>}
      <ul>
        {enrolledCourses.map((course) => (
          <li key={course.id}>
            {course.name} ({course.code})
            <button onClick={() => dispatch(unenroll(course.id))}>Remove</button>
          </li>
        ))}
      </ul>
    </section>
  )
}
