// AuthProvider.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";
import Cookies from "js-cookie";

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
}

interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  fullname: string | null;
  isAuthenticated: boolean;
  login: (accessToken: string, refreshToken: string, user: User) => void;
  logout: () => void;
  getAccessToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(Cookies.get("accessToken") || null);
  const [refreshToken, setRefreshToken] = useState<string | null>(Cookies.get("refreshToken") || null);
  const [fullname, setFullname] = useState<string | null>(Cookies.get("fullname") || null);

  const isAuthenticated = !!accessToken;

  const login = (accessToken: string, refreshToken: string, user: User) => {
    const fullname = `${user.first_name} ${user.last_name}`;
    
    setAccessToken(accessToken);
    setRefreshToken(refreshToken);
    setFullname(fullname);

    // Збереження даних у кукі
    Cookies.set("accessToken", accessToken, { expires: 7 });
    Cookies.set("refreshToken", refreshToken, { expires: 7 });
    Cookies.set("fullname", fullname, { expires: 7 });
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    setFullname(null);

    // Видалення даних із кукі при виході
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
    Cookies.remove("fullname");
  };

  const getAccessToken = () => {
    return accessToken; // Returns the current access token
  };

  return (
    <AuthContext.Provider value={{ accessToken, refreshToken, fullname, isAuthenticated, getAccessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const isAuthenticated = () => {
  const context = useAuth();
  return context.isAuthenticated;
};
