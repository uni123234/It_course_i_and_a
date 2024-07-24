import { AfterViewInit, Component, HostListener, Inject, PLATFORM_ID, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, NgForm, Validators } from '@angular/forms';
import {} from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterOutlet, CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [DataService],
  encapsulation: ViewEncapsulation.None,
})

export class LoginComponent {
  isAuthenticated: boolean = false;
  loginObj: LoginTemplate;
  credentialsError: string | null = null;
  // message: string = '';

  constructor(
    private fb: FormBuilder, 
    private dataService: DataService, 
    private router: Router,
    private authService: AuthService
  ) {
    this.loginObj = new LoginTemplate();
  }

  get emailInvalid(): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return !emailRegex.test(this.loginObj.email);
  }

  get passwordInvalid(): boolean {
    return this.loginObj.password.length < 6;
  }

    login(loginForm: NgForm) {;
      if (loginForm.valid && !this.emailInvalid && !this.passwordInvalid) {
          const loginData = {
              email: this.loginObj.email,
              password: this.loginObj.password,
              timestamp: new Date().toISOString()
          };
          console.log('abc')
          this.dataService.userLogin(loginData).subscribe({
              next: (response) => {
                  console.log('Login successful', response);
                  const username = response['user']['username']
                  if (username) {
                  this.authService.setUser(username) }
                  this.router.navigate(['/']);
              },
              error: (error) => {
                this.credentialsError = "Неправильне ім'я користувача або пароль";
                console.error('Register failed', error);
              },
          });
      }
  }

}

export class LoginTemplate {
  email: string;
  password: string;

  constructor() {
    this.email = "";
    this.password = "";
  }
}
