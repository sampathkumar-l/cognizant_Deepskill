import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { courses } from '../data/courses.js'
import { enroll } from '../features/enrollment/enrollmentSlice.js'

// Task 1, step 79: useParams() reads :courseId from the URL.
export default function CourseDetailPage() {
  const { courseId } = useParams()
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const course = courses.find((c) => String(c.id) === courseId)

  if (!course) {
    return <p>Course not found.</p>
  }

  const handleEnroll = () => {
    dispatch(enroll(course))
    // Task 1, step 80: navigate to /profile automatically after enrolling.
    navigate('/profile')
  }

  return (
    <section id="course-detail">
      <h2>{course.name}</h2>
      <p>{course.code} &mdash; {course.credits} credits</p>
      <p>Grade: {course.grade}</p>
      <button onClick={handleEnroll}>Enroll</button>
    </section>
  )
}
