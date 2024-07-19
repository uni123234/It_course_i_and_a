import { Component, NgModule } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NoiseOverlayComponent } from './noise-overlay/noise-overlay.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NoiseOverlayComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
}
