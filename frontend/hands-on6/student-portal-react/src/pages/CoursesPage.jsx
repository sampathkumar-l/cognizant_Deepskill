import { useState } from 'react'
import CourseCard from '../components/CourseCard.jsx'
import { courses as seedCourses } from '../data/courses.js'

// Task 1, step 77: this is the component rendered at the /courses route.
export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('')

  const filteredCourses = seedCourses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <section id="courses">
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="course-grid">
        {filteredCourses.map((course) => (
          <CourseCard key={course.id} {...course} />
        ))}
      </div>
      {filteredCourses.length === 0 && <p>No courses found.</p>}
    </section>
  )
}
