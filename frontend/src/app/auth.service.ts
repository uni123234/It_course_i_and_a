import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'user_data';
  private loggedIn = new BehaviorSubject<boolean>(this.isTokenPresent());

  constructor() { }

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    const decodedToken = this.getDecodedToken();
    console.log(decodedToken)
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  isLoggedIn(): Observable<boolean> {
    return this.loggedIn.asObservable();
  }

  removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  private isTokenPresent(): boolean {
    return !!this.getToken();
  }

  getAuthorizationToken(): string | null {
    return this.getToken();
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
      return jwtDecode(token);
    }
    return null;
  }
}