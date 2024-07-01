import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-sign_in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css'],
})
export class Sign_InComponent {
  registerForm: FormGroup;

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password1: ['', Validators.required],
      password2: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.registerForm.valid) {
      this.dataService.userRegister(this.registerForm.value).subscribe(
        (response) => {
          console.log('Registration successful', response);
        },
        (error) => {
          console.error('Registration failed', error);
        }
      );
    }
  }
}
