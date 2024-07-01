import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Sign_InComponent } from './sign-in.component';

describe('Sign_InComponent', () => {
  let component: Sign_InComponent;
  let fixture: ComponentFixture<Sign_InComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Sign_InComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(Sign_InComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
