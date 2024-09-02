import { LoginPage, RegisterPage } from './pages';
import { createBrowserRouter } from "react-router-dom"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <div>Hello world!
    </div>,
  },
  {
    path: "/login",
    element: <LoginPage />
  },
  {
    path: '/register',
    element: <RegisterPage />
  }
]);
