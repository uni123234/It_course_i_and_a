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

    login(loginForm: NgForm) {;
      if (loginForm.valid) {
          const loginData = {
              email: this.loginObj.email,
              password: this.loginObj.password,
              timestamp: new Date().toISOString()
          };
          this.dataService.userLogin(loginData).subscribe({
              next: (response) => {
                  console.log('Login successful', response);
                  const username = response['user']['username']
                  if (username) {
                  this.authService.setUser(username) }
                  this.router.navigate(['/']);
              },
              error: (error) => {
                  if (error.status === 401 && error.error.message === 'Invalid credentials') {
                      this.credentialsError = "Неправильне ім'я користувача або пароль";
                  } else {
                      console.error('Login failed', error);
                  }
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
