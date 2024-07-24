import { isPlatformBrowser } from '@angular/common';
import { Component, AfterViewInit, Inject, PLATFORM_ID } from '@angular/core';

@Component({
  selector: 'app-noise-overlay',
  templateUrl: './noise-overlay.component.html',
  styleUrls: ['./noise-overlay.component.css'],
  standalone: true
})
export class NoiseOverlayComponent implements AfterViewInit {

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.generateNoiseTexture();
    }
  }
  
  generateNoiseTexture(): void {
    const canvas = document.getElementById('noiseCanvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');

    if (ctx) {
      const width = window.innerWidth;
      const height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;

      const imageData = ctx.createImageData(width, height);
      const data = imageData.data;
      const density = 0.13; // 13% density

      for (let i = 0; i < data.length; i += 4) {
        const isParticle = Math.random() < density;
        const alpha = isParticle ? Math.floor(Math.random() * 20) : 0; // Random transparency up to 10%
        data[i] = 255; // Red
        data[i + 1] = 255; // Green
        data[i + 2] = 255; // Blue
        data[i + 3] = alpha; // Random transparency for particles, fully transparent otherwise
      }

      ctx.putImageData(imageData, 0, 0);
    }
  }

}
