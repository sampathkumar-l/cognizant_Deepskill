import { configureStore } from '@reduxjs/toolkit'
import enrollmentReducer from './features/enrollment/enrollmentSlice.js'

// Task 3, step 86: configureStore sets up the store with Redux DevTools
// support enabled automatically in development.
export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
})
