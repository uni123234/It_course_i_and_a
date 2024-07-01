import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-login-in',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule],
  templateUrl: './login-in.component.html',
  styleUrls: ['./login-in.component.css'],
  providers: [DataService],
})
export class LoginInComponent {
  loginForm: FormGroup;
  message: string = '';

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  login() {
    if (this.loginForm.valid) {
      const credentials = this.loginForm.value;
      this.dataService.userLogin(credentials).subscribe(
        (response) => {
          this.message = response.message;
        },
        (error) => {
          this.message = 'An error occurred. Please try again.';
        }
      );
    } else {
      this.message = 'Please fill out all fields.';
    }
  }
}
