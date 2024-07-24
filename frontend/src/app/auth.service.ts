import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { jwtDecode } from 'jwt-decode';
import { CookieService } from 'ngx-cookie-service';
import { DOCUMENT } from '@angular/common';
import { Token } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private token: string;
  private username: string;

  constructor(@Inject(DOCUMENT) private document: Document, private cookieService: CookieService) {
    const cookies = this.parseCookies(this.document.cookie);
    this.token = cookies['token']
    this.username = cookies['username']
  }

  private parseCookies(cookieString: string): { [key: string]: string } {
    return cookieString.split(';').reduce((cookies, cookie) => {
      const [name, value] = cookie.split('=').map(c => c.trim());
      cookies[name] = value;
      return cookies;
    }, {} as { [key: string]: string });
  }

  setToken(token: string) {
    this.cookieService.set('token', token);
  }

  getToken(): string {
    return this.token;
  }
  
  isAuthenticated(): boolean { // fixed typo
    return !!this.getToken();
  }

  setUser(username: string) {
    this.cookieService.set('username', username);
  }

  getUsername(): string {
    return this.cookieService.get('username');
  }

  deleteToken() {
    this.cookieService.delete('token');
  }

  deleteUsername() {
    this.cookieService.delete('username');
  }
}
