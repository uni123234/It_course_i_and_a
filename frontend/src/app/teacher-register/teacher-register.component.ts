import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
  ReactiveFormsModule,
} from '@angular/forms';
import { DataService } from '../data.service';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-teacher-register',
  standalone: true,
  imports: [ReactiveFormsModule, RouterOutlet],
  templateUrl: './teacher-register.component.html',
  styleUrls: ['./teacher-register.component.css'],
})
export class TeacherRegisterInComponent {
  registerForm: FormGroup;

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.registerForm = this.fb.group(
      {
        username: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        password1: ['', Validators.required],
        password2: ['', Validators.required],
      },
      { validators: this.passwordMatchValidator }
    );
  }

  passwordMatchValidator(
    control: AbstractControl
  ): { [key: string]: boolean } | null {
    const password = control.get('password1');
    const confirmPassword = control.get('password2');
    if (
      password &&
      confirmPassword &&
      password.value !== confirmPassword.value
    ) {
      return { passwordMismatch: true };
    }
    return null;
  }

  onSubmit() {
    if (this.registerForm.valid) {
      this.dataService.teacherRegister(this.registerForm.value).subscribe(
        (response) => {
          console.log('Teacher registration successful', response);
        },
        (error) => {
          console.error('Teacher registration failed', error);
        }
      );
    }
  }
}
