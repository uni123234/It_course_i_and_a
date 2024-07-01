import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginInComponent } from './login-in.component';

describe('LoginInComponent', () => {
  let component: LoginInComponent;
  let fixture: ComponentFixture<LoginInComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginInComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LoginInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
