import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../AuthProvider";

interface AuthGuardProps {
  children: React.ReactNode;
}

const AuthGuard: React.FC<AuthGuardProps> = ({ children }) => {
  const { isAuthenticated } = useAuth(); // Використання isAuthenticated

  return isAuthenticated ? (
    <>{children}</>
  ) : (
    <Navigate to="/login" />
  );
};

export default AuthGuard;