import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';
import './App.css';

function App() {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Task 3: fetch courses from API on mount
  useEffect(() => {
    async function loadCourses() {
      try {
        const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
        if (!res.ok) throw new Error('Failed to load courses');
        const posts = await res.json();

        const mapped = posts.map((post, i) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS10${i + 1}`,
          credits: 3 + (i % 2),
          grade: 'A'
        }));

        setCourses(mapped);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  // log whenever courses state changes
  useEffect(() => {
    console.log('Courses updated');
    // empty dependency array elsewhere would mean "run once on mount";
    // depending on `courses` here means this effect re-runs every time
    // the courses array reference changes, e.g. after the fetch resolves.
  }, [courses]);

  const handleEnroll = (course) => {
    setEnrolledCourses((prev) => {
      if (prev.some((c) => c.id === course.id)) return prev;
      return [...prev, course];
    });
  };

  const filteredCourses = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main>
        <section id="courses">
          <h2>Courses</h2>

          <input
            type="text"
            placeholder="Search courses..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          {loading && <p>Loading...</p>}
          {error && <p className="error-msg">{error}</p>}

          <div className="course-grid">
            {filteredCourses.map((course) => (
              <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
            ))}
          </div>
        </section>

        <StudentProfile />
      </main>

      <Footer />
    </>
  );
}

export default App;