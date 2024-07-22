import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';
import { Observable, take, map } from 'rxjs';
import { AuthService } from './auth.service';

export const loginGuard: CanActivateFn = (route, state) => {
  return true;
};

@Injectable({
  providedIn: 'root'
})

export class LoginGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> {
      return this.authService.isLoggedIn().pipe(
        take(1),
        map((isLoggedIn: boolean) => {
          if (isLoggedIn) {
            this.router.navigate(['/']);
            return false;
          }
          return true;
        })
      );
  }
}
