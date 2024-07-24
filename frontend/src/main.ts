import { enableProdMode, importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideClientHydration } from '@angular/platform-browser';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { provideServerRendering } from '@angular/platform-server';

if (process.env['NODE_ENV'] === 'production') {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient(),
    importProvidersFrom(ReactiveFormsModule),
    provideHttpClient(withFetch()),
    provideRouter(routes),
    provideServerRendering(),
    provideClientHydration(),
  ],
}).catch((err) => console.error(err));
