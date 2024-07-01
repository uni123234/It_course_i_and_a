import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app/app.component';
import { HelpCHComponent } from './app/help-c-h/help-c-h.component'

bootstrapApplication(AppComponent, {
  providers: [importProvidersFrom(ReactiveFormsModule), provideHttpClient()],
}).catch((err) => console.error(err));
