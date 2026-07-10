import { useState } from 'react';

function StudentProfile() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [semester, setSemester] = useState('');

  return (
    <section className="student-profile">
      <h2>Student Profile</h2>
      <form>
        <label>
          Name
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>

        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>

        <label>
          Semester
          <input
            type="number"
            value={semester}
            onChange={(e) => setSemester(e.target.value)}
          />
        </label>
      </form>
    </section>
  );
}

export default StudentProfile;