import { LoginPage, RegisterPage, HomePage } from './pages';
import { createBrowserRouter } from "react-router-dom"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />
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
