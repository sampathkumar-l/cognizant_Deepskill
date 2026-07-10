import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectEnrolledCourses } from '../features/enrollment/enrollmentSlice.js'

// Task 1, step 78: nav links use <Link> instead of <a> so navigation is
// client-side (no full page reload).
// Task 3, step 89: enrolled count now comes from the Redux store via
// useSelector instead of prop drilling or Context.
export default function Header({ siteName }) {
  const enrolledCourses = useSelector(selectEnrolledCourses)

  return (
    <header className="site-header">
      <h1>{siteName}</h1>
      <nav aria-label="Main navigation">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </nav>
      <span className="enrolled-count">Enrolled: {enrolledCourses.length}</span>
    </header>
  )
}
