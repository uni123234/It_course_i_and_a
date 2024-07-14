import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-edit-password',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule, RouterOutlet],
  templateUrl: './edit-password.component.html',
  styleUrls: ['./edit-password.component.css'],
  providers: [DataService],
})
export class EditPasswordComponent {
  passwordForm: FormGroup;
  message: string = '';

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.passwordForm = this.fb.group({
      userId: ['', [Validators.required]],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      token: ['', [Validators.required]],
    });
  }

  requestPasswordChange() {
    if (this.passwordForm.valid) {
      const formValues = this.passwordForm.value;
      this.dataService.requestPasswordChange(formValues).subscribe(
        (response) => {
          this.message = response.message;
        },
        (error) => {
          this.message = 'An error occurred. Please try again.';
        }
      );
    } else {
      this.message = 'Please fill in all required fields.';
    }
  }
}
