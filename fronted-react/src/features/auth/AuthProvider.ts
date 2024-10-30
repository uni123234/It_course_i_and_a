import React, { createContext, useContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);

    // Функція для логіна
    const login = (token, userData) => {
        // Зберігаємо токен та дані користувача у cookies
        Cookies.set('token', token, { expires: 7, secure: true });
        Cookies.set('user', JSON.stringify(userData), { expires: 7, secure: true });
        setToken(token);
        setUser(userData);
    };

    // Функція для логауту
    const logout = () => {
        Cookies.remove('token');
        Cookies.remove('user');
        setToken(null);
        setUser(null);
    };

    // Відновлення стану з cookies
    useEffect(() => {
        const storedToken = Cookies.get('token');
        const storedUser = Cookies.get('user');
        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
