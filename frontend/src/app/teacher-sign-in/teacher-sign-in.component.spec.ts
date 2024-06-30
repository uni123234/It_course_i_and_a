import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherSignInComponent } from './teacher-sign-in.component';

describe('TeacherSignInComponent', () => {
  let component: TeacherSignInComponent;
  let fixture: ComponentFixture<TeacherSignInComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherSignInComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TeacherSignInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
