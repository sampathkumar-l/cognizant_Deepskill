import { courses } from './data.js';


function fetchUser(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then(res => res.json())
    .then(user => {
      console.log('Promise chain — user name:', user.name);
      return user;
    });
}


async function fetchUserAsync(id) {
  try {
    const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    const user = await res.json();
    console.log('Async/await — user name:', user.name);
    return user;
  } catch (err) {
    console.error('fetchUserAsync failed:', err.message);
  }
}


function fetchAllCourses() {
  return new Promise(resolve => {
    setTimeout(() => resolve(courses), 1000);
  });
}

async function loadCoursesWithDelay() {
  const loadingMsg = document.getElementById('courses-loading');
  loadingMsg.textContent = 'Loading courses...';

  const data = await fetchAllCourses();

  loadingMsg.textContent = '';
  renderCourses(data);
  updateTotalCredits(data);
}


async function fetchTwoUsers() {
  const [user1, user2] = await Promise.all([
    fetch('https://jsonplaceholder.typicode.com/users/1').then(r => r.json()),
    fetch('https://jsonplaceholder.typicode.com/users/2').then(r => r.json())
  ]);
  console.log('Promise.all — both users:', user1.name, user2.name);
}

fetchUser(1);
fetchUserAsync(2);
loadCoursesWithDelay();
fetchTwoUsers();



async function apiFetch(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

async function loadNotifications(url = 'https://jsonplaceholder.typicode.com/posts?_limit=5') {
  const section = document.getElementById('notifications-list');
  const spinner = document.getElementById('notifications-spinner');
  const errorBox = document.getElementById('notifications-error');

  section.innerHTML = '';
  errorBox.innerHTML = '';
  spinner.style.display = 'block';

  try {
    const posts = await apiFetch(url);
    spinner.style.display = 'none';

    posts.forEach(post => {
      const card = document.createElement('div');
      card.className = 'notification-card';
      card.innerHTML = `<h4>${post.title}</h4><p>${post.body}</p>`;
      section.appendChild(card);
    });
  } catch (err) {
    spinner.style.display = 'none';
    errorBox.innerHTML = `
      <p class="error-msg">Couldn't load notifications: ${err.message}</p>
      <button id="retry-btn">Retry</button>
    `;
    document.getElementById('retry-btn').addEventListener('click', () => {
      loadNotifications('https://jsonplaceholder.typicode.com/posts?_limit=5');
    });
  }
}

document.getElementById('load-notifications').addEventListener('click', () => {
  loadNotifications();
});

document.getElementById('simulate-error').addEventListener('click', () => {
  loadNotifications('https://jsonplaceholder.typicode.com/nonexistent');
});

document.getElementById('load-notifications').addEventListener('click', () => {
  loadNotifications();
});

document.getElementById('simulate-error').addEventListener('click', () => {
  loadNotifications('https://jsonplaceholder.typicode.com/nonexistent');
});

async function apiFetchAxios(url, params = {}) {
  
  const response = await axios.get(url, { params });
  return response.data;
}

axios.interceptors.request.use(config => {
  console.log(`API call started: ${config.url}`);
  return config;
});

async function loadUser1Posts() {
  try {
    const posts = await apiFetchAxios('https://jsonplaceholder.typicode.com/posts', { userId: 1 });
    console.log('Axios — user 1 posts:', posts.length);
  } catch (err) {
    console.error('Axios request failed:', err.message);
  }
}

loadUser1Posts();

// Fetch vs Axios — 3 key differences:
// 1. Axios auto-parses JSON; Fetch requires a manual .json() call.
// 2. Axios rejects on HTTP error status codes (4xx/5xx); Fetch only rejects on network failure.
// 3. Axios supports request/response interceptors and built-in timeout; Fetch needs manual wiring for both.

/* ---------- Reused course rendering (from Hands-On 3) ---------- */

function renderCourses(list) {
  const grid = document.querySelector('.course-grid');
  grid.innerHTML = '';
  list.forEach(course => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    grid.appendChild(article);
  });
}

function updateTotalCredits(list) {
  const total = list.reduce((sum, c) => sum + c.credits, 0);
  document.getElementById('total-credits').textContent = `Total credits: ${total}`;
}