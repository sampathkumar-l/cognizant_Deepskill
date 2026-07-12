# Student Portal — Vue.js (Hands-On 8)

Vue 3 rebuild of the Student Portal using the Composition API, Vue Router, and Pinia.

## Setup

```bash
npm install
npm run dev
```

Open the URL Vite prints (typically `http://localhost:5173`).

## Where each task lives

### Task 1 — Components & Reactive Data
- `src/components/Header.vue`, `src/components/CourseCard.vue` — single-file components
  (`<template>` / `<script setup>` / `<style scoped>`).
- `CourseCard.vue` — props declared with `defineProps` (`id`, `name`, `code`, `credits`, `grade`).
- `src/views/CoursesView.vue` — `ref([])` populated `onMounted` (simulated async load),
  `v-for` with `:key="course.id"`, props passed with `v-bind` shorthand, and a `computed`
  `filteredCourses` driven by a `searchTerm` ref bound with `v-model`.

### Task 2 — Vue Router
- `src/router/index.js` — routes for `/`, `/courses`, `/courses/:id`, `/profile`, plus a
  `router.beforeEach` guard that logs `Navigating to: <path>`.
- `src/App.vue` — `<RouterLink>` in the header nav (see `Header.vue`) and `<RouterView />`
  as the page outlet.
- `src/views/CourseDetailView.vue` — `useRoute()` to read the `:id` param, `useRouter().push('/profile')`
  after enrolling.

### Task 3 — Pinia
- `src/stores/enrollment.js` — `defineStore('enrollment', () => { ... })` setup-store with
  `enrolledCourses` state, a `totalCredits` computed getter, and `enroll` / `unenroll` actions.
- `CoursesView.vue` and `CourseDetailView.vue` call `store.enroll(course)`.
- `ProfileView.vue` lists `store.enrolledCourses` and shows `store.totalCredits`, using
  `storeToRefs` to destructure without losing reactivity.
- `Header.vue` shows `store.enrolledCourses.length` as the enrolled-course badge.

To inspect state changes live, install the **Vue DevTools** browser extension and open its
**Pinia** tab while enrolling/removing courses.
