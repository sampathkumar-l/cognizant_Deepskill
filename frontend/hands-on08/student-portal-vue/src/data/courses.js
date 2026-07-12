// Step 109: canonical course data used across the Vue app.
// CoursesView loads this (simulating an API call) inside onMounted.
// CourseDetailView imports the same list to resolve the :id route param.
export const courses = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Wireless Communication', code: 'EC3501', credits: 3, grade: 'B+' },
  { id: 3, name: 'Network Security', code: 'CS305', credits: 4, grade: 'A-' },
  { id: 4, name: 'Operating Systems', code: 'CS204', credits: 4, grade: 'B' },
  { id: 5, name: 'Database Systems', code: 'CS210', credits: 3, grade: 'A' }
]
