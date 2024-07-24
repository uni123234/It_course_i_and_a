import { AfterViewInit, Component, HostListener, Inject, PLATFORM_ID, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, NgForm, Validators } from '@angular/forms';
import {} from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { CommonModule, isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterOutlet, ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  encapsulation: ViewEncapsulation.None,
})

export class RegisterComponent {
  regObj: RegTemplate;
  credentialsError: string | null = null;
  // message: string = '';

  constructor(
    private fb: FormBuilder, 
    private dataService: DataService, 
    private router: Router, 
  ) {
    this.regObj = new RegTemplate();
  }

  get emailInvalid(): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return !emailRegex.test(this.regObj.email);
  }

  get usernameInvalid(): boolean {
    return this.regObj.username.length < 6;
  }

  get passwordInvalid(): boolean {
    return this.regObj.password.length < 6;
  }

  get confirmInvalid(): boolean {
    return this.regObj.password != this.regObj.password2
  }

  register(regForm: NgForm) {
    console.log(this.regObj.email);
    if (regForm.valid && !this.emailInvalid && !this.passwordInvalid && !this.confirmInvalid && !this.usernameInvalid) {
      const regData = { email: this.regObj.email, password: this.regObj.password, username: this.regObj.username   };
      this.dataService.userRegister(regData).subscribe({
        next: (response) => {
          console.log('Register successful', response);
          this.router.navigate(['/login']);
        },
        error: (error) => {
          this.credentialsError = "Неправильне ім'я користувача або пароль";
          console.error('Register failed', error);
        },
      });
      // console.log("sfd " + this.authService.getToken());
    }
  }

}

export class RegTemplate {
  email: string;
  password: string;
  password2: string;
  username: string;

  constructor() {
    this.email = "";
    this.password = "";
    this.password2 = ""
    this.username = "";
  }
}
