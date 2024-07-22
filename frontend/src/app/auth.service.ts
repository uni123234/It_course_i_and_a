import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'user_data';

  constructor() { }

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    const decodedToken = this.getDecodedToken();
    console.log(decodedToken)
  }

  getToken(): string | null {
    if (typeof localStorage !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  isAuthenticatedObservable(): Observable<boolean> {
    return of(this.isAuthenticated());
  }

  setUser(email: string): void {
    localStorage.setItem(this.USER_KEY, email);
  }

  getUser(): string | null {
    if (typeof localStorage !== 'undefined') {
      return localStorage.getItem(this.USER_KEY);
    }
    return null;
  }

  removeUser(): void {
    localStorage.removeItem(this.USER_KEY);
  }

  logout(): void {
    this.removeToken();
    this.removeUser();
  }

getDecodedToken(): any {
  const token = this.getToken();
  if (token) {
    try {
      return jwtDecode(token);
    } catch (error) {
      console.error('Token decode error:', error);
      return null;
    }
  }
  return null;
}
}