import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { enroll } from '../features/enrollment/enrollmentSlice.js'

// Task 1, step 79-80: clicking through to /courses/:courseId happens via the
// <Link>. Enrolling then calls useNavigate() to redirect to /profile.
export default function CourseCard({ id, name, code, credits, grade }) {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleEnroll = () => {
    dispatch(enroll({ id, name, code, credits, grade }))
    navigate('/profile')
  }

  return (
    <article className="course-card">
      <h3><Link to={`/courses/${id}`}>{name}</Link></h3>
      <p>{code} &mdash; {credits} credits</p>
      <span>Grade: {grade}</span>
      <button onClick={handleEnroll}>Enroll</button>
    </article>
  )
}
