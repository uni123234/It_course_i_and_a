import { LoginPage, RegisterPage, HomePage, DashboardPage, CoursePage } from "./pages";
import { NavBar } from "./components";
import { createBrowserRouter } from "react-router-dom";

import { AuthGuard, LoginGuard } from "./features";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <NavBar />,
    children: [
      {
        path: "/",
        element: (
          <LoginGuard>
            <HomePage />
          </LoginGuard>
        ),
      },
      {
        path: "/login",
        element: (
          <LoginGuard>
            <LoginPage />
          </LoginGuard>
        ),
      },
      {
        path: "/register",
        element: (
          <LoginGuard>
            <RegisterPage />
          </LoginGuard>
        ),
      },
      {
        path: "/dashboard",
        element: (
          <AuthGuard>
            <DashboardPage />
          </AuthGuard>
        ),
      },
      {
        path: "/course/:courseId",
        element: (
          <AuthGuard>
            <CoursePage />
          </AuthGuard>
        ),
      },
    ],
  },
]);
