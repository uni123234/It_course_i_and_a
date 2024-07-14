import { Component } from '@angular/core';
import { Route,RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-course',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './course.component.html',
  styleUrl: './course.component.css'
})
export class CourseComponent {

}
