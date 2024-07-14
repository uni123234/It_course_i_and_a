import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherRegisterInComponent } from './teacher-register.component';

describe('TeacherRegisterInComponent', () => {
  let component: TeacherRegisterInComponent;
  let fixture: ComponentFixture<TeacherRegisterInComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherRegisterInComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TeacherRegisterInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
