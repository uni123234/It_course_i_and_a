import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../AuthProvider";

interface LoginGuardProps {
  children: React.ReactNode;
}

const LoginGuard: React.FC<LoginGuardProps> = ({ children }) => {
  const { isAuthenticated } = useAuth(); // Використання isAuthenticated

  return !isAuthenticated ? (
    <>{children}</>
  ) : (
    <Navigate to="/dashboard" />
  );
};

export default LoginGuard;