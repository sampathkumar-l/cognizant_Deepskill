import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import App from './App.jsx'
import { store } from './store.js'
// The Context provider from Task 2 is kept available for reference/comparison,
// but is not wired in here since Task 3 replaces it with the Redux store below.
// import { EnrollmentProvider } from './context/EnrollmentContext.jsx'

// Task 1, step 76: wrap <App /> in <BrowserRouter> for client-side routing.
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Provider store={store}>
        <App />
      </Provider>
    </BrowserRouter>
  </React.StrictMode>
)
