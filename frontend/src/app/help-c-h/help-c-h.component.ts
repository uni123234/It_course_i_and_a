import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {} from '@angular/common/http';
import { DataService } from '../data.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-help-c-h',
  standalone: true,
  imports: [ReactiveFormsModule, RouterOutlet],
  templateUrl: './help-c-h.component.html',
  styleUrls: ['./help-c-h.component.css'],
  providers: [DataService],
})
export class HelpCHComponent {
  helpRequestForm: FormGroup;
  message: string = '';

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.helpRequestForm = this.fb.group({
      courseId: ['', [Validators.required]],
      request: ['', [Validators.required]],
    });
  }

  submitHelpRequest() {
    if (this.helpRequestForm.valid) {
      const helpRequestData = this.helpRequestForm.value;
      this.dataService.submitHelpRequest(helpRequestData).subscribe(
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
