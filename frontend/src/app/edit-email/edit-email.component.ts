import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-edit-email',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule, RouterOutlet],
  templateUrl: './edit-email.component.html',
  styleUrls: ['./edit-email.component.css'],
  providers: [DataService],
})
export class EditEmailComponent {
  emailForm: FormGroup;
  message: string = '';

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.emailForm = this.fb.group({
      newEmail: ['', [Validators.required, Validators.email]],
    });
  }

  requestEmailChange() {
    if (this.emailForm.valid) {
      const newEmail = this.emailForm.get('newEmail')?.value;
      this.dataService.requestEmailChange(newEmail).subscribe(
        (response) => {
          this.message = response.message;
        },
        (error) => {
          this.message = 'An error occurred. Please try again.';
        }
      );
    } else {
      this.message = 'Please enter a valid email address.';
    }
  }
}
