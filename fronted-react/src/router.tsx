import Login from './pages/login.tsx'
import { createBrowserRouter } from "react-router-dom"

export const router = createBrowserRouter([
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
