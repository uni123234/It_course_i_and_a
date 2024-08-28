import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Login from './components/login/login.tsx'
import './index.css'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <div>Hello world!
      <button>a</button>
    </div>,
  },
  {
    path: "/login",
    element: <Login />
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
