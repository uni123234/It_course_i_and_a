import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CookieService } from 'ngx-cookie-service';
import { DOCUMENT } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private token: string | null;
  private username: string | null;

  constructor(@Inject(PLATFORM_ID) private platformId: Object, @Inject(DOCUMENT) private document: Document, private cookieService: CookieService) {
    if (isPlatformBrowser(this.platformId)) {
      const cookies = this.parseCookies(this.document.cookie);
      this.token = cookies['token'];
      this.username = cookies['username'];
    } else {
      this.token = null;
      this.username = null;
    }
  }

  private parseCookies(cookieString: string): { [key: string]: string } {
    return cookieString.split(';').reduce((cookies, cookie) => {
      const [name, value] = cookie.split('=').map(c => c.trim());
      cookies[name] = value;
      return cookies;
    }, {} as { [key: string]: string });
  }

  setToken(token: string) {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.set('token', token);
      this.token = token;
    }
  }

  getToken(): string | null {
    return this.token;
  }
  
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  setUser(username: string) {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.set('username', username);
      this.username = username;
    }
  }

  getUsername(): string | null {
    return this.username;
  }

  deleteToken() {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.delete('token');
      this.token = null;
    }
  }

  deleteUsername() {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.delete('username');
      this.username = null;
    }
  }
}
