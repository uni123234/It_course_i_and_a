import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { DataService } from '../data.service';
import { HttpClientModule } from '@angular/common/http';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-teacher-login',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule,RouterOutlet],
  templateUrl: './teacher-login.component.html',
  styleUrls: ['./teacher-login.component.css'],
  providers: [DataService],
})
export class TeacherLoginComponent {
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
      this.dataService.teacherLogin(credentials).subscribe(
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
