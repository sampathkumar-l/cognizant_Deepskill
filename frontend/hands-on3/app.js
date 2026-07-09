import { courses } from './data.js';

/* ---------- Task 1: ES6+ Syntax Practice ---------- */

// destructuring in a loop
for (const course of courses) {
  const { name, credits } = course;
  console.log(`${name} — ${credits} credits`);
}

// map: formatted strings
const formatted = courses.map(
  ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);
console.log('Formatted courses:', formatted);

// filter: credits >= 4
const heavyCourses = courses.filter(course => course.credits >= 4);
console.log('Courses with 4+ credits:', heavyCourses.length);

// reduce: total credits
const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
console.log('Total credits:', totalCredits);

/* ---------- Task 2: DOM Selection & Dynamic Rendering ---------- */

const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const resultsCountEl = document.getElementById('results-count');

function renderCourses(list) {
  courseGrid.innerHTML = ''; // clear before re-render to avoid duplicates

  const fragment = document.createDocumentFragment();

  list.forEach(course => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.dataset.id = course.id;
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    fragment.appendChild(article);
  });

  courseGrid.appendChild(fragment);

  if (resultsCountEl) {
    resultsCountEl.textContent = `${list.length} course${list.length !== 1 ? 's' : ''} found`;
  }
}

function updateTotalCredits(list) {
  const sum = list.reduce((acc, c) => acc + c.credits, 0);
  totalCreditsEl.textContent = `Total credits: ${sum}`;
}

renderCourses(courses);
updateTotalCredits(courses);

/* ---------- Task 3: Event Listeners & Interactivity ---------- */

const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-credits');
const selectedCourseEl = document.getElementById('selected-course');

// live search filter
searchInput.addEventListener('input', (e) => {
  const term = e.target.value.toLowerCase();
  const filtered = courses.filter(c => c.name.toLowerCase().includes(term));
  renderCourses(filtered);
  updateTotalCredits(filtered);
});

// sort by credits descending
sortButton.addEventListener('click', () => {
  courses.sort((a, b) => b.credits - a.credits);
  renderCourses(courses);
  updateTotalCredits(courses);
});

// event delegation: single listener on the grid container
courseGrid.addEventListener('click', (e) => {
  const card = e.target.closest('.course-card');
  if (!card) return;

  const course = courses.find(c => c.id === Number(card.dataset.id));
  if (course && selectedCourseEl) {
    selectedCourseEl.textContent = `${course.name} — Grade: ${course.grade}`;
  }
});