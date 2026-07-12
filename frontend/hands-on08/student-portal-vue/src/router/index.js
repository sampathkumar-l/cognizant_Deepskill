import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// Step 112: routes for /, /courses, /courses/:id and /profile.
// Route-level code splitting: CoursesView, CourseDetailView and ProfileView
// are lazy-loaded so the initial bundle only contains HomeView.
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('../views/CoursesView.vue')
    },
    {
      path: '/courses/:id',
      name: 'course-detail',
      component: () => import('../views/CourseDetailView.vue'),
      props: true
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    }
  ]
})

// Step 116: navigation guard - logs every route change before it completes.
router.beforeEach((to, from) => {
  console.log(`Navigating to: ${to.path}`)
})

export default router
