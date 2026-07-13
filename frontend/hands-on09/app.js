
const courses = [
  { id: 1, name: "Data Structures", code: "CS101", credits: 4, grade: "A" },
  { id: 2, name: "Web Development", code: "CS102", credits: 3, grade: "A-" },
  { id: 3, name: "Database Systems", code: "CS201", credits: 4, grade: "B+" },
  { id: 4, name: "Operating Systems", code: "CS202", credits: 4, grade: "A" },
  { id: 5, name: "Cloud Computing", code: "CS301", credits: 3, grade: "B" },
];

const courseGrid = document.querySelector("#course-grid");
const resultsCount = document.querySelector("#results-count");
const selectedCourseEl = document.querySelector("#selected-course");
const searchInput = document.querySelector("#search-courses");

/**
 * Renders course cards as real <button> elements so they are natively
 * focusable and operable with both mouse and keyboard (Enter / Space)
 * without any extra tabindex/keydown wiring needed.
 */
function renderCourses(list) {
  courseGrid.innerHTML = "";

  list.forEach((course) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "course-card";
    card.setAttribute("data-id", course.id);
    card.setAttribute(
      "aria-label",
      `${course.name}, code ${course.code}, ${course.credits} credits, grade ${course.grade}`
    );
    card.innerHTML = `
      <h3>${course.name}</h3>
      <p class="credits">${course.code} &middot; ${course.credits} credits</p>
    `;
    card.addEventListener("click", () => showSelectedCourse(course));
    courseGrid.appendChild(card);
  });

  // aria-live region on #results-count announces the new count to
  // screen reader users whenever the filtered list changes (Task 2, step 130).
  resultsCount.textContent = `${list.length} course${list.length === 1 ? "" : "s"} found`;
}

function showSelectedCourse(course) {
  selectedCourseEl.textContent = `Selected: ${course.name} — Grade: ${course.grade}`;
}

// Live filtering as the user types (search input has a bound <label>)
searchInput.addEventListener("input", (event) => {
  const term = event.target.value.trim().toLowerCase();
  const filtered = courses.filter((c) => c.name.toLowerCase().includes(term));
  renderCourses(filtered);
});

// ---------- Mobile nav toggle with aria-expanded ----------
const navToggle = document.querySelector("#nav-toggle");
const primaryNav = document.querySelector("#primary-nav");

navToggle.addEventListener("click", () => {
  const isOpen = primaryNav.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

// ---------- Explore Courses button scrolls to course section ----------
document.querySelector("#explore-btn").addEventListener("click", () => {
  document.querySelector("#courses-section").scrollIntoView({ behavior: "smooth" });
});

// ---------- Profile form: basic validation + feedback ----------
const profileForm = document.querySelector("#profile-form");
profileForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (profileForm.checkValidity()) {
    alert("Profile saved.");
  } else {
    // Native browser validation messages are announced by screen readers
    // when reportValidity() is called on an invalid form.
    profileForm.reportValidity();
  }
});

// ---------- Feature detection (safer than browser sniffing) ----------
// Task 3, step 136-137: prefer @supports / typeof checks over UA sniffing.
const supportsCSSGap =
  typeof CSS !== "undefined" && CSS.supports && CSS.supports("gap", "1rem");
if (!supportsCSSGap) {
  console.warn(
    "CSS 'gap' is not supported in this browser — margin-based fallback spacing is already applied via styles.css."
  );
}

const supportsCSSVars =
  typeof window !== "undefined" &&
  window.CSS &&
  CSS.supports &&
  CSS.supports("(--a: 0)");

if (!supportsCSSVars && typeof cssVars === "function") {
  // css-vars-ponyfill (loaded via CDN in index.html) polyfills CSS custom
  // properties for browsers that don't support them natively (e.g. IE11).
  cssVars({
    include: "style,link[rel=stylesheet]",
    onlyLegacy: true,
  });
}

// ---------- Initial render ----------
renderCourses(courses);