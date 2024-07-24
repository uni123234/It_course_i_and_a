import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, map, Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private tokenSubject: BehaviorSubject<string | null>;
  private usernameSubject: BehaviorSubject<string | null>;
  public token$: Observable<string | null>;
  public username$: Observable<string | null>;
  private isBrowser: boolean;

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private cookieService: CookieService
  ) {
    this.isBrowser = isPlatformBrowser(this.platformId);

    // Initialize subjects with current cookie values or null
    const token = this.isBrowser ? this.cookieService.get('token') : null;
    const username = this.isBrowser ? this.cookieService.get('username') : null;

    this.tokenSubject = new BehaviorSubject<string | null>(token);
    this.usernameSubject = new BehaviorSubject<string | null>(username);
    this.token$ = this.tokenSubject.asObservable();
    this.username$ = this.usernameSubject.asObservable();
  }

  setToken(token: string) {
    if (this.isBrowser) {
      this.cookieService.set('token', token);
      this.tokenSubject.next(token);
    }
  }

  getToken(): Observable<string | null> {
    return this.token$;
  }

  isAuthenticated(): Observable<boolean> {
    // Directly return whether the token is available without any delays
    return this.token$.pipe(map(token => !!token));
  }

  setUser(username: string) {
    if (this.isBrowser) {
      this.cookieService.set('username', username);
      this.usernameSubject.next(username);
    }
  }

  getUsername(): Observable<string | null> {
    return this.username$;
  }

  deleteToken() {
    if (this.isBrowser) {
      this.cookieService.delete('token');
      this.tokenSubject.next(null);
    }
  }

  deleteUsername() {
    if (this.isBrowser) {
      this.cookieService.delete('username');
      this.usernameSubject.next(null);
    }
  }
}
