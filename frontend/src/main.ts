import { bootstrapApplication, provideClientHydration } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http'; 
import { ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app/app.component';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(ReactiveFormsModule),
    provideHttpClient(withFetch()), 
    provideRouter(routes),
    provideClientHydration(),


  ],
}).catch((err) => console.error(err));
